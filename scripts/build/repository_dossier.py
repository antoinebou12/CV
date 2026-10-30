"""Derive a per-project technical dossier from cached, verified repository sources.

python scripts/build/repository_dossier.py [--repo uml-mcp] [--offline]

Reads the snapshot cached by repository_docs.py (_site/repository-docs-cache) and the
GitDiagram export, then writes hugo/data/repository_dossiers.json. Without --offline it
also fetches a few small build/CI/deploy files that the source scan skips (Dockerfile,
*.csproj, workflows, compose files). Repository code is read as text, never executed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path, PurePosixPath
from urllib.parse import quote

_SPEC = spec_from_file_location(
    "repository_docs", Path(__file__).with_name("repository_docs.py")
)
docs = module_from_spec(_SPEC)
_SPEC.loader.exec_module(docs)

ROOT = docs.ROOT
OUT = ROOT / "hugo/data/repository_dossiers.json"
EXTRA_MAX_BYTES = 300_000
EXTRA_MAX_FILES = 60
LIMIT = 14

# Layers are path conventions, shown top (closest to the user) to bottom.
LAYERS = [
    ("presentation", "Presentation", "Présentation"),
    ("interface", "Entry points and API", "Points d’entrée et API"),
    ("application", "Application services", "Services applicatifs"),
    ("domain", "Domain and business rules", "Domaine et règles métier"),
    ("infrastructure", "Data and infrastructure", "Données et infrastructure"),
    ("core", "Core source", "Source principale"),
]
SIDE_LAYERS = [
    ("tests", "Tests", "Tests"),
    ("hosting", "Build, CI and hosting", "Build, CI et hébergement"),
]
LAYER_DIRS = {
    "presentation": {
        "components", "pages", "views", "templates", "ui", "frontend", "public",
        "static", "layouts", "screens", "widgets", "web", "www", "client", "assets",
        "styles", "css", "res", "romfs", "gui", "app-ui", "console", "webui",
    },
    "interface": {
        "routes", "api", "apis", "controllers", "handlers", "endpoints", "cli",
        "commands", "server", "bin", "http", "rest", "graphql", "rpc", "mcp", "tools",
        "cmd", "entrypoints", "middleware",
    },
    "application": {
        "services", "service", "usecases", "use_cases", "application", "app",
        "workers", "jobs", "tasks", "managers", "pipeline", "pipelines", "engine",
        "jobs", "scheduler", "agents", "plugins", "scripts",
    },
    "domain": {
        "models", "model", "entities", "entity", "domain", "core", "schemas",
        "schema", "types", "dto", "dtos", "logic", "game", "strategy", "strategies",
        "algorithms", "simulation", "physics", "math", "geometry", "rules",
    },
    "infrastructure": {
        "db", "database", "migrations", "repositories", "repository", "storage",
        "persistence", "cache", "adapters", "clients", "integrations", "drivers",
        "hal", "platform", "sql", "prisma", "data", "io", "network", "net", "infra",
        "providers", "lib", "libs", "external",
    },
}
UI_EXT = {".vue", ".tsx", ".jsx", ".html", ".htm", ".css", ".scss", ".sass", ".svelte", ".blade.php", ".xml"}
SOURCE_EXT = set(docs.LANGUAGES) | UI_EXT | {".vue", ".java", ".kt", ".gradle", ".glsl", ".ino", ".ps1"}
HOSTING_NAMES = {
    "dockerfile", "docker-compose.yml", "docker-compose.yaml", "compose.yml",
    "compose.yaml", "vercel.json", "netlify.toml", "procfile", "fly.toml",
    "render.yaml", "wrangler.toml", "app.json", "makefile", "cmakelists.txt",
    "justfile", "taskfile.yml", "nginx.conf", "platformio.ini",
}
HOSTING_DIRS = {".github", ".gitlab", "ci", "deploy", "deployment", "k8s", "kubernetes", "helm", "terraform", "infra", "docker", ".devcontainer", "ansible"}
TEST_DIRS = {"test", "tests", "__tests__", "spec", "specs", "testing", "e2e", "integration_tests"}

EXTRA_NAMES = re.compile(
    r"(?:^|/)(?:Dockerfile[\w.\-]*|[\w.\-]*\.(?:csproj|fsproj|sql|prisma)|pom\.xml|go\.mod|"
    r"build\.gradle|settings\.gradle(?:\.kts)?|(?:docker-)?compose[\w.\-]*\.ya?ml|"
    r"openapi[\w.\-]*\.(?:ya?ml|json)|swagger[\w.\-]*\.(?:ya?ml|json)|SECURITY\.md|"
    r"pytest\.ini|tox\.ini|setup\.cfg|(?:jest|vitest|playwright|cypress)\.config\.\w+|"
    r"phpunit\.xml(?:\.dist)?|vercel\.json|netlify\.toml|fly\.toml|wrangler\.toml|"
    r"dependabot\.ya?ml|renovate\.json|codecov\.ya?ml)$"
)
WORKFLOW = re.compile(r"^\.github/workflows/[\w.\-]+\.ya?ml$")


def L(en, fr=None):
    return [en, fr or en]


# --- Pattern tables: (regex, name, kind) ---------------------------------------------

INTEGRATIONS = [
    (r"^\s*(?:import|from)\s+openai\b|api\.openai\.com|from ['\"]openai['\"]|require\(['\"]openai|langchain_openai", "OpenAI API", "ai"),
    (r"^\s*(?:import|from)\s+anthropic\b|api\.anthropic\.com|@anthropic-ai/", "Anthropic API", "ai"),
    (r"^\s*(?:import|from)\s+ollama\b|localhost:11434", "Ollama", "ai"),
    (r"huggingface_hub|from transformers import|api-inference\.huggingface", "Hugging Face", "ai"),
    (r"^\s*import whisper|faster_whisper|whisper\.load_model", "Whisper", "ai"),
    (r"\bkroki\b", "Kroki", "rendering"),
    (r"plantuml\.com|PlantUMLServer|plantuml_server", "PlantUML server", "rendering"),
    (r"api\.github\.com|\bOctokit\b|from github import|PyGithub", "GitHub API", "platform"),
    (r"\bboto3\b|@aws-sdk|aws-sdk|amazonaws\.com", "AWS", "cloud"),
    (r"azure\.identity|azure\.storage|@azure/|login\.microsoftonline\.com|using Azure\.", "Azure / Microsoft Entra", "cloud"),
    (r"(?<!fonts\.)googleapis\.com|google\.cloud|firebase", "Google Cloud / Firebase", "cloud"),
    (r"sentry_sdk|@sentry/|\bSentrySdk\b|using Sentry", "Sentry", "observability"),
    (r"^\s*import stripe|from ['\"]stripe|api\.stripe\.com", "Stripe", "payments"),
    (r"discord(?:\.py|\.js|api)|discord\.com/api", "Discord", "messaging"),
    (r"api\.telegram\.org|python-telegram-bot|telebot", "Telegram", "messaging"),
    (r"slack_sdk|hooks\.slack\.com|@slack/", "Slack", "messaging"),
    (r"\byfinance\b", "Yahoo Finance (yfinance)", "data"),
    (r"\balpaca\b", "Alpaca", "data"),
    (r"finnhub|polygon\.io|alphavantage|newsapi", "Market and news data APIs", "data"),
    (r"homeassistant\.", "Home Assistant", "platform"),
    (r"renpho", "Renpho cloud API", "data"),
    (r"paho\.mqtt|PubSubClient|\bmqtt\b", "MQTT broker", "messaging"),
    (r"socket\.io|\bwebsockets?\b|new WebSocket\(|ws://", "WebSocket", "transport"),
    (r"api\.spotify\.com|accounts\.spotify\.com|spotipy", "Spotify Web API", "data"),
    (r"donneesquebec|data\.gouv|ckan", "Open data portal (CKAN)", "data"),
    (r"api\.vercel\.com|@vercel/", "Vercel", "cloud"),
    (r"api\.cloudflare\.com|workers\.dev|@cloudflare/", "Cloudflare", "cloud"),
    (r"docker\.from_env|/var/run/docker\.sock|dockerode", "Docker Engine API", "platform"),
    (r"WiFiClient|HTTPClient\.h|esp_http_client", "Wi-Fi HTTP client (ESP32)", "transport"),
    (r"\bnifm\b|\bsocInitialize\b|curl_easy_", "Console network stack (libnx/libctru)", "transport"),
    (r"\bsmtplib\b|nodemailer|Mail::|PHPMailer", "Email (SMTP)", "messaging"),
]
HTTP_CLIENTS = [
    (r"^\s*import requests|^\s*from requests", "requests"),
    (r"\bhttpx\b", "httpx"),
    (r"\baiohttp\b", "aiohttp"),
    (r"urllib\.request|from urllib import request", "urllib"),
    (r"\bfetch\(", "fetch"),
    (r"\baxios\b", "axios"),
    (r"\breqwest\b", "reqwest"),
    (r"\bHttpClient\b", "HttpClient"),
    (r"curl_easy_|libcurl", "libcurl"),
    (r"OkHttp|Retrofit", "OkHttp / Retrofit"),
    (r"GuzzleHttp|Http::(?:get|post)", "Laravel HTTP / Guzzle"),
    (r"Net::HTTP|Faraday|HTTParty", "Ruby HTTP"),
]
DATABASES = [
    (r"^\s*import sqlite3|from sqlite3|aiosqlite|rusqlite|SQLiteDatabase|better-sqlite3|sqlite:///|sqlite3_open|Microsoft\.Data\.Sqlite", "SQLite", "sql"),
    (r"^\s*(?:import|from)\s+sqlalchemy|sqlmodel", "SQLAlchemy", "orm"),
    (r"psycopg|asyncpg|postgres(?:ql)?(?:\+\w+)?://|from ['\"]pg['\"]|require\(['\"]pg['\"]\)|Npgsql|org\.postgresql", "PostgreSQL", "sql"),
    (r"pymysql|mysql\.connector|mysql(?:\+\w+)?://|mysql2|MySqlConnector|com\.mysql|mariadb://|DB_CONNECTION=mysql", "MySQL / MariaDB", "sql"),
    (r"pymongo|motor\.motor_asyncio|mongoose|MongoClient|mongodb(?:\+srv)?://", "MongoDB", "document"),
    (r"^\s*import redis|from redis|ioredis|redis://|StackExchange\.Redis|require\(['\"]redis", "Redis", "key-value"),
    (r"@prisma/client|PrismaClient", "Prisma", "orm"),
    (r"typeorm|sequelize|\bknex\b|drizzle-orm", "Node ORM / query builder", "orm"),
    (r"\bdiesel\b|\bsqlx\b|\bsea_orm\b", "Rust SQL toolkit", "orm"),
    (r"\bsled\b|rocksdb|lmdb", "Embedded key-value store", "key-value"),
    (r"Illuminate\\Database|Schema::create|extends Model\b", "Eloquent ORM", "orm"),
    (r"ActiveRecord|ApplicationRecord", "Active Record", "orm"),
    (r"jakarta\.persistence|javax\.persistence|JpaRepository|@Entity\b", "JPA / Spring Data", "orm"),
    (r"androidx\.room|@Dao\b", "Room", "orm"),
    (r"SharedPreferences|DataStore<", "Android preferences", "local"),
    (r"localStorage|sessionStorage", "Browser localStorage", "local"),
    (r"indexedDB|IndexedDB|idb-keyval|localforage", "IndexedDB", "local"),
    (r"Preferences\.h|\bEEPROM\b|SPIFFS|LittleFS|nvs_flash", "Device flash storage", "local"),
    (r"DbContext|EntityFrameworkCore", "Entity Framework Core", "orm"),
    (r"\bDapper\b", "Dapper", "sql"),
    (r"\bh2database|jdbc:h2", "H2", "sql"),
    (r"\bpandas\b.*to_(?:csv|parquet)|\.to_csv\(|\.to_parquet\(", "CSV / Parquet files", "files"),
    (r"json\.dump\(|JSON\.stringify\(.*writeFile|fs\.writeFileSync", "JSON files", "files"),
]
TEST_FRAMEWORKS = [
    (r"^\s*import pytest|^\s*from pytest|@pytest\.", "pytest"),
    (r"^\s*import unittest|unittest\.TestCase", "unittest"),
    (r"from ['\"]vitest['\"]", "Vitest"),
    (r"@jest/|jest\.fn\(|from ['\"]@testing-library", "Jest / Testing Library"),
    (r"@playwright/test", "Playwright"),
    (r"\bcypress\b", "Cypress"),
    (r"#\[test\]|#\[cfg\(test\)\]|#\[tokio::test\]", "cargo test"),
    (r"org\.junit|@Test\b", "JUnit"),
    (r"\[Fact\]|\[Theory\]|using Xunit", "xUnit"),
    (r"using NUnit|\[TestFixture\]", "NUnit"),
    (r"extends TestCase|PHPUnit", "PHPUnit"),
    (r"RSpec\.describe|require ['\"]rails_helper", "RSpec"),
    (r"Minitest|ActiveSupport::TestCase", "Minitest"),
    (r"\bTEST_F?\(|gtest/gtest\.h", "GoogleTest"),
    (r"TEST_CASE\(|catch2", "Catch2"),
    (r"doctest\.h", "doctest"),
    (r"unity\.h|TEST_ASSERT_", "Unity (embedded)"),
]
TEST_CASES = re.compile(
    r"^\s*(?:async\s+)?def test_\w+|^\s*(?:it|test)\(\s*['\"`]|#\[(?:tokio::)?test\]|@Test\b|"
    r"\[Fact\]|\[Theory\]|\[Test\]|\bTEST_F?\(|TEST_CASE\(|^\s*public function test\w+",
    re.MULTILINE,
)
SECURITY = [
    (r"\bjwt\b|jsonwebtoken|PyJWT|JwtBearer", "JWT tokens", "auth"),
    (r"\boauth2?\b|authlib|OAuth2PasswordBearer|passport\.", "OAuth", "auth"),
    (r"[\"']Bearer |HTTPBearer|BearerAuth|bearer_token", "Bearer authentication", "auth"),
    (r"X-API-Key|api_key_header|APIKeyHeader", "API key header", "auth"),
    (r"Sanctum|Fortify|Auth::(?:attempt|user|check)|->middleware\(['\"]auth", "Laravel authentication", "auth"),
    (r"spring-boot-starter-security|SecurityFilterChain|@EnableWebSecurity", "Spring Security", "auth"),
    (r"\bdevise\b|has_secure_password", "Rails authentication", "auth"),
    (r"bcrypt|argon2|password_hash\(|PasswordHasher|scrypt", "Password hashing", "auth"),
    (r"\bhmac\b|compare_digest|timingSafeEqual", "HMAC / constant-time comparison", "auth"),
    (r"\bpydantic\b|BaseModel\)", "Pydantic validation", "validation"),
    (r"\bzod\b|\bjoi\b|\byup\b|class-validator", "Schema validation (TS)", "validation"),
    (r"jsonschema|marshmallow|cerberus", "JSON Schema validation", "validation"),
    (r"->validate\(|FormRequest|@Valid\b|@Validated\b", "Framework request validation", "validation"),
    (r"CORSMiddleware|flask_cors|\bcors\(|@CrossOrigin|AllowAnyOrigin|Access-Control-Allow-Origin", "CORS policy", "web"),
    (r"\bcsrf\b|CSRF|VerifyCsrfToken|@csrf", "CSRF protection", "web"),
    (r"\bhelmet\b|Content-Security-Policy|X-Frame-Options|Strict-Transport-Security", "Security headers", "web"),
    (r"slowapi|express-rate-limit|RateLimiter|rate_limit|ratelimit|ThrottleRequests|middleware\(['\"]throttle", "Rate limiting", "web"),
    (r"ssl\.create_default_context|ssl_context|WiFiClientSecure|rustls|native-tls|SslStream|https\.createServer|certfile=", "TLS configuration", "transport"),
    (r"keyring|SecretStr|secrets\.token_|crypto\.randomBytes|getrandom", "Secret handling / secure randomness", "secrets"),
]
REVIEW = [
    (r"shell\s*=\s*True", "subprocess with shell=True", ".py"),
    (r"verify\s*=\s*False", "TLS verification disabled", ".py"),
    (r"(?<![\w.])eval\(", "eval()", (".py", ".js", ".ts", ".php")),
    (r"pickle\.loads?\(", "pickle deserialization", ".py"),
    (r"yaml\.load\((?![^)]*Loader)", "yaml.load without SafeLoader", ".py"),
    (r"dangerouslySetInnerHTML|\.innerHTML\s*=", "raw HTML injection", (".js", ".ts", ".tsx", ".jsx", ".vue")),
    (r"\bstrcpy\(|\bsprintf\(|\bgets\(", "unbounded C string call", (".c", ".cpp", ".h", ".hpp", ".cc")),
]
ENV_VARS = re.compile(
    r"os\.environ(?:\.get)?[\[(]\s*['\"]([A-Z][A-Z0-9_]{2,})|os\.getenv\(\s*['\"]([A-Z][A-Z0-9_]{2,})|"
    r"process\.env\.([A-Z][A-Z0-9_]{2,})|process\.env\[['\"]([A-Z][A-Z0-9_]{2,})|"
    r"\benv\(\s*['\"]([A-Z][A-Z0-9_]{2,})|std::env::var\(\s*\"([A-Z][A-Z0-9_]{2,})|"
    r"getenv\(\s*\"([A-Z][A-Z0-9_]{2,})|GetEnvironmentVariable\(\s*\"([A-Z][A-Z0-9_]{2,})|"
    r"System\.getenv\(\s*\"([A-Z][A-Z0-9_]{2,})"
)
ROUTES = [
    (re.compile(r"@(?:\w+\.)?(?:app|router|bp|api|blueprint|\w+_router|\w+_bp)\.(get|post|put|patch|delete|route|websocket|api_route)\(\s*['\"]([^'\"]*)['\"]"), ".py"),
    (re.compile(r"\b(?:app|router|server|api|routes)\.(get|post|put|patch|delete|all)\(\s*['\"`](/[^'\"`]*)['\"`]"), (".js", ".ts", ".mjs", ".cjs")),
    (re.compile(r"Route::(get|post|put|patch|delete|resource|apiResource|match|any)\(\s*['\"]([^'\"]+)['\"]"), ".php"),
    (re.compile(r"@(Get|Post|Put|Delete|Patch|Request)Mapping\(\s*(?:value\s*=\s*|path\s*=\s*)?\{?\s*\"([^\"]*)\""), (".java", ".kt")),
    (re.compile(r"#\[(get|post|put|delete|patch)\(\s*\"([^\"]+)\""), ".rs"),
    (re.compile(r"\.route\(\s*\"([^\"]+)\"\s*,\s*(get|post|put|delete|patch)\("), ".rs"),
    (re.compile(r"\[Http(Get|Post|Put|Delete|Patch)\(\s*\"([^\"]*)\""), ".cs"),
    (re.compile(r"\.Map(Get|Post|Put|Delete|Patch)\(\s*\"([^\"]+)\""), ".cs"),
    (re.compile(r"^\s*(get|post|put|patch|delete|resources?)\s+['\":]([\w/:\-]+)", re.MULTILINE), "routes.rb"),
]
MCP_DECOR = re.compile(r"@(?:\w+\.)?(tool|resource|prompt)\((?:\s*['\"]([^'\"]+)['\"])?[^)]*\)\s*\n(?:\s*@[^\n]*\n)*\s*(?:async\s+)?def\s+(\w+)")
MCP_REGISTER = re.compile(r"\.(?:tool|registerTool|addTool)\(\s*['\"]([\w\-.]+)['\"]")
CLI = [
    (re.compile(r"add_parser\(\s*['\"]([\w\-]+)['\"]"), "subcommand"),
    (re.compile(r"add_argument\(\s*['\"](--?[\w\-]+)['\"]"), "option"),
    (re.compile(r"@(?:\w+\.)?command\((?:\s*(?:name\s*=\s*)?['\"]([\w\-]+)['\"])?[^)]*\)\s*\n(?:\s*@[^\n]*\n)*\s*def\s+(\w+)"), "command"),
    (re.compile(r"#\[(?:arg|clap)\(\s*(?:short,\s*)?long(?:\s*=\s*\"([\w\-]+)\")?"), "option"),
    (re.compile(r"\.option\(\s*['\"](--?[\w\-]+)"), "option"),
]
SERVICE_SUFFIX = re.compile(r"(Service|Manager|Client|Provider|Repository|Repo|Controller|Handler|Worker|Engine|Scheduler|Store|Gateway|Adapter|Router|Server|Renderer|Loader|Processor|Pipeline|Runner|Daemon)$")
ROLE = {
    "Controller": L("Controller", "Contrôleur"), "Handler": L("Handler", "Gestionnaire"),
    "Router": L("Router", "Routeur"), "Server": L("Server", "Serveur"),
    "Repository": L("Repository", "Dépôt de données"), "Repo": L("Repository", "Dépôt de données"),
    "Store": L("Store", "Magasin d’état"), "Client": L("Client", "Client"),
    "Gateway": L("Gateway", "Passerelle"), "Adapter": L("Adapter", "Adaptateur"),
    "Provider": L("Provider", "Fournisseur"),
}
LOGIC_HINT = re.compile(r"(?i)(service|engine|strategy|calculator|validator|processor|pipeline|solver|planner|scorer|parser|analy[sz]er|simulat|backtest|render|detector|classifier|scheduler|manager|game|physics|controller)")


NAME_FR = {
    "Python logging": "Journalisation Python",
    "Node logging": "Journalisation Node",
    ".NET logging": "Journalisation .NET",
    "JVM / Android logging": "Journalisation JVM / Android",
    "C++ logging": "Journalisation C++",
    "Rust logging": "Journalisation Rust",
    "Error reporting service": "Service de signalement d’erreurs",
    "Metrics endpoint": "Point de métriques",
    "Distributed tracing": "Traçage distribué",
    "Grafana dashboards": "Tableaux de bord Grafana",
    "Uptime monitoring": "Surveillance de disponibilité",
    "Web analytics": "Analytique web",
    "Alerting": "Alertes",
    "Market and news data APIs": "API de données de marché et d’actualités",
    "Open data portal (CKAN)": "Portail de données ouvertes (CKAN)",
    "Wi-Fi HTTP client (ESP32)": "Client HTTP Wi-Fi (ESP32)",
    "Console network stack (libnx/libctru)": "Pile réseau console (libnx/libctru)",
    "Email (SMTP)": "Courriel (SMTP)",
    "Renpho cloud API": "API infonuagique Renpho",
    "Node ORM / query builder": "ORM / constructeur de requêtes Node",
    "Rust SQL toolkit": "Boîte à outils SQL Rust",
    "Embedded key-value store": "Stockage clé-valeur embarqué",
    "Android preferences": "Préférences Android",
    "Browser localStorage": "localStorage du navigateur",
    "Device flash storage": "Mémoire flash de l’appareil",
    "CSV / Parquet files": "Fichiers CSV / Parquet",
    "JSON files": "Fichiers JSON",
    "JWT tokens": "Jetons JWT",
    "Bearer authentication": "Authentification Bearer",
    "API key header": "En-tête de clé d’API",
    "Laravel authentication": "Authentification Laravel",
    "Rails authentication": "Authentification Rails",
    "Password hashing": "Hachage des mots de passe",
    "HMAC / constant-time comparison": "HMAC / comparaison à temps constant",
    "Pydantic validation": "Validation Pydantic",
    "Schema validation (TS)": "Validation par schéma (TS)",
    "JSON Schema validation": "Validation JSON Schema",
    "Framework request validation": "Validation des requêtes du cadriciel",
    "CORS policy": "Politique CORS",
    "CSRF protection": "Protection CSRF",
    "Security headers": "En-têtes de sécurité",
    "Rate limiting": "Limitation de débit",
    "TLS configuration": "Configuration TLS",
    "Secret handling / secure randomness": "Gestion des secrets / aléa sûr",
    "subprocess with shell=True": "subprocess avec shell=True",
    "TLS verification disabled": "Vérification TLS désactivée",
    "pickle deserialization": "Désérialisation pickle",
    "yaml.load without SafeLoader": "yaml.load sans SafeLoader",
    "raw HTML injection": "Injection de HTML brut",
    "unbounded C string call": "Appel de chaîne C non borné",
}


def rel_url(analysis, path, line=None):
    return analysis["source_url"] + quote(path) + (f"#L{line}" if line else "")


def evidence(analysis, path, line=None):
    return {"file": path, "line": line, "url": rel_url(analysis, path, line)}


def line_of(text, index):
    return text.count("\n", 0, index) + 1


def is_test(path):
    p = PurePosixPath(path)
    parts = {x.lower() for x in p.parts[:-1]}
    name = p.name
    return bool(
        parts & TEST_DIRS
        or re.match(r"test_.*\.py$|conftest\.py$", name)
        or re.search(r"_test\.\w+$|\.(?:test|spec)\.\w+$|Tests?\.(?:java|kt|cs|php|swift)$", name)
    )


def layer_of(path):
    p = PurePosixPath(path)
    name = p.name.lower()
    parts = [x.lower() for x in p.parts[:-1]]
    if is_test(path):
        return "tests"
    if name in HOSTING_NAMES or name.startswith("dockerfile") or set(parts) & HOSTING_DIRS:
        return "hosting"
    # The deepest matching directory wins: src/api/models → domain.
    matched = None
    for part in parts:
        for layer, names in LAYER_DIRS.items():
            if part in names:
                matched = layer
    if matched:
        if matched == "presentation" and p.suffix.lower() in {".py", ".rs", ".go"} and not set(parts) & {"ui", "gui", "views", "templates"}:
            return "core"
        return matched
    if any(name.endswith(ext) for ext in UI_EXT):
        return "presentation"
    stem = p.stem.lower()
    if re.search(r"(^|_|-)(main|app|server|cli|index|routes?|api|__main__|handler|lambda)$", stem):
        return "interface"
    if re.search(r"service|manager|worker|pipeline|engine|scheduler", stem):
        return "application"
    if re.search(r"model|entity|schema|types?$|domain|dto", stem):
        return "domain"
    if re.search(r"db|database|repo(sitory)?|storage|cache|client|adapter|driver|migration", stem):
        return "infrastructure"
    return "core"


def is_source(path):
    p = PurePosixPath(path)
    name = p.name.lower()
    if any(part.startswith(".") and part not in {".github", ".devcontainer"} for part in p.parts[:-1]):
        return False  # IDE and tool folders (.idea, .vscode) are not project modules.
    return p.suffix.lower() in SOURCE_EXT or name.endswith(".blade.php")


GENERIC_DIRS = {"src", "source", "lib", "main", "java", "kotlin", "include", "packages", "crates", "app", "com", "org", "net"}


def module_key(path, depth=2):
    """Return (label, real prefix): up to `depth` meaningful folders, skipping src/lib/main."""
    parts = PurePosixPath(path).parts[:-1]
    if not parts:
        return "(root)", ""
    picked, end = [], 0
    for index, part in enumerate(parts):
        if part.lower() in GENERIC_DIRS and index < len(parts) - 1:
            continue
        picked.append(part)
        end = index + 1
        if len(picked) == depth:
            break
    if not picked:
        picked, end = [parts[0]], 1
    return "/".join(picked), "/".join(parts[:end])


def safe_extra(entry):
    path = PurePosixPath(entry["path"])
    if entry.get("type") != "blob" or entry.get("mode") == "120000" or entry.get("size", 0) > EXTRA_MAX_BYTES:
        return False
    if ".." in path.parts or any(p.lower() in docs.EXCLUDED - {"docs"} for p in path.parts):
        return False
    if any(p.startswith(".env") for p in path.parts):
        return False
    return bool(EXTRA_NAMES.search(entry["path"]) or WORKFLOW.match(entry["path"]))


def load_texts(repo, inputs, offline):
    commit = inputs["commit"]
    tree = inputs["tree"]["tree"]
    wanted = [e for e in tree if docs.source_candidate(e) and e.get("size", 0) <= docs.MAX_BYTES]
    extras = [e for e in tree if safe_extra(e) and not docs.source_candidate(e)][:EXTRA_MAX_FILES]
    texts = {}

    def read(entry, allow_fetch):
        cached = docs.CACHE / "blobs" / entry["sha"]
        if not cached.exists() and not allow_fetch:
            return None
        try:
            return entry["path"], docs.fetch_blob(repo, commit, entry, not allow_fetch)
        except (OSError, ValueError, UnicodeDecodeError):
            return None

    with ThreadPoolExecutor(max_workers=8) as pool:
        jobs = [pool.submit(read, e, False) for e in wanted]
        jobs += [pool.submit(read, e, not offline) for e in extras]
        for job in jobs:
            result = job.result()
            if result:
                texts[result[0]] = result[1]
    return texts


# --- Section builders ----------------------------------------------------------------


def build_layers(analysis, paths, types):
    sources = [p for p in paths if is_source(p) or layer_of(p) == "hosting"]
    type_count = Counter(t["file"] for t in types)
    buckets = {}
    for path in sources:
        layer = layer_of(path)
        module, prefix = module_key(path, 1 if layer in {"tests", "hosting"} else 2)
        bucket = buckets.setdefault(layer, {})
        item = bucket.setdefault(module, {"files": 0, "types": 0, "languages": Counter(), "prefix": prefix})
        item["files"] += 1
        item["types"] += type_count.get(path, 0)
        item["languages"][PurePosixPath(path).suffix.lower() or PurePosixPath(path).name] += 1
    layers = []
    for key, en, fr in LAYERS + SIDE_LAYERS:
        if key not in buckets:
            continue
        modules = sorted(buckets[key].items(), key=lambda kv: (-kv[1]["files"], kv[0]))
        layers.append(
            {
                "key": key,
                "label": [en, fr],
                "side": key in {k for k, _, _ in SIDE_LAYERS},
                "files": sum(m["files"] for _, m in modules),
                "types": sum(m["types"] for _, m in modules),
                "modules": [
                    {
                        "name": name,
                        "files": m["files"],
                        "types": m["types"],
                        "extensions": [ext for ext, _ in m["languages"].most_common(3)],
                        "url": analysis["tree_url"] + ("/" + quote(m["prefix"]) if m["prefix"] else ""),
                    }
                    for name, m in modules[:8]
                ],
                "more_modules": max(0, len(modules) - 8),
            }
        )
    return layers


def build_modules(analysis, paths, types):
    """Module inventory across layers: one row per meaningful folder."""
    type_count = Counter(t["file"] for t in types)
    rows = {}
    for path in paths:
        if not is_source(path) or is_test(path) or layer_of(path) == "hosting":
            continue
        name, prefix = module_key(path)
        row = rows.setdefault(name, {"name": name, "prefix": prefix, "files": 0, "types": 0, "layers": Counter(), "ext": Counter()})
        row["files"] += 1
        row["types"] += type_count.get(path, 0)
        row["layers"][layer_of(path)] += 1
        row["ext"][PurePosixPath(path).suffix.lower()] += 1
    labels = {k: [en, fr] for k, en, fr in LAYERS + SIDE_LAYERS}
    ranked = sorted(rows.values(), key=lambda r: (-r["files"], r["name"]))
    return {
        "items": [
            {
                "name": r["name"],
                "files": r["files"],
                "types": r["types"],
                "layer": labels[r["layers"].most_common(1)[0][0]],
                "extensions": [e for e, _ in r["ext"].most_common(3) if e],
                "url": analysis["tree_url"] + ("/" + quote(r["prefix"]) if r["prefix"] else ""),
            }
            for r in ranked[:LIMIT]
        ],
        "total": len(rows),
    }


def layers_mermaid(layers, lang):
    i = 1 if lang == "fr" else 0
    lines = ["flowchart TB"]
    main = [l for l in layers if not l["side"]]
    side = [l for l in layers if l["side"]]
    for layer in main + side:
        title = layer["label"][i].replace('"', "'")
        lines.append(f'  subgraph L_{layer["key"]}["{title}"]')
        lines.append("    direction LR")
        for index, module in enumerate(layer["modules"][:4]):
            name = module["name"].replace('"', "'")
            unit = "fichiers" if i else "files"
            lines.append(f'    {layer["key"]}_{index}["{name}<br/>{module["files"]} {unit}"]')
        if layer["more_modules"] or len(layer["modules"]) > 4:
            extra = layer["more_modules"] + max(0, len(layer["modules"]) - 4)
            lines.append(f'    {layer["key"]}_more["+{extra}"]')
        lines.append("  end")
    for upper, lower in zip(main, main[1:]):
        lines.append(f"  L_{upper['key']} ~~~ L_{lower['key']}")
    if main and side:
        for layer in side:
            lines.append(f"  L_{main[-1]['key']} ~~~ L_{layer['key']}")
    return "\n".join(lines) + "\n"


def parse_gitdiagram(analysis, paths):
    view = analysis.get("gitdiagram") or {}
    source = view.get("mermaid")
    if view.get("status") not in {"available", "needs_review"} or not source:
        return None
    by_name = {}
    for path in paths:
        by_name.setdefault(PurePosixPath(path).name, []).append(path)
    nodes, groups, edges, group = {}, [], [], None
    # Mermaid shapes: [rect] [[subroutine]] [(cylinder)] ([stadium]) ((circle)) {decision} {{hexagon}} [/slant/] >flag]
    node_re = re.compile(r'^\s*(\w+)\s*(?:\[\(|\(\[|\[\[?|\(\(?|\{\{?|\[/|>)"?(.*?)"?(?:\)\]|\]\)|\]\]?|\)\)?|\}\}?|/\])\s*$')
    edge_re = re.compile(r'^\s*(\w+)\s*(-\.->|-->|==>|---|-.-)\s*(?:\|"?(.*?)"?\|\s*)?(\w+)\s*$')
    for raw in source.splitlines():
        sub = re.match(r'^\s*subgraph\s+(\w+)\s*\["?(.*?)"?\]', raw)
        if sub:
            group = {"label": sub[2], "nodes": []}
            groups.append(group)
            continue
        if raw.strip() == "end":
            group = None
            continue
        edge = edge_re.match(raw)
        if edge:
            edges.append({"from": edge[1], "to": edge[4], "label": (edge[3] or "").strip(), "async": edge[2].startswith("-.")})
            continue
        node = node_re.match(raw)
        if node and node[1] not in {"flowchart", "graph", "direction"}:
            label = node[2]
            file_match = re.search(r"\[([^\]]+)\]\s*$", label.replace("<br/>", " "))
            name = re.sub(r"<br\s*/?>.*$", "", label).strip()
            entry = {"id": node[1], "label": name}
            if file_match:
                fname = file_match[1].strip()
                candidates = by_name.get(PurePosixPath(fname).name, [])
                entry["file"] = fname
                if len(candidates) == 1:
                    entry["url"] = rel_url(analysis, candidates[0])
                    entry["path"] = candidates[0]
            nodes[node[1]] = entry
            if group is not None:
                group["nodes"].append(node[1])
    if not edges:
        return None
    incoming = Counter(e["to"] for e in edges)
    starts = [n for n in nodes if incoming[n] == 0 and any(e["from"] == n for e in edges)]
    order, seen, queue = [], set(), list(starts) or [edges[0]["from"]]
    while queue:
        current = queue.pop(0)
        for index, e in enumerate(edges):
            if e["from"] == current and index not in seen:
                seen.add(index)
                order.append(e)
                queue.append(e["to"])
    order += [e for index, e in enumerate(edges) if index not in seen]
    label = lambda n: nodes.get(n, {"label": n.replace("node_", "").replace("_", " ")})
    steps = [
        {"from": label(e["from"])["label"], "to": label(e["to"])["label"], "label": e["label"], "async": e["async"]}
        for e in order[:24]
    ]
    return {
        "status": view["status"],
        "url": view.get("url"),
        "groups": [
            {"label": g["label"], "nodes": [label(n) for n in g["nodes"]]} for g in groups if g["nodes"]
        ],
        "steps": steps,
        "more_steps": max(0, len(order) - 24),
        "entry_points": [label(n)["label"] for n in starts[:4]],
        "sequence": sequence_mermaid(steps[:16]),
    }


def mlabel(text, limit=48):
    """Text that is safe inside a quoted Mermaid label."""
    text = re.sub(r"[\"<>{}|#;`]", "'", str(text)).replace("\n", " ").strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def sequence_mermaid(steps):
    """The GitDiagram edges in walk order, as a time-ordered sequence diagram."""
    if len(steps) < 2:
        return None
    names = list(dict.fromkeys(name for s in steps for name in (s["from"], s["to"])))
    ids = {name: f"P{index}" for index, name in enumerate(names)}
    lines = ["sequenceDiagram", "  autonumber"]
    lines += [f"  participant {ids[n]} as {mlabel(n, 32)}" for n in names]
    for s in steps:
        arrow = "--)" if s["async"] else "->>"
        lines.append(f"  {ids[s['from']]}{arrow}{ids[s['to']]}: {mlabel(s['label'] or '…', 40).replace(':', ' ')}")
    return "\n".join(lines) + "\n"


def scan_patterns(analysis, texts, table, code_only=True):
    found = {}
    for path, text in texts.items():
        if code_only and not is_source(path):
            continue
        for pattern, name, kind in table:
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                item = found.setdefault(name, {"name": name, "label": L(name, NAME_FR.get(name)), "kind": kind, "files": 0, "evidence": evidence(analysis, path, line_of(text, match.start())), "_tests": True})
                item["files"] += 1
                if not is_test(path) and item["_tests"]:
                    item["evidence"] = evidence(analysis, path, line_of(text, match.start()))
                    item["_tests"] = False
    result = sorted(found.values(), key=lambda x: (x["_tests"], -x["files"], x["name"]))
    for item in result:
        item.pop("_tests")
    return result[:LIMIT]


def external_hosts(analysis, texts, repo):
    ignore = re.compile(
        r"(?:^|\.)(?:w3\.org|schema\.org|json-schema\.org|example\.(?:com|org)|localhost|shields\.io|opensource\.org|"
        r"apache\.org|mozilla\.org|gnu\.org|creativecommons\.org|purl\.org|xmlns\.com|wikipedia\.org|"
        r"stackoverflow\.com|readthedocs\.io|python\.org|npmjs\.com|githubusercontent\.com|youtube\.com|"
        r"googletagmanager\.com|fonts\.googleapis\.com|fonts\.gstatic\.com|cdn\.jsdelivr\.net|unpkg\.com|cdnjs\.cloudflare\.com)$"
    )
    hosts = {}
    for path, text in texts.items():
        if not is_source(path) or is_test(path) or PurePosixPath(path).suffix.lower() in {".md", ".html", ".css"}:
            continue
        for match in re.finditer(r"[\"'`](?:https?|wss?)://([a-z0-9][a-z0-9.\-]+\.[a-z]{2,})(?::\d+)?[/\"'`?]", text, re.IGNORECASE):
            host = match[1].lower()
            if ignore.search(host) or re.match(r"^(?:\d+\.){3}\d+$", host):
                continue
            # The project's own deployments and documentation placeholders are not dependencies.
            if host == "github.com" or repo.lower() in host or re.search(r"(?:^|\.)(?:contoso|example|test|invalid)\.", host + "."):
                continue
            item = hosts.setdefault(host, {"host": host, "files": set(), "evidence": evidence(analysis, path, line_of(text, match.start()))})
            item["files"].add(path)
    ranked = sorted(hosts.values(), key=lambda h: (-len(h["files"]), h["host"]))[:10]
    return [{"host": h["host"], "files": len(h["files"]), "evidence": h["evidence"]} for h in ranked]


def build_integrations(analysis, texts, repo):
    clients = []
    for pattern, name in HTTP_CLIENTS:
        for path, text in texts.items():
            if is_source(path) and not is_test(path):
                match = re.search(pattern, text, re.MULTILINE)
                if match:
                    clients.append({"name": name, "evidence": evidence(analysis, path, line_of(text, match.start()))})
                    break
    return {
        "services": scan_patterns(analysis, {p: t for p, t in texts.items() if not p.lower().endswith(".md")}, INTEGRATIONS),
        "http_clients": clients,
        "hosts": external_hosts(analysis, texts, repo),
    }


def compose_images(analysis, texts):
    images = []
    for path, text in texts.items():
        name = PurePosixPath(path).name.lower()
        if re.match(r"(?:docker-)?compose.*\.ya?ml$", name):
            for match in re.finditer(r"^\s*image:\s*['\"]?([\w./\-]+)(?::([\w.\-]+))?", text, re.MULTILINE):
                images.append({"image": match[1], "tag": match[2] or "", "evidence": evidence(analysis, path, line_of(text, match.start()))})
    return images


def build_database(analysis, texts, paths):
    engines = scan_patterns(analysis, {p: t for p, t in texts.items() if not p.lower().endswith(".md")}, DATABASES)
    tables = {}
    for path, text in texts.items():
        if not (is_source(path) or path.endswith(".sql")) or is_test(path):
            continue
        for pattern in (
            r"CREATE TABLE(?: IF NOT EXISTS)?\s+[`\"\[]?(\w+)",
            r"Schema::create\(\s*['\"](\w+)['\"]",
            r"create_table\s+:(\w+)",
            r"__tablename__\s*=\s*['\"](\w+)['\"]",
            r"@Table\(\s*name\s*=\s*\"(\w+)\"",
            r"@Entity\(\s*tableName\s*=\s*\"(\w+)\"",
            r"^\s*model\s+(\w+)\s*\{",
        ):
            for match in re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE):
                tables.setdefault(match[1], evidence(analysis, path, line_of(text, match.start())))
    migrations = [p for p in paths if re.search(r"(?:^|/)(?:migrations?|db/migrate|alembic/versions)/", p)]
    stores = [i for i in compose_images(analysis, texts) if re.search(r"postgres|mysql|mariadb|mongo|redis|sqlite|influx|elastic|minio|valkey|clickhouse|qdrant|chroma", i["image"], re.I)]
    return {
        "engines": engines,
        "tables": [{"name": k, **v} for k, v in list(tables.items())[:LIMIT]],
        "table_count": len(tables),
        "migrations": len(migrations),
        "migration_dir": (analysis["tree_url"] + "/" + quote(str(PurePosixPath(migrations[0]).parent))) if migrations else None,
        "containers": stores[:8],
    }


def entity_kind(t, text_lines):
    line = text_lines[t["line"] - 1] if 0 < t["line"] <= len(text_lines) else ""
    before = "\n".join(text_lines[max(0, t["line"] - 4) : t["line"] - 1])
    bases = " ".join(t.get("bases", []))
    lang = t["language"]
    if lang in {"php", "csharp"} and re.search(r"(?:^|/)(?:Models|Entities)/", t["file"]):
        return "orm" if lang == "php" else "record"
    if re.search(r"@Entity|@Table|\(db\.Model\)|\bModel\b|Authenticatable|ApplicationRecord|DeclarativeBase|\bBase\b", before + " " + bases + " " + line) and lang in {"python", "java", "kotlin", "php", "ruby"}:
        if lang != "python" or re.search(r"db\.Model|DeclarativeBase|\bBase\b|SQLModel|models\.Model", bases):
            return "orm"
    if lang == "python":
        if re.search(r"BaseModel|SQLModel|BaseSettings", bases):
            return "schema"
        if "@dataclass" in before or "attrs.define" in before or "@define" in before:
            return "dataclass"
        if re.search(r"TypedDict|NamedTuple", bases):
            return "record"
        if re.search(r"\bEnum\b|IntEnum|StrEnum|Flag", bases):
            return "enum"
        return None
    if t["kind"] in {"enum"}:
        return "enum"
    if t["kind"] == "record" or re.search(r"\bdata class\b|\brecord\b", line):
        return "record"
    if lang == "rust" and t["kind"] == "struct" and re.search(r"derive\([^)]*(Serialize|Deserialize|Clone|Debug|PartialEq)", before):
        return "record"
    if lang in {"typescript", "tsx"} and t["kind"] == "interface" and not t["methods"]:
        return "record"
    if lang in {"c", "cpp", "go"} and t["kind"] == "struct" and not t["methods"]:
        return "struct"
    if lang == "csharp" and not t["methods"] and re.search(r"Models?|Dto|Entities", t["file"]):
        return "record"
    return None


def entity_fields(t, lines):
    """(name, type) pairs for the first fields of a data type; type is "" when not declared."""
    fields = []
    start = t["line"]
    if t["language"] == "php":
        block = "\n".join(lines[start : start + 80])
        match = re.search(r"\$fillable\s*=\s*\[([^\]]*)\]", block)
        return [(name, "") for name in re.findall(r"['\"](\w+)['\"]", match[1])[:8]] if match else []
    indent = None
    for raw in lines[start : start + 40]:
        if not raw.strip():
            continue
        current = len(raw) - len(raw.lstrip())
        if indent is None:
            indent = current
        if t["language"] == "python" and current < indent:
            break
        if re.match(r"^\s*(?:def |fn |public .*\(|func |\}\s*$)", raw) and fields:
            break
        patterns = [
            r"^\s*(\w+)\??\s*:\s*([^=#;]+?)\s*(?:=|#|;|$)",                  # py / ts
            r"^\s*(?:pub(?:\(crate\))?\s+)?(\w+)\s*:\s*([^,]+),",           # rust
            r"^\s*(\w+)\s*=\s*(?:db\.)?(?:Column|Field|mapped_column)\(()",   # orm
            r"^\s*(?:private|public|protected)?\s*(?:val|var)\s+(\w+)\s*:\s*([\w<>?, ]+)",  # kotlin
            r"^\s*(?:private|public|protected)\s+([\w<>\[\], ?]+)\s+(\w+)\s*(?:;|=|\{)",  # java / c#
            r"^\s*(?:const\s+)?([\w:<>*& ]+?)\s+\*?(\w+)(?:\[[^\]]*\])?\s*;",      # c / c++
        ]
        for index, pattern in enumerate(patterns):
            match = re.match(pattern, raw)
            if match:
                name, kind = (match[2], match[1]) if index in {4, 5} else (match[1], match[2] or "")
                if name not in {"return", "class", "self", "const", "static", "else", "if", "pass", "typedef"} and not name.startswith("__"):
                    fields.append((name, kind.strip().rstrip(",;")))
                break
        if len(fields) >= 8:
            break
    return list({name: (name, kind) for name, kind in fields}.values())


def mermaid_type(kind):
    """list[Item] -> list~Item~; nested or multi-argument generics keep only the outer name."""
    kind = kind.strip().replace("Optional[", "").replace("Option<", "")
    match = re.match(r"^([\w.:]+)\s*[\[<]\s*([\w.]+)\s*[\]>]+\??$", kind)
    if match:
        return f"{match[1].split('.')[-1]}~{match[2].split('.')[-1]}~"
    head = re.match(r"^[\w.:]+", kind)
    return head[0].split(".")[-1].split("::")[-1] if head else ""


def entity_mermaid(items):
    """Class diagram of the listed entities; an arrow means a field's type names another entity."""
    if len(items) < 2:
        return None
    picked = list({e["name"]: e for e in items}.values())[:10]
    names = {e["name"] for e in picked}
    ids = {e["name"]: f"E{index}" for index, e in enumerate(picked)}
    lines = ["classDiagram", "  direction LR"]
    relations = []
    for e in picked:
        lines.append(f'  class {ids[e["name"]]}["{mlabel(e["name"], 40)}"] {{')
        if e["kind"] == "enum":
            lines.append("    <<enumeration>>")
        for name, kind in e["field_types"][:6]:
            mtype = mermaid_type(kind)
            lines.append(f"    +{mtype + ' ' if mtype else ''}{name}")
            for other in names - {e["name"]}:
                if re.search(r"\b" + re.escape(other) + r"\b", kind):
                    relations.append(f"  {ids[e['name']]} --> {ids[other]} : {name}")
        lines.append("  }")
    lines += list(dict.fromkeys(relations))
    return "\n".join(lines) + "\n"


CONSTRUCTORS = {"__init__", "__new__", "constructor", "new", "init", "initialize"}


def behaviour(t):
    """Methods that say what a type does: constructors and destructors repeat the type name."""
    return [m for m in t["methods"] if m not in CONSTRUCTORS and m.lstrip("~") != t["name"]]


GENERATED = re.compile(r"(?:^|/)(?:pkg|__generated__|generated|gen)/|\.(?:g|generated|pb|min)\.\w+$|_pb2\.py$")


def generated(t):
    """Code emitted by tools (wasm-pack pkg/, protobuf, *.g.cs) describes the tool, not the project."""
    return bool(GENERATED.search(t["file"])) or "__destroy_into_raw" in t["methods"]


def unique(items, key):
    """Drop repeats: a type defined twice (two files, two platforms) would print the same row twice."""
    seen, kept = set(), []
    for item in items:
        k = key(item)
        if k not in seen:
            seen.add(k)
            kept.append(item)
    return kept


def build_entities(analysis, texts, types):
    order = {"orm": 0, "schema": 1, "dataclass": 2, "record": 3, "enum": 4, "struct": 5}
    found = []
    for t in types:
        if is_test(t["file"]) or generated(t) or t["file"] not in texts:
            continue
        lines = texts[t["file"]].splitlines()
        kind = entity_kind(t, lines)
        if not kind:
            continue
        pairs = entity_fields(t, lines)
        found.append({"name": t["name"], "kind": kind, "fields": [n for n, _ in pairs], "field_types": pairs, **evidence(analysis, t["file"], t["line"])})
    found.sort(key=lambda e: (order[e["kind"]], -len(e["fields"]), layer_of(e["file"]) != "domain", e["name"]))
    found = unique(found, lambda e: (e["name"], tuple(e["fields"])))
    counts = Counter(e["kind"] for e in found)
    items = found[:LIMIT]
    diagram = entity_mermaid(items)
    for item in items:
        item.pop("field_types")
    return {"items": items, "total": len(found), "by_kind": dict(counts), "diagram": diagram}


def build_services(analysis, texts, types, paths):
    roles = {}
    for t in types:
        if is_test(t["file"]) or generated(t):
            continue
        match = SERVICE_SUFFIX.search(t["name"])
        if not match:
            continue
        suffix = match[1]
        role = ROLE.get(suffix, L("Service", "Service"))
        methods = behaviour(t)
        roles.setdefault(role[0], {"label": role, "items": []})["items"].append(
            {"name": t["name"], "methods": methods[:5], "method_count": len(methods), **evidence(analysis, t["file"], t["line"])}
        )
    for group in roles.values():
        group["items"] = unique(group["items"], lambda x: (x["name"], tuple(x["methods"])))
        group["total"] = len(group["items"])
        group["items"] = sorted(group["items"], key=lambda x: -x["method_count"])[:8]
    hosting = []
    signals = [
        (r"(?:^|/)Dockerfile[\w.\-]*$", "Docker image", "Image Docker"),
        (r"(?:^|/)(?:docker-)?compose[\w.\-]*\.ya?ml$", "Docker Compose stack", "Pile Docker Compose"),
        (r"(?:^|/)vercel\.json$", "Vercel", "Vercel"),
        (r"(?:^|/)netlify\.toml$", "Netlify", "Netlify"),
        (r"(?:^|/)fly\.toml$", "Fly.io", "Fly.io"),
        (r"(?:^|/)wrangler\.toml$", "Cloudflare Workers", "Cloudflare Workers"),
        (r"(?:^|/)Procfile$", "Procfile (Heroku-style)", "Procfile (style Heroku)"),
        (r"(?:^|/)render\.yaml$", "Render", "Render"),
        (r"\.service$", "systemd unit", "Unité systemd"),
        (r"(?:^|/)(?:k8s|kubernetes|helm)/", "Kubernetes manifests", "Manifestes Kubernetes"),
        (r"(?:^|/)platformio\.ini$", "PlatformIO firmware build", "Build firmware PlatformIO"),
        (r"\.nro$|(?:^|/)Makefile$.*", "Native build (Make)", "Build natif (Make)"),
        (r"(?:^|/)CMakeLists\.txt$", "CMake build", "Build CMake"),
        (r"(?:^|/)\.devcontainer/", "Dev container", "Conteneur de développement"),
        (r"(?:^|/)mkdocs\.ya?ml$", "MkDocs site", "Site MkDocs"),
        (r"(?:^|/)hugo\.toml$|(?:^|/)config\.toml$", "Static site generator", "Générateur de site statique"),
    ]
    for pattern, en, fr in signals:
        hits = [p for p in paths if re.search(pattern, p)]
        if hits:
            hosting.append({"label": [en, fr], "count": len(hits), **evidence(analysis, hits[0])})
    deploys = [path for path, text in texts.items() if WORKFLOW.match(path) and re.search(r"pages|deploy|vercel|docker/build-push|gh-pages|publish|release", text, re.I)]
    if deploys:
        hosting.append({"label": ["CI deploy workflow", "Workflow de déploiement CI"], "count": len(deploys), **evidence(analysis, deploys[0])})
    containers = []
    for path, text in texts.items():
        if re.search(r"(?:^|/)(?:docker-)?compose[\w.\-]*\.ya?ml$", path, re.I):
            block = re.search(r"^services:\s*\n((?:[ \t]+.*\n|\s*\n)+)", text + "\n", re.MULTILINE)
            if block:
                for match in re.finditer(r"^ {2}([\w.\-]+):\s*$", block[1], re.MULTILINE):
                    containers.append(match[1])
    from_images = []
    for path, text in texts.items():
        if PurePosixPath(path).name.lower().startswith("dockerfile"):
            for match in re.finditer(r"^\s*FROM\s+(?:--platform=\S+\s+)?([\w./\-:@]+)", text, re.MULTILINE | re.IGNORECASE):
                from_images.append({"image": match[1], **evidence(analysis, path, line_of(text, match.start()))})
    return {
        "roles": sorted(roles.values(), key=lambda g: -g["total"]),
        "hosting": hosting[:10],
        "containers": list(dict.fromkeys(containers))[:16],
        "base_images": from_images[:8],
    }


def build_logic(analysis, texts, types, entity_names):
    ranked = []
    for t in types:
        if is_test(t["file"]) or generated(t) or t["name"] in entity_names or layer_of(t["file"]) in {"presentation", "hosting", "tests"}:
            continue
        methods = behaviour(t)
        score = len(methods) + (6 if LOGIC_HINT.search(t["name"] + " " + t["file"]) else 0) + (4 if layer_of(t["file"]) in {"domain", "application"} else 0)
        if len(methods) < 2:
            continue
        ranked.append((score, t, methods))
    ranked.sort(key=lambda x: (-x[0], x[1]["name"]))
    # Identical method lists (copies of one class) are listed once.
    ranked = unique(unique(ranked, lambda x: tuple(x[2])), lambda x: x[1]["name"])
    items = [
        {"name": t["name"], "kind": t["kind"], "layer": layer_of(t["file"]), "methods": methods[:6], "method_count": len(methods), **evidence(analysis, t["file"], t["line"])}
        for _, t, methods in ranked[:10]
    ]
    files = []
    if not items:
        sizes = {e["path"]: e.get("size", 0) for e in analysis.get("_tree", [])}
        candidates = sorted(
            (p for p in texts if is_source(p) and not is_test(p) and layer_of(p) not in {"presentation", "hosting"} and not p.lower().endswith(".md")),
            key=lambda p: -sizes.get(p, len(texts[p])),
        )
        for path in candidates[:6]:
            functions = re.findall(r"^\s*(?:async\s+)?(?:def|function|fn|func|sub)\s+(\w+)|^(\w+)\s*\(\)\s*\{", texts[path], re.MULTILINE)
            names = [a or b for a, b in functions]
            files.append({"functions": names[:6], "function_count": len(names), **evidence(analysis, path)})
    return {"types": items, "files": files}


def build_public(analysis, texts, types, manifests):
    routes = []
    for path, text in texts.items():
        if is_test(path):
            continue
        for pattern, suffix in ROUTES:
            suffixes = suffix if isinstance(suffix, tuple) else (suffix,)
            if not path.endswith(suffixes):
                continue
            for match in pattern.finditer(text):
                a, b = match[1], match[2]
                method, route = (b, a) if pattern.pattern.startswith(r"\.route") else (a, b)
                routes.append({"method": method.upper().replace("ROUTE", "ANY").replace("API_ROUTE", "ANY"), "path": route or "/", **evidence(analysis, path, line_of(text, match.start()))})
    tools = []
    for path, text in texts.items():
        if is_test(path) or not is_source(path):
            continue
        if path.endswith(".py"):
            for match in MCP_DECOR.finditer(text):
                if re.search(r"mcp|server|fastmcp", text[: match.start()], re.IGNORECASE):
                    tools.append({"kind": match[1], "name": match[2] or match[3], **evidence(analysis, path, line_of(text, match.start()))})
        elif re.search(r"modelcontextprotocol|McpServer", text):
            for match in MCP_REGISTER.finditer(text):
                tools.append({"kind": "tool", "name": match[1], **evidence(analysis, path, line_of(text, match.start()))})
    cli = []
    for path, text in texts.items():
        if is_test(path) or not is_source(path):
            continue
        for pattern, kind in CLI:
            for match in pattern.finditer(text):
                name = next((g for g in match.groups() if g), None)
                if name and name not in {"-h", "--help"}:
                    cli.append({"kind": kind, "name": name, **evidence(analysis, path, line_of(text, match.start()))})
    entry_points = []
    for path, text in texts.items():
        name = PurePosixPath(path).name
        if name == "pyproject.toml":
            try:
                data = tomllib.loads(text)
            except tomllib.TOMLDecodeError:
                continue
            for key, value in (data.get("project", {}).get("scripts", {}) | data.get("tool", {}).get("poetry", {}).get("scripts", {})).items():
                entry_points.append({"name": key, "target": str(value), "kind": "console script", **evidence(analysis, path)})
        elif name == "package.json":
            try:
                data = json.loads(text)
            except ValueError:
                continue
            if isinstance(data, dict):
                bins = data.get("bin")
                if isinstance(bins, str):
                    entry_points.append({"name": data.get("name", "bin"), "target": bins, "kind": "bin", **evidence(analysis, path)})
                elif isinstance(bins, dict):
                    for key, value in bins.items():
                        entry_points.append({"name": key, "target": str(value), "kind": "bin", **evidence(analysis, path)})
                for key in ("main", "module", "types"):
                    if isinstance(data.get(key), str):
                        entry_points.append({"name": key, "target": data[key], "kind": "package export", **evidence(analysis, path)})
        elif name == "__main__.py" or re.fullmatch(r"main\.(?:py|rs|go|c|cpp|cc|kt|java|ts|js)|Program\.cs|server\.(?:py|ts|js)|app\.(?:py|ts|js)|index\.(?:ts|js)", name):
            if len(PurePosixPath(path).parts) <= 3 and not is_test(path):
                entry_points.append({"name": name, "target": path, "kind": "entry file", **evidence(analysis, path)})
    exported = []
    for path, text in texts.items():
        if path.endswith("__init__.py"):
            match = re.search(r"__all__\s*=\s*[\[(]([^\])]+)", text)
            if match:
                exported.extend(re.findall(r"['\"](\w+)['\"]", match[1]))
    public_types = [t for t in types if not t["name"].startswith("_") and not is_test(t["file"]) and not re.search(r"(?:^|/)(?:internal|private|detail|impl)/", t["file"])]
    headers = [p for p in texts if re.search(r"(?:^|/)include/.*\.(?:h|hpp|hh)$", p)]
    dedupe = lambda items, key: list({key(i): i for i in items}.values())
    unique_routes = dedupe(routes, lambda r: (r["method"], r["path"]))
    for route in unique_routes:
        route["ops"] = bool(OPS_ROUTE.search(route["path"]))
    return {
        "routes": unique_routes[:24],
        "route_total": len(unique_routes),
        "route_map": route_mermaid(unique_routes),
        "mcp": dedupe(tools, lambda t: (t["kind"], t["name"]))[:24],
        "mcp_total": len(dedupe(tools, lambda t: (t["kind"], t["name"]))),
        "cli": dedupe(cli, lambda c: (c["kind"], c["name"]))[:18],
        "cli_total": len(dedupe(cli, lambda c: (c["kind"], c["name"]))),
        "entry_points": dedupe(entry_points, lambda e: (e["kind"], e["name"], e["target"]))[:10],
        "exports": list(dict.fromkeys(exported))[:24],
        "public_types": len(public_types),
        "headers": [evidence(analysis, p) for p in sorted(headers)[:10]],
        "header_total": len(headers),
    }


OPS_ROUTE = re.compile(r"(?i)(?:^|/)(?:admin|internal|debug|health|healthz|ready|readyz|live|metrics|status)(?:/|$)")


def route_mermaid(routes):
    """HTTP routes grouped by their first path segment, as a left-to-right tree."""
    if len(routes) < 3:
        return None
    groups = {}
    for route in routes:
        segment = route["path"].strip("/").split("/")[0] or "/"
        groups.setdefault(segment, []).append(route)
    lines = ["flowchart LR", '  api(["HTTP API"])']
    for gi, (segment, items) in enumerate(sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:10]):
        label = "/" if segment == "/" else f"/{segment}"
        lines.append(f'  g{gi}["{mlabel(label, 28)}"]')
        lines.append(f"  api --> g{gi}")
        for ri, route in enumerate(items[:5]):
            lines.append(f'  g{gi}r{ri}["{route["method"]} {mlabel(route["path"], 36)}"]')
            lines.append(f"  g{gi} --> g{gi}r{ri}")
        if len(items) > 5:
            lines.append(f'  g{gi}m["+{len(items) - 5}"]')
            lines.append(f"  g{gi} --> g{gi}m")
    if len(groups) > 10:
        lines.append(f'  more["+{len(groups) - 10} groups"]')
        lines.append("  api --> more")
    return "\n".join(lines) + "\n"


def context_mermaid(public, integrations, database, services, repo, lang):
    """System context: who calls the project on the left, what it depends on on the right."""
    fr = lang == "fr"
    callers = []
    if public["routes"]:
        callers.append("Client HTTP" if fr else "HTTP client")
    if public["mcp"]:
        callers.append("Client MCP" if fr else "MCP client")
    if public["cli"] or any(e["kind"] == "console script" for e in public["entry_points"]):
        callers.append("Utilisateur en ligne de commande" if fr else "Command-line user")
    i = 1 if fr else 0
    deps = [(s["label"][i], "ext") for s in integrations["services"][:7]]
    deps += [(e["label"][i], "db") for e in database["engines"][:4]]
    deps += [(h["host"], "ext") for h in integrations["hosts"][:4] if not any(h["host"].split(".")[-2] in d[0].lower() for d in deps)]
    if not deps or not (callers or len(deps) > 1):
        return None
    lines = ["flowchart LR", f'  sys["{mlabel(repo, 32)}"]']
    for index, caller in enumerate(callers or ["Utilisateur" if fr else "User"]):
        lines += [f'  c{index}(["{caller}"])', f"  c{index} --> sys"]
    for index, (name, kind) in enumerate(deps[:12]):
        shape = f'[("{mlabel(name, 30)}")]' if kind == "db" else f'["{mlabel(name, 30)}"]'
        lines += [f"  d{index}{shape}", f"  sys --> d{index}"]
    if services["hosting"]:
        host = services["hosting"][0]["label"][i]
        lines += [f'  h{{{{"{mlabel(host, 30)}"}}}}', "  h -.- sys"]
    return "\n".join(lines) + "\n"


def build_private(analysis, texts):
    counts = Counter()
    examples = []
    rules = [
        (".py", re.compile(r"^\s*(?:async\s+)?def\s+(_[A-Za-z]\w*)\s*\(", re.MULTILINE), "underscore helper", "Assistant préfixé _"),
        ((".ts", ".tsx"), re.compile(r"^\s*(?:private|protected)\s+(?:readonly\s+|static\s+|async\s+)*(\w+)\s*[(:=]", re.MULTILINE), "private member", "Membre privé"),
        ((".js", ".ts", ".mjs"), re.compile(r"^\s*#(\w+)\s*[(=]", re.MULTILINE), "private class field", "Champ privé de classe"),
        (".rs", re.compile(r"^\s*pub\((?:crate|super)\)\s+fn\s+(\w+)", re.MULTILINE), "crate-visible function", "Fonction visible dans la crate"),
        (".rs", re.compile(r"^(?:\s{0,4})fn\s+(\w+)", re.MULTILINE), "module-private function", "Fonction privée au module"),
        ((".cs", ".java", ".kt", ".php"), re.compile(r"^\s*(?:private|internal|protected)\s+(?:static\s+|async\s+|override\s+|final\s+|suspend\s+|fun\s+)*(?:[\w<>\[\],?]+\s+)?(\w+)\s*\(", re.MULTILINE), "private / internal method", "Méthode privée ou interne"),
        ((".c", ".cpp", ".cc"), re.compile(r"^static\s+(?:inline\s+)?[\w\s\*]+?\b(\w+)\s*\([^;]*$", re.MULTILINE), "static (file-local) function", "Fonction static (locale au fichier)"),
        ((".cpp", ".cc", ".hpp"), re.compile(r"^\s*namespace\s*\{", re.MULTILINE), "anonymous namespace", "Espace de noms anonyme"),
    ]
    for path, text in texts.items():
        if is_test(path):
            continue
        for suffix, pattern, en, fr in rules:
            suffixes = suffix if isinstance(suffix, tuple) else (suffix,)
            if not path.endswith(suffixes):
                continue
            for match in pattern.finditer(text):
                counts[en] += 1
                if len([e for e in examples if e["kind"][0] == en]) < 3:
                    name = match.group(1) if match.groups() else "namespace { }"
                    examples.append({"kind": [en, fr], "name": name, **evidence(analysis, path, line_of(text, match.start()))})
    labels = {en: [en, fr] for _, _, en, fr in rules}
    internal_dirs = sorted({str(PurePosixPath(p).parent) for p in texts if re.search(r"(?:^|/)(?:internal|private|_internal|detail|impl)/", p)})[:6]
    private_modules = sorted({p for p in texts if re.match(r"_[a-z]\w*\.py$", PurePosixPath(p).name) and PurePosixPath(p).name != "__init__.py"})[:8]
    return {
        "counts": [{"label": labels[k], "count": v} for k, v in counts.most_common()],
        "examples": examples[:14],
        "internal_dirs": [{"path": d, "url": analysis["tree_url"] + "/" + quote(d)} for d in internal_dirs],
        "private_modules": [evidence(analysis, p) for p in private_modules],
    }


def workflow_jobs(text):
    """Jobs, their `needs` and step labels from a GitHub Actions file, read line by line."""
    jobs, current, in_jobs = [], None, False
    for raw in text.splitlines():
        if re.match(r"^jobs:\s*$", raw):
            in_jobs = True
            continue
        if not in_jobs:
            continue
        if re.match(r"^\S", raw):
            break
        job = re.match(r"^  ([\w-]+):\s*$", raw)
        if job:
            current = {"name": job[1], "needs": [], "steps": []}
            jobs.append(current)
            continue
        if current is None:
            continue
        needs = re.match(r"^    needs:\s*\[?([^\]#]+)\]?", raw)
        if needs:
            current["needs"] = [n.strip(" '\"") for n in needs[1].split(",") if n.strip(" '\"")]
        title = re.match(r"^    name:\s*['\"]?(.+?)['\"]?\s*$", raw)
        if title:
            current["title"] = without_expressions(title[1]) or current["name"]
        step = re.match(r"^\s+- (name|uses|run):\s*['\"]?(.+?)['\"]?\s*$", raw)
        if step and len(current["steps"]) < 10:
            label = step[2]
            if step[1] == "uses":
                label = label.split("@")[0]
            elif step[1] == "run":
                label = label.lstrip("|> ").strip() or "run"
            label = without_expressions(label)
            if label:
                current["steps"].append(label[:48])
    return jobs[:6]


def without_expressions(text):
    # GitHub expressions such as ${{ matrix.suffix }} only make sense inside the workflow.
    return re.sub(r"\s*\(?[^()]*\$\{\{.*?\}\}[^()]*\)?", "", text).strip(" -:")


def build_tests(analysis, texts, paths):
    test_paths = [p for p in paths if is_test(p) and is_source(p)]
    source_paths = [p for p in paths if is_source(p) and not is_test(p) and layer_of(p) not in {"hosting"}]
    frameworks = []
    for pattern, name in TEST_FRAMEWORKS:
        for path in test_paths + [p for p in texts if not is_test(p)]:
            text = texts.get(path)
            if text and re.search(pattern, text, re.MULTILINE) and (is_test(path) or name in {"cargo test", "doctest"}):
                frameworks.append({"name": name, **evidence(analysis, path)})
                break
    for name, pattern in (("pytest", r"(?:^|/)(?:pytest\.ini|conftest\.py)$"), ("Vitest", r"vitest\.config\."), ("Jest / Testing Library", r"jest\.config\."), ("Playwright", r"playwright\.config\."), ("PHPUnit", r"phpunit\.xml"), ("CTest", r"(?:^|/)CTestTestfile|enable_testing")):
        if not any(f["name"] == name for f in frameworks):
            hit = next((p for p in paths if re.search(pattern, p)), None)
            if hit:
                frameworks.append({"name": name, **evidence(analysis, hit)})
    cases = sum(len(TEST_CASES.findall(texts[p])) for p in test_paths if p in texts)
    cases += sum(len(re.findall(r"#\[(?:tokio::)?test\]", t)) for p, t in texts.items() if p.endswith(".rs") and not is_test(p))
    dirs = Counter(str(PurePosixPath(p).parent) for p in test_paths)
    workflows = []
    for path, text in texts.items():
        if WORKFLOW.match(path):
            runs = re.findall(r"(pytest|npm (?:run )?test|pnpm (?:run )?test|yarn test|vitest|jest|cargo test|dotnet test|ctest|go test|phpunit|php artisan test|gradlew? test|mvn test|rspec|playwright test|ruff|eslint|mypy|tsc --noEmit|clippy|codeql)", text)
            if runs:
                name = re.search(r"^name:\s*['\"]?(.+?)['\"]?\s*$", text, re.MULTILINE)
                workflows.append({"name": name[1] if name else PurePosixPath(path).stem, "runs": list(dict.fromkeys(runs))[:6], "jobs": workflow_jobs(text), **evidence(analysis, path)})
    workflows.sort(key=lambda w: -len(w["runs"]))
    coverage = [p for p in paths if re.search(r"(?:^|/)(?:codecov\.ya?ml|\.coveragerc|\.nycrc|jest\.config\.|vitest\.config\.)", p)]
    kinds = Counter(test_kind(p, texts.get(p, "")) for p in test_paths)
    tools = []
    for pattern, name in COVERAGE_TOOLS:
        hit = next(((p, t) for p, t in texts.items() if re.search(pattern, t)), None)
        if hit:
            tools.append({"name": name, **evidence(analysis, hit[0], line_of(hit[1], re.search(pattern, hit[1]).start()))})
    return {
        "files": len(test_paths),
        "source_files": len(source_paths),
        "cases": cases,
        "kinds": [{"key": k, "label": TEST_KINDS[k], "files": n} for k, n in kinds.most_common()],
        "frameworks": frameworks[:8],
        "directories": [{"path": d, "files": n, "url": analysis["tree_url"] + "/" + quote(d)} for d, n in dirs.most_common(6)],
        "workflows": workflows[:8],
        "coverage_config": [evidence(analysis, p) for p in coverage[:3]],
        "coverage_tools": tools[:5],
    }


TEST_KINDS = {
    "unit": L("Unit", "Unitaires"),
    "integration": L("Integration", "Intégration"),
    "e2e": L("End-to-end", "De bout en bout"),
    "benchmark": L("Benchmark", "Performance"),
}
COVERAGE_TOOLS = [
    (r"pytest-cov|--cov\b|coverage run|coverage\.py", "coverage.py"),
    (r"\bc8\b|\bnyc\b|--coverage\b|coverageThreshold|@vitest/coverage", "JS coverage (c8/nyc/vitest)"),
    (r"jacoco", "JaCoCo"),
    (r"coverlet|XPlat Code Coverage", "Coverlet"),
    (r"codecov/codecov-action|codecov\.io", "Codecov"),
    (r"cargo[- ]tarpaulin|cargo llvm-cov|grcov", "Rust coverage"),
    (r"gcovr|lcov --capture|geninfo|-fprofile-arcs", "gcov/lcov"),
]


def test_kind(path, text):
    """Classify a test file by its path, then by the tools it imports."""
    lower = path.lower()
    if re.search(r"bench", lower):
        return "benchmark"
    if re.search(r"(?:^|/)(?:e2e|end-to-end|playwright|cypress|selenium)(?:/|[._-])", lower) or re.search(r"@playwright/test|cypress|selenium|webdriver|page\.goto\(", text):
        return "e2e"
    if re.search(r"integration|(?:^|/)it(?:/|[._-])|functional|(?:^|/)api[_-]?tests?/", lower) or re.search(r"TestClient\(|testcontainers|supertest|WebApplicationFactory|@SpringBootTest|RefreshDatabase", text):
        return "integration"
    return "unit"


MONITORING = [
    (r"^\s*import logging|getLogger\(|\bloguru\b|structlog", "Python logging", "logging"),
    (r"\bwinston\b|\bpino\b|\bbunyan\b|log4js", "Node logging", "logging"),
    (r"\bSerilog\b|\bNLog\b|ILogger<", ".NET logging", "logging"),
    (r"org\.slf4j|log4j|java\.util\.logging|Timber\.|android\.util\.Log", "JVM / Android logging", "logging"),
    (r"\bspdlog\b|\bglog\b|PLOG_|easylogging", "C++ logging", "logging"),
    (r"\btracing::|env_logger|\blog::(?:info|warn|error)!", "Rust logging", "logging"),
    (r"sentry_sdk|@sentry/|SentrySdk|using Sentry|sentry-native", "Sentry", "errors"),
    (r"\bbugsnag\b|\brollbar\b", "Error reporting service", "errors"),
    (r"prometheus_client|prom-client|micrometer|\bstatsd\b|/metrics[\"']", "Metrics endpoint", "metrics"),
    (r"opentelemetry|\bjaeger\b|\bzipkin\b", "Distributed tracing", "tracing"),
    (r"grafana", "Grafana dashboards", "dashboards"),
    (r"uptime-kuma|uptimerobot|healthchecks\.io", "Uptime monitoring", "uptime"),
    (r"static\.cloudflareinsights\.com|googletagmanager|gtag\(|plausible\.io|umami", "Web analytics", "analytics"),
    (r"alertmanager|pagerduty|opsgenie", "Alerting", "alerting"),
]


def build_monitoring(analysis, texts, routes):
    """Logging, error tracking, metrics, tracing, health checks and dashboards found in the code."""
    signals = scan_patterns(analysis, {p: t for p, t in texts.items() if not is_test(p) and not p.lower().endswith(".md")}, MONITORING)
    health = [r for r in routes if re.search(r"(?i)(?:^|/)(?:health|healthz|ready|readyz|live|livez|status|ping|metrics)(?:/|$)", r["path"])]
    checks = []
    for path, text in texts.items():
        name = PurePosixPath(path).name.lower()
        if name.startswith("dockerfile") or re.search(r"compose[\w.-]*\.ya?ml$", name):
            for match in re.finditer(r"^\s*(HEALTHCHECK\b.*|healthcheck:)", text, re.MULTILINE | re.IGNORECASE):
                checks.append({"label": "Docker HEALTHCHECK" if match[1].upper().startswith("HEALTHCHECK") else "Compose healthcheck", **evidence(analysis, path, line_of(text, match.start()))})
    return {"signals": signals, "health_routes": health[:8], "health_checks": checks[:6]}


DEPLOY_STEPS = re.compile(r"(?i)deploy|publish|release|push|upload|pages|vercel|wrangler|helm|kubectl|terraform|gh-pages|pypi|npm publish|nuget push|docker/build-push")
PUBLISH_TARGETS = [
    (r"actions/deploy-pages|peaceiris/actions-gh-pages|gh-pages", "GitHub Pages", "GitHub Pages"),
    (r"docker/build-push-action|docker push|ghcr\.io", "Container registry", "Registre de conteneurs"),
    (r"pypa/gh-action-pypi-publish|twine upload|uv publish|poetry publish", "PyPI", "PyPI"),
    (r"npm publish|JS-DevTools/npm-publish", "npm", "npm"),
    (r"nuget push|dotnet nuget push", "NuGet", "NuGet"),
    (r"vercel(?:-action| deploy|/action| --prod| build| pull)|amondnet/vercel|VERCEL_TOKEN", "Vercel", "Vercel"),
    (r"wrangler (?:deploy|publish)|cloudflare/wrangler-action|pages deploy", "Cloudflare", "Cloudflare"),
    (r"softprops/action-gh-release|gh release create|goreleaser|release-please|semantic-release", "GitHub Releases", "Versions GitHub"),
    (r"helm upgrade|kubectl apply|azure/k8s-deploy", "Kubernetes", "Kubernetes"),
    (r"terraform apply", "Terraform", "Terraform"),
]


def workflow_triggers(text):
    block = re.search(r"^on:\s*(.*)$((?:\n[ \t]+.*)*)", text, re.MULTILINE)
    if not block:
        return []
    inline = re.findall(r"[\w-]+", block[1]) if block[1].strip() else []
    nested = re.findall(r"^  ([\w-]+):", block[2], re.MULTILINE)
    return list(dict.fromkeys(inline + nested))[:6]


def build_deployment(analysis, texts, services):
    """Where the code runs and how it gets there: hosting files, images, deploy pipelines, publish targets."""
    pipelines, targets = [], {}
    for path, text in sorted(texts.items()):
        if not WORKFLOW.match(path):
            continue
        for pattern, en, fr in PUBLISH_TARGETS:
            match = re.search(pattern, text)
            if match and en not in targets:
                targets[en] = {"label": [en, fr], **evidence(analysis, path, line_of(text, match.start()))}
        jobs = workflow_jobs(text)
        steps = [s for job in jobs for s in job["steps"] if DEPLOY_STEPS.search(s)]
        if steps:
            name = re.search(r"^name:\s*['\"]?(.+?)['\"]?\s*$", text, re.MULTILINE)
            environments = re.findall(r"^\s+environment:\s*(?:\n\s+name:\s*)?['\"]?([\w-]+)", text, re.MULTILINE)
            pipelines.append({
                "name": name[1] if name else PurePosixPath(path).stem,
                "triggers": workflow_triggers(text),
                "environments": list(dict.fromkeys(environments))[:4],
                "steps": list(dict.fromkeys(steps))[:6],
                **evidence(analysis, path),
            })
    return {
        "hosting": services["hosting"],
        "containers": services["containers"],
        "base_images": services["base_images"],
        "pipelines": pipelines[:5],
        "targets": list(targets.values()),
    }


def build_security(analysis, texts, paths):
    controls = scan_patterns(analysis, {p: t for p, t in texts.items() if not is_test(p) and not p.lower().endswith(".md")}, SECURITY)
    env = Counter()
    first = {}
    for path, text in texts.items():
        if is_test(path) or not is_source(path):
            continue
        for match in ENV_VARS.finditer(text):
            name = next(g for g in match.groups() if g)
            env[name] += 1
            first.setdefault(name, evidence(analysis, path, line_of(text, match.start())))
    secret_like = re.compile(r"KEY|TOKEN|SECRET|PASSWORD|PASS|CREDENTIAL|AUTH|DSN")
    variables = sorted(env, key=lambda n: (not secret_like.search(n), -env[n], n))[:16]
    review = []
    for pattern, label, suffix in REVIEW:
        suffixes = suffix if isinstance(suffix, tuple) else (suffix,)
        hits = [(p, t) for p, t in texts.items() if p.endswith(suffixes) and not is_test(p) and re.search(pattern, t)]
        if hits:
            path, text = hits[0]
            review.append({"label": L(label, NAME_FR.get(label)), "files": len(hits), **evidence(analysis, path, line_of(text, re.search(pattern, text).start()))})
    supply = []
    for pattern, en, fr in (
        (r"(?:^|/)\.github/dependabot\.ya?ml$", "Dependabot updates", "Mises à jour Dependabot"),
        (r"(?:^|/)renovate\.json5?$|(?:^|/)\.renovaterc", "Renovate updates", "Mises à jour Renovate"),
        (r"(?:^|/)SECURITY\.md$", "Security policy", "Politique de sécurité"),
        (r"codeql", "CodeQL scanning", "Analyse CodeQL"),
        (r"(?:^|/)(?:uv\.lock|poetry\.lock|package-lock\.json|pnpm-lock\.yaml|yarn\.lock|Cargo\.lock|composer\.lock|Gemfile\.lock|packages\.lock\.json|go\.sum)$", "Lockfile (pinned dependencies)", "Fichier de verrouillage (dépendances figées)"),
        (r"(?:^|/)\.pre-commit-config\.ya?ml$", "pre-commit hooks", "Hooks pre-commit"),
        (r"(?:^|/)\.gitleaks\.toml$|gitleaks|trufflehog", "Secret scanning", "Détection de secrets"),
        (r"(?:^|/)\.env\.example$|(?:^|/)\.env\.sample$", "Example environment file (no values)", "Exemple de fichier d’environnement (sans valeurs)"),
    ):
        hits = [p for p in paths if re.search(pattern, p, re.I)]
        if not hits and "codeql" in pattern:
            hits = [p for p, t in texts.items() if WORKFLOW.match(p) and "codeql" in t.lower()]
        if hits:
            supply.append({"label": [en, fr], **evidence(analysis, hits[0])})
    return {
        "controls": controls,
        "env_vars": [{"name": n, "uses": env[n], "secret": bool(secret_like.search(n)), **first[n]} for n in variables],
        "env_total": len(env),
        "supply_chain": supply,
        "review": review,
    }


def requirement_name(spec):
    match = re.match(r"\s*([A-Za-z0-9][A-Za-z0-9._\-]*)(\[[^\]]*\])?\s*(.*)", spec)
    if not match:
        return None
    version = re.sub(r";.*$", "", match[3]).strip()
    return {"name": match[1], "version": version[:24]}


def build_stack(analysis, texts):
    manifests = []

    def add(path, ecosystem, runtime, dev=(), toolchain=None):
        runtime = [d for d in runtime if d and d.get("name")]
        dev = [d for d in dev if d and d.get("name")]
        if runtime or dev or toolchain:
            manifests.append({"ecosystem": ecosystem, "runtime": runtime[:24], "runtime_total": len(runtime), "dev": dev[:16], "dev_total": len(dev), "toolchain": toolchain or [], **evidence(analysis, path)})

    # Root manifests first: they describe the project, nested ones its examples or sub-packages.
    for path, text in sorted(texts.items(), key=lambda kv: (len(PurePosixPath(kv[0]).parts), kv[0])):
        name = PurePosixPath(path).name
        if is_test(path) and name not in {"package.json"}:
            continue
        try:
            if name == "pyproject.toml":
                data = tomllib.loads(text)
                project = data.get("project", {})
                poetry = data.get("tool", {}).get("poetry", {})
                runtime = [requirement_name(s) for s in project.get("dependencies", [])]
                runtime += [{"name": k, "version": v if isinstance(v, str) else ""} for k, v in poetry.get("dependencies", {}).items() if k != "python"]
                dev = [requirement_name(s) for group in project.get("optional-dependencies", {}).values() for s in group]
                dev += [requirement_name(s) for group in data.get("dependency-groups", {}).values() for s in group if isinstance(s, str)]
                tool = []
                if project.get("requires-python"):
                    tool.append(f"Python {project['requires-python']}")
                add(path, "Python", runtime, dev, tool)
            elif re.fullmatch(r"requirements[\w.\-]*\.txt", name):
                deps = [requirement_name(l) for l in text.splitlines() if l.strip() and not l.lstrip().startswith(("#", "-"))]
                add(path, "Python", [] if "dev" in name else deps, deps if "dev" in name else [])
            elif name == "package.json":
                data = json.loads(text)
                if not isinstance(data, dict):
                    continue
                as_list = lambda d: [{"name": k, "version": str(v)[:24]} for k, v in (d or {}).items()] if isinstance(d, dict) else []
                engines = [f"{k} {v}" for k, v in (data.get("engines") or {}).items()] if isinstance(data.get("engines"), dict) else []
                add(path, "Node.js", as_list(data.get("dependencies")), as_list(data.get("devDependencies")), engines)
            elif name == "Cargo.toml":
                data = tomllib.loads(text)
                pick = lambda d: [{"name": k, "version": v if isinstance(v, str) else str(v.get("version", "")) if isinstance(v, dict) else ""} for k, v in (d or {}).items()]
                deps = pick(data.get("dependencies")) + pick(data.get("workspace", {}).get("dependencies"))
                edition = data.get("package", {}).get("edition")
                add(path, "Rust", deps, pick(data.get("dev-dependencies")), [f"Rust edition {edition}"] if edition else [])
            elif name == "composer.json":
                data = json.loads(text)
                as_list = lambda d: [{"name": k, "version": str(v)} for k, v in (d or {}).items() if k != "php"]
                php = (data.get("require") or {}).get("php")
                add(path, "PHP", as_list(data.get("require")), as_list(data.get("require-dev")), [f"PHP {php}"] if php else [])
            elif name == "Gemfile":
                gems = [{"name": m[1], "version": ""} for m in re.finditer(r"^\s*gem\s+['\"]([\w\-]+)['\"]", text, re.MULTILINE)]
                ruby = re.search(r"^ruby\s+['\"]([^'\"]+)", text, re.MULTILINE)
                add(path, "Ruby", gems, [], [f"Ruby {ruby[1]}"] if ruby else [])
            elif name in {"build.gradle", "build.gradle.kts"}:
                deps = [{"name": m[2], "version": ""} for m in re.finditer(r"^\s*(implementation|api|kapt|ksp|compileOnly|runtimeOnly)\s*\(?\s*['\"]([^'\"]+)['\"]", text, re.MULTILINE)]
                dev = [{"name": m[2], "version": ""} for m in re.finditer(r"^\s*(testImplementation|androidTestImplementation)\s*\(?\s*['\"]([^'\"]+)['\"]", text, re.MULTILINE)]
                deps += [{"name": m[1], "version": ""} for m in re.finditer(r"implementation\s*\(\s*libs\.([\w.]+)\)", text)]
                tool = [f"{k} {v}" for k, v in re.findall(r"(compileSdk|minSdk|targetSdk|jvmTarget)\s*=?\s*['\"]?(\w+)", text)][:4]
                add(path, "JVM (Gradle)", deps, dev, tool)
            elif name == "pom.xml":
                deps = [{"name": f"{m[1]}:{m[2]}", "version": ""} for m in re.finditer(r"<dependency>\s*<groupId>([^<]+)</groupId>\s*<artifactId>([^<]+)</artifactId>", text)]
                java = re.search(r"<java\.version>([^<]+)<", text)
                add(path, "JVM (Maven)", deps, [], [f"Java {java[1]}"] if java else [])
            elif name.endswith((".csproj", ".fsproj")):
                deps = [{"name": m[1], "version": m[2] or ""} for m in re.finditer(r"<PackageReference\s+Include=\"([^\"]+)\"(?:\s+Version=\"([^\"]+)\")?", text)]
                tfm = re.findall(r"<TargetFrameworks?>([^<]+)<", text)
                add(path, ".NET", deps, [], [f"Target {t}" for t in tfm])
            elif name == "go.mod":
                deps = [{"name": m[1], "version": m[2]} for m in re.finditer(r"^\s*([\w.\-/]+\.[\w.\-/]+)\s+(v[\w.\-+]+)", text, re.MULTILINE)]
                go = re.search(r"^go\s+([\d.]+)", text, re.MULTILINE)
                add(path, "Go", deps, [], [f"Go {go[1]}"] if go else [])
            elif name == "CMakeLists.txt" and len(PurePosixPath(path).parts) <= 2:
                deps = [{"name": m, "version": ""} for m in re.findall(r"find_package\(\s*(\w+)", text)]
                deps += [{"name": m, "version": "FetchContent"} for m in re.findall(r"FetchContent_Declare\(\s*(\w+)", text)]
                std = re.findall(r"CMAKE_CXX_STANDARD\s+(\d+)|cxx_std_(\d+)", text)
                tool = [f"C++{a or b}" for a, b in std[:1]]
                cm = re.search(r"cmake_minimum_required\s*\(\s*VERSION\s+([\d.]+)", text, re.I)
                if cm:
                    tool.append(f"CMake ≥ {cm[1]}")
                add(path, "C/C++ (CMake)", list({d["name"]: d for d in deps}.values()), [], tool)
            elif name == "platformio.ini":
                tool = [f"{k} {v.strip()}" for k, v in re.findall(r"^(platform|board|framework)\s*=\s*(.+)$", text, re.MULTILINE)][:4]
                libs = re.search(r"lib_deps\s*=\s*((?:\n\s+.+)+|.+)", text)
                deps = [{"name": l.strip(), "version": ""} for l in (libs[1].splitlines() if libs else []) if l.strip()]
                add(path, "Embedded (PlatformIO)", deps, [], tool)
            elif name == "Makefile" and len(PurePosixPath(path).parts) == 1:
                libs = re.search(r"^LIBS\s*[:+]?=\s*(.+)$", text, re.MULTILINE)
                deps = [{"name": l, "version": ""} for l in (libs[1].split() if libs else []) if l.startswith("-l")]
                devkit = re.search(r"DEVKIT(?:PRO|ARM)|devkitA64|libnx|libctru", text)
                add(path, "Native (Make)", deps, [], [devkit[0]] if devkit else [])
        except (ValueError, tomllib.TOMLDecodeError, AttributeError, TypeError):
            continue
    # Languages and Docker base images already appear in the language panel and Services section.
    # Manifests that declare exactly the same packages (a library and its sample, say) are shown once.
    manifests = unique(manifests, lambda m: (m["ecosystem"], tuple(d["name"] for d in m["runtime"]), tuple(d["name"] for d in m["dev"])))
    return {"manifests": manifests[:10], "manifest_total": len(manifests)}


def dossier(note, offline):
    analysis = load_analysis(note["repo"])
    inputs = docs.load(docs.CACHE / note["slug"] / "inputs.json")
    if not analysis or not inputs:
        return None
    tree = inputs["tree"]["tree"]
    analysis["_tree"] = tree
    paths = [e["path"] for e in tree if e.get("type") == "blob"]
    texts = load_texts(note["repo"], inputs, offline)
    types = analysis.get("types", [])
    layers = build_layers(analysis, paths, types)
    entities = build_entities(analysis, texts, types)
    public = build_public(analysis, texts, types, analysis.get("manifests", []))
    services = build_services(analysis, texts, types, paths)
    integrations = build_integrations(analysis, texts, note["repo"])
    database = build_database(analysis, texts, paths)
    listed = {e["name"] for e in entities["items"]} | {i["name"] for g in services["roles"] for i in g["items"]}
    result = {
        "repo": note["repo"],
        "commit": analysis["commit"],
        "tree_url": analysis["tree_url"],
        "files_scanned": len(texts),
        "layers": layers,
        "layers_mermaid": [layers_mermaid(layers, "en"), layers_mermaid(layers, "fr")] if layers else None,
        "modules": build_modules(analysis, paths, types),
        "flow": parse_gitdiagram(analysis, paths),
        "public": public,
        "private": build_private(analysis, texts),
        "services": services,
        "logic": build_logic(analysis, texts, types, listed),
        "entities": entities,
        "database": database,
        "integrations": integrations,
        "context_mermaid": [
            context_mermaid(public, integrations, database, services, note["repo"], lang) for lang in ("en", "fr")
        ],
        "stack": build_stack(analysis, texts),
        "security": build_security(analysis, texts, paths),
        "tests": build_tests(analysis, texts, paths),
        "monitoring": build_monitoring(analysis, texts, public["routes"]),
        "deployment": build_deployment(analysis, texts, services),
    }
    return result


_ANALYSIS = None


def load_analysis(repo):
    global _ANALYSIS
    if _ANALYSIS is None:
        _ANALYSIS = docs.load(docs.DATA, {"repositories": {}})["repositories"]
    return _ANALYSIS.get(repo)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", action="append", help="Repository name; repeat to select several")
    parser.add_argument("--offline", action="store_true", help="Use cached verified blobs only")
    args = parser.parse_args()
    notes = docs.load(ROOT / "hugo/data/repository_notes.json")["notes"]
    if args.repo and set(args.repo) - {n["repo"] for n in notes}:
        parser.error("Unknown repository; only the public site inventory is accepted")
    output = docs.load(OUT, {"schema_version": 1, "repositories": {}})
    for note in notes:
        if args.repo and note["repo"] not in args.repo:
            continue
        value = dossier(note, args.offline)
        if value is None:
            print(f"{note['repo']}: no cached snapshot, skipped", flush=True)
            continue
        output["repositories"][note["repo"]] = value
        print(
            f"{note['repo']}: {value['files_scanned']} files, {len(value['layers'])} layers, "
            f"{value['public']['route_total']} routes, {value['entities']['total']} entities, "
            f"{value['tests']['files']} test files",
            flush=True,
        )
    output["repositories"] = dict(sorted(output["repositories"].items(), key=lambda kv: kv[0].lower()))
    docs.save(OUT, output)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())

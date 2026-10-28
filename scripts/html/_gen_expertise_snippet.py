"""One-shot helper: print EN/FR Technical Expertise markup (not imported by CI)."""
from __future__ import annotations

# Local copies made by scripts/build/fetch_cv_icons.py; add new slugs there first.
ICON = "images/tech-icons/{slug}.svg"

CERT_AWS = {
    "url": "https://www.credly.com/badges/b57717b2-640e-459b-be04-6de7062b1564",
    "title_en": "AWS Certified Cloud Practitioner",
    "title_fr": "AWS Certified Cloud Practitioner",
    "icon": ICON.format(slug="amazonwebservices"),
}
CERT_MCP = {
    "url": "https://credentials.verify.cvpartners.com/?credentialId=394c8a269dbc0a77cba976cfb23518c2",
    "title_en": "Claude Academy: Introduction to Model Context Protocol",
    "title_fr": "Claude Academy : Introduction to Model Context Protocol",
    "icon": ICON.format(slug="anthropic"),
}
# Prefer linking MCP cert to a known credential id string on the page; Claude Academy
# may not resolve via that verify URL — use credential id text match on Certifications.
CERT_MCP["url"] = "#certifications"


def pill(name: str, slug: str, url: str, cert: dict | None = None) -> str:
    icon = ICON.format(slug=slug)
    cert_html = ""
    if cert:
        title = cert["title_en"]  # patched per locale below via placeholder
        cert_html = (
            f'<a class="expertise-cert" href="{cert["url"]}" '
            f'target="_blank" rel="noopener noreferrer" '
            f'title="__CERT_TITLE__" aria-label="__CERT_TITLE__">'
            f'<img src="{cert["icon"]}" alt="" width="14" height="14" '
            f'loading="lazy" decoding="async"></a>'
        ).replace("__CERT_TITLE__", "{cert_title}")
        # Store titles on cert for locale render
    main = (
        f'<li class="expertise-pill" data-skill="{name}">'
        f'<a class="expertise-pill-main" href="{url}" target="_blank" rel="noopener noreferrer">'
        f'<img class="expertise-pill-icon" src="{icon}" alt="" width="16" height="16" '
        f'loading="lazy" decoding="async">'
        f"<span>{name}</span></a>"
    )
    if cert:
        t_en = cert["title_en"]
        t_fr = cert["title_fr"]
        # locale-specific emission handled in render_pill
        return (name, slug, url, cert)
    return (name, slug, url, None)


# Actually simplify: emit_pill(lang)


def emit_pill(lang: str, name: str, slug: str, url: str, cert: dict | None = None) -> str:
    icon = ICON.format(slug=slug)
    parts = [
        f'<li class="expertise-pill" data-skill="{name}">',
        f'<a class="expertise-pill-main" href="{url}" target="_blank" rel="noopener noreferrer">',
        f'<img class="expertise-pill-icon" src="{icon}" alt="" width="16" height="16" loading="lazy" decoding="async">',
        f"<span>{name}</span></a>",
    ]
    if cert:
        title = cert["title_fr"] if lang == "fr" else cert["title_en"]
        href = cert["url"]
        external = not href.startswith("#")
        rel = ' target="_blank" rel="noopener noreferrer"' if external else ""
        parts.append(
            f'<a class="expertise-cert" href="{href}"{rel} '
            f'title="{title}" aria-label="{title}">'
            f'<img src="{cert["icon"]}" alt="" width="14" height="14" loading="lazy" decoding="async"></a>'
        )
    parts.append("</li>")
    return "".join(parts)


def pills(lang: str, items: list[tuple]) -> str:
    out = ['<ul class="expertise-pills" role="list">']
    for item in items:
        if len(item) == 4:
            name, slug, url, cert = item
        else:
            name, slug, url = item
            cert = None
        out.append(emit_pill(lang, name, slug, url, cert))
    out.append("</ul>")
    return "\n".join(out)


DOMAINS = [
    ("languages-formats", "Languages & Formats", "Langages et formats"),
    ("application", "Applications", "Applicatif"),
    ("data-analytics", "Data & Analytics", "Données et analytique"),
    ("platform-devops", "Platform & DevOps", "Plateforme et DevOps"),
    ("quality-tests", "Quality & Testing", "Qualité et tests"),
    ("graphics-3d", "Graphics & Simulation", "Graphismes et simulation"),
]

# domain -> list of (sub_id, en, fr, pills)
CONTENT = {
    "languages-formats": [
        (
            "languages",
            "Languages",
            "Langages",
            [
                ("Python", "python", "https://www.python.org/"),
                ("Java", "openjdk", "https://dev.java/"),
                ("Kotlin", "kotlin", "https://kotlinlang.org/"),
                ("C++", "cplusplus", "https://isocpp.org/"),
                ("C#", "csharp", "https://learn.microsoft.com/dotnet/csharp/"),
                ("TypeScript", "typescript", "https://www.typescriptlang.org/"),
                ("JavaScript", "javascript", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"),
            ],
        ),
        (
            "formats",
            "Formats & Documentation",
            "Formats et documentation",
            [
                ("JSON", "json", "https://www.json.org/"),
                ("XML", "xml", "https://www.w3.org/XML/"),
                ("Markdown", "markdown", "https://commonmark.org/"),
                ("Mermaid", "mermaid", "https://mermaid.js.org/"),
            ],
        ),
    ],
    "application": [
        (
            "frontend",
            "Frontend & UI",
            "Frontend et UI",
            [
                ("Angular", "angular", "https://angular.dev/"),
                ("React", "react", "https://react.dev/"),
                ("Vue.js", "vuedotjs", "https://vuejs.org/"),
            ],
        ),
        (
            "backend",
            "Backend & APIs",
            "Backend et API",
            [
                ("Spring Boot", "springboot", "https://spring.io/projects/spring-boot"),
                ("FastAPI", "fastapi", "https://fastapi.tiangolo.com/"),
                ("Django", "django", "https://www.djangoproject.com/"),
                (".NET", "dotnet", "https://dotnet.microsoft.com/"),
                ("Flask", "flask", "https://flask.palletsprojects.com/"),
                ("GraphQL", "graphql", "https://graphql.org/"),
                ("MCP", "modelcontextprotocol", "https://modelcontextprotocol.io/", CERT_MCP),
            ],
        ),
        (
            "runtimes",
            "Web servers & runtimes",
            "Serveurs web et runtimes",
            [
                ("Android", "android", "https://developer.android.com/"),
            ],
        ),
    ],
    "data-analytics": [
        (
            "databases",
            "Databases",
            "Bases de données",
            [
                ("SQL", "postgresql", "https://www.iso.org/standard/76583.html"),
                ("PostgreSQL", "postgresql", "https://www.postgresql.org/"),
                ("MongoDB", "mongodb", "https://www.mongodb.com/"),
                ("Redis", "redis", "https://redis.io/"),
            ],
        ),
        (
            "connectors",
            "Connectors & messaging",
            "Connecteurs et messagerie",
            [
                ("Kafka", "apachekafka", "https://kafka.apache.org/"),
            ],
        ),
        (
            "ia-llm",
            "AI & LLM",
            "IA et LLM",
            [
                ("MCP", "modelcontextprotocol", "https://modelcontextprotocol.io/", CERT_MCP),
                ("Jupyter", "jupyter", "https://jupyter.org/"),
            ],
        ),
    ],
    "platform-devops": [
        (
            "cicd",
            "CI/CD & deployment",
            "CI/CD et déploiement",
            [
                ("Git", "git", "https://git-scm.com/"),
                ("GitLab CI/CD", "gitlab", "https://docs.gitlab.com/ee/ci/"),
                ("GitHub Actions", "githubactions", "https://docs.github.com/en/actions"),
                ("Azure DevOps", "azuredevops", "https://azure.microsoft.com/products/devops"),
            ],
        ),
        (
            "cloud",
            "Cloud & infrastructure",
            "Cloud et infrastructure",
            [
                ("Terraform", "terraform", "https://www.terraform.io/"),
                ("GCP", "googlecloud", "https://cloud.google.com/"),
                ("Azure", "microsoftazure", "https://azure.microsoft.com/"),
                ("AWS", "amazonaws", "https://aws.amazon.com/", CERT_AWS),
            ],
        ),
        (
            "containers",
            "Containers & systems",
            "Conteneurs et systèmes",
            [
                ("Docker", "docker", "https://www.docker.com/"),
                ("Kubernetes", "kubernetes", "https://kubernetes.io/"),
                ("Linux", "linux", "https://www.kernel.org/"),
            ],
        ),
        (
            "observability",
            "Observability",
            "Observabilité",
            [
                ("ELK", "elasticstack", "https://www.elastic.co/elastic-stack"),
                ("Grafana", "grafana", "https://grafana.com/"),
                ("Prometheus", "prometheus", "https://prometheus.io/"),
                ("Sentry", "sentry", "https://sentry.io/"),
            ],
        ),
        (
            "security-practice",
            "Identity, security & practice",
            "Identité, sécurité et pratiques",
            [
                ("Auth0", "auth0", "https://auth0.com/"),
                ("OWASP", "owasp", "https://owasp.org/"),
            ],
        ),
    ],
    "quality-tests": [
        (
            "quality",
            "Quality & tests",
            "Qualité et tests",
            [
                ("Playwright", "playwright", "https://playwright.dev/"),
                ("JUnit", "junit5", "https://junit.org/junit5/"),
                ("Selenium", "selenium", "https://www.selenium.dev/"),
            ],
        ),
    ],
    "graphics-3d": [
        (
            "realtime",
            "Real-time rendering",
            "Rendu temps réel",
            [
                ("OpenGL", "opengl", "https://www.opengl.org/"),
                ("GLSL", "opengl", "https://www.khronos.org/opengl/wiki/OpenGL_Shading_Language"),
                ("C++", "cplusplus", "https://isocpp.org/"),
            ],
        ),
        (
            "assets-compute",
            "Assets & compute",
            "Assets et calcul",
            [
                ("Blender", "blender", "https://www.blender.org/"),
                ("CUDA", "nvidia", "https://developer.nvidia.com/cuda-toolkit"),
                ("OpenCV", "opencv", "https://opencv.org/"),
            ],
        ),
    ],
}


def render(lang: str) -> str:
    fr = lang == "fr"
    title = "Expertise technique" if fr else "Technical Expertise"
    subtitle = (
        "Parcourir par domaine d'ingénierie"
        if fr
        else "Browse by engineering domain"
    )
    search_ph = "Rechercher une compétence…" if fr else "Search skills…"
    search_label = "Rechercher des compétences" if fr else "Search skills"
    empty = (
        "Aucune compétence ne correspond à cette recherche."
        if fr
        else "No skills match this search."
    )
    all_label = "Tout" if fr else "All"
    tech_word = "technologies"

    lines = [
        f'<div class="expertise" data-expertise data-expertise-lang="{lang}">',
        '<div class="expertise-header">',
        f'<div><p class="expertise-title">{title}</p>',
        f'<p class="expertise-subtitle">{subtitle}</p></div>',
        "</div>",
        f'<label class="visually-hidden" for="expertise-search-{lang}">{search_label}</label>',
        f'<input class="expertise-search" id="expertise-search-{lang}" type="search" '
        f'placeholder="{search_ph}" autocomplete="off" data-expertise-search>',
        '<div class="expertise-domains" role="tablist" '
        f'aria-label="{"Domaines" if fr else "Domains"}">',
    ]
    for i, (did, en, frl) in enumerate(DOMAINS):
        selected = "true" if i == 0 else "false"
        label = frl if fr else en
        lines.append(
            f'<button type="button" class="expertise-domain" role="tab" '
            f'id="expertise-tab-{lang}-{did}" data-domain="{did}" '
            f'aria-selected="{selected}" aria-controls="expertise-panel-{lang}-{did}">'
            f"{label}</button>"
        )
    lines.append("</div>")
    lines.append('<div class="expertise-workspace">')

    for di, (did, en, frl) in enumerate(DOMAINS):
        hidden = "" if di == 0 else " hidden"
        dlabel = frl if fr else en
        subs = CONTENT[did]
        n = sum(len(s[3]) for s in subs)
        count_label = (
            f"{n} technologie" + ("s" if n != 1 else "")
            if fr
            else f"{n} technolog" + ("ies" if n != 1 else "y")
        )
        lines.append(
            f'<div class="expertise-panel" id="expertise-panel-{lang}-{did}" '
            f'role="tabpanel" data-domain-panel="{did}" data-domain-label="{dlabel}" '
            f'aria-labelledby="expertise-tab-{lang}-{did}"{hidden}>'
        )
        lines.append('<div class="expertise-body">')
        lines.append('<div class="expertise-subs" role="tablist" '
                     f'aria-label="{"Sous-catégories" if fr else "Subcategories"}">')
        lines.append(
            f'<button type="button" class="expertise-sub" data-sub="all" '
            f'aria-selected="true">{all_label}</button>'
        )
        for sid, sen, sfr, _items in subs:
            slabel = sfr if fr else sen
            lines.append(
                f'<button type="button" class="expertise-sub" data-sub="{sid}" '
                f'aria-selected="false">{slabel}</button>'
            )
        lines.append("</div>")
        lines.append('<div class="expertise-main">')
        lines.append('<div class="expertise-main-head">')
        lines.append(f'<h3 class="expertise-main-title">{dlabel}</h3>')
        lines.append(f'<span class="expertise-count" data-expertise-count>{count_label}</span>')
        lines.append("</div>")
        for sid, sen, sfr, items in subs:
            slabel = sfr if fr else sen
            lines.append(f'<div class="expertise-subgroup" data-sub-panel="{sid}">')
            lines.append(f'<p class="expertise-subgroup-label">{slabel}</p>')
            # normalize items to 4-tuples
            norm = []
            for it in items:
                if len(it) == 4:
                    norm.append(it)
                else:
                    norm.append((*it, None))
            lines.append(pills(lang, norm))
            lines.append("</div>")
        lines.append(f'<p class="expertise-empty" data-expertise-empty hidden>{empty}</p>')
        lines.append("</div></div></div>")

    lines.append("</div></div>")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    print(render(lang))

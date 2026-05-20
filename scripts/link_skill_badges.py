"""Link competence skill badges to official docs (index-en.html, index-fr.html)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SKILL_URLS: dict[str, str] = {
    "OpenGL": "https://www.opengl.org/",
    "GLSL": "https://www.khronos.org/opengl/wiki/OpenGL_Shading_Language",
    "C++": "https://isocpp.org/",
    "Blender": "https://www.blender.org/",
    "CUDA": "https://developer.nvidia.com/cuda-toolkit",
    "OpenCV": "https://opencv.org/",
    "Java": "https://dev.java/",
    "Kotlin": "https://kotlinlang.org/",
    "Python": "https://www.python.org/",
    "JavaScript": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
    "Spring Boot": "https://spring.io/projects/spring-boot",
    "Django": "https://www.djangoproject.com/",
    "Flask": "https://flask.palletsprojects.com/",
    "API REST": "https://developer.mozilla.org/fr/docs/Glossary/REST",
    "Microservices": "https://microservices.io/",
    "C#": "https://learn.microsoft.com/dotnet/csharp/",
    ".NET": "https://dotnet.microsoft.com/",
    "Android": "https://developer.android.com/",
    "GraphQL": "https://graphql.org/",
    "HTML": "https://developer.mozilla.org/docs/Web/HTML",
    "Angular": "https://angular.dev/",
    "React": "https://react.dev/",
    "Vue": "https://vuejs.org/",
    "CSS": "https://developer.mozilla.org/docs/Web/CSS",
    "TypeScript": "https://www.typescriptlang.org/",
    "Git": "https://git-scm.com/",
    "GitLab CI/CD": "https://docs.gitlab.com/ee/ci/",
    "Pipelines GitLab": "https://docs.gitlab.com/ee/ci/pipelines/",
    "GitHub Actions": "https://docs.github.com/en/actions",
    "Azure DevOps": "https://azure.microsoft.com/products/devops",
    "DevOps": "https://aws.amazon.com/devops/what-is-devops/",
    "DevSecOps": "https://www.devsecops.org/",
    "Docker": "https://www.docker.com/",
    "Kubernetes": "https://kubernetes.io/",
    "Docker Swarm": "https://docs.docker.com/engine/swarm/",
    "IaC": "https://developer.hashicorp.com/terraform/tutorials",
    "GCP": "https://cloud.google.com/",
    "Azure": "https://azure.microsoft.com/",
    "AWS": "https://aws.amazon.com/",
    "Terraform": "https://www.terraform.io/",
    "ELK": "https://www.elastic.co/elastic-stack",
    "Elasticsearch": "https://www.elastic.co/elasticsearch/",
    "Kibana": "https://www.elastic.co/kibana/",
    "Grafana": "https://grafana.com/",
    "Prometheus": "https://prometheus.io/",
    "Sentry": "https://sentry.io/",
    "Serilog": "https://serilog.net/",
    "SQL": "https://www.iso.org/standard/76583.html",
    "PostgreSQL": "https://www.postgresql.org/",
    "MySQL": "https://www.mysql.com/",
    "MongoDB": "https://www.mongodb.com/",
    "Redis": "https://redis.io/",
    "Kafka": "https://kafka.apache.org/",
    "Science des données": "https://scikit-learn.org/",
    "Playwright": "https://playwright.dev/",
    "Selenium": "https://www.selenium.dev/",
    "JUnit": "https://junit.org/junit5/",
    "Linux": "https://www.kernel.org/",
    "Bash": "https://www.gnu.org/software/bash/",
    "Ansible": "https://www.ansible.com/",
    "MCP": "https://modelcontextprotocol.io/",
    "Auth0": "https://auth0.com/",
    "OWASP": "https://owasp.org/",
    "Agile": "https://agilemanifesto.org/",
    "SCRUM": "https://scrumguides.org/",
    "Kanban": "https://kanban.university/what-is-kanban/",
    "Livraison orientée sécurité": "https://owasp.org/www-project-devsecops-guidelines/",
    "Open-source maintainer (uml-mcp)": "https://github.com/antoinebou12/uml-mcp",
    "Mainteneur open source (uml-mcp)": "https://github.com/antoinebou12/uml-mcp",
}

SPAN_RE = re.compile(
    r'<span class="skill badge(?!\s+skill-badge-note)">([^<]+)</span>'
)

MARKERS = (
    ("<!-- COMPETENCES -->", "<!-- COMPÉTENCES -->"),
    ("<!-- COMPETENCES -->", "<!-- COMPÉTENCES -->"),
    ("<!-- RECOMMENDATIONS -->", "<!-- RECOMMANDATIONS -->"),
)


def link_badges(html: str) -> tuple[str, int]:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        label = match.group(1)
        url = SKILL_URLS.get(label)
        if not url:
            return match.group(0)
        count += 1
        return (
            f'<a class="skill badge" href="{url}" target="_blank" '
            f'rel="noopener noreferrer">{label}</a>'
        )

    return SPAN_RE.sub(repl, html), count


def main() -> None:
    for name in ("index-en.html", "index-fr.html"):
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        new_text, n = link_badges(text)
        path.write_text(new_text, encoding="utf-8")
        print(f"{name}: linked {n} skill badges")


if __name__ == "__main__":
    main()

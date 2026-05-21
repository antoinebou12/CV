#!/usr/bin/env python3
"""Generate About/FAQ HTML and patch CV pages from data/aeo.yaml."""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from _repo import REPO_ROOT, script_path
AEO_PATH = REPO_ROOT / "data" / "aeo.yaml"
SITE_ROOT = "https://antoineboucher.info/CV"
BLOG_URL = "https://antoineboucher.info/CV/blog/"

JSONLD_BEGIN = "<!-- AEO_JSONLD:BEGIN -->"
JSONLD_END = "<!-- AEO_JSONLD:END -->"
LEAD_BEGIN = "<!-- AEO_LEAD:BEGIN -->"
LEAD_END = "<!-- AEO_LEAD:END -->"
FRESHNESS_BEGIN = "<!-- AEO_FRESHNESS:BEGIN -->"
FRESHNESS_END = "<!-- AEO_FRESHNESS:END -->"
UPDATED_BEGIN = "<!-- CV_LAST_UPDATED:BEGIN -->"
UPDATED_END = "<!-- CV_LAST_UPDATED:END -->"

LOCALES = {
    "en": {
        "about": REPO_ROOT / "about-en.html",
        "cv": REPO_ROOT / "index-en.html",
        "page_url": f"{SITE_ROOT}/about-en.html",
        "cv_url": f"{SITE_ROOT}/index-en.html",
        "lang": "en",
        "html_lang": "en",
        "title": "About Antoine Boucher",
        "person_name": "Antoine Boucher",
        "home_label": "Home",
        "cv_href": "index-en.html",
        "about_label": "About",
        "blog_nav": "Blog",
        "back_home": "Back to home",
        "faq_heading": "Frequently asked questions",
        "faq_subtitle": "Short answers for recruiters, collaborators, and search agents.",
        "recognition_heading": "Recognition and proof points",
        "recognition_subtitle": "A compact section for credibility without overloading the page.",
        "summary_aria": "Recruiter summary",
        "actions_aria": "Primary actions",
        "tags_heading_id": "about-tags-en",
        "tags_aria": "Core strengths",
        "last_updated_label": "Last updated",
        "date_locale": "en_CA",
    },
    "fr": {
        "about": REPO_ROOT / "about-fr.html",
        "cv": REPO_ROOT / "index-fr.html",
        "page_url": f"{SITE_ROOT}/about-fr.html",
        "cv_url": f"{SITE_ROOT}/index-fr.html",
        "lang": "fr",
        "html_lang": "fr",
        "title": "À propos — Antoine Boucher",
        "person_name": "Antoine Boucher",
        "home_label": "Accueil",
        "cv_href": "index-fr.html",
        "about_label": "À propos",
        "blog_nav": "Blog",
        "back_home": "Retour à l'accueil",
        "faq_heading": "Foire aux questions",
        "faq_subtitle": "Réponses courtes pour recruteurs, collaborateurs et agents de recherche.",
        "recognition_heading": "Reconnaissance et preuves",
        "recognition_subtitle": "Une section compacte pour la crédibilité sans surcharger la page.",
        "summary_aria": "Résumé pour recruteurs",
        "actions_aria": "Actions principales",
        "tags_heading_id": "about-tags-fr",
        "tags_aria": "Forces principales",
        "last_updated_label": "Dernière mise à jour",
        "date_locale": "fr_CA",
    },
}


def load_aeo() -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML required (pip install pyyaml)")
    return yaml.safe_load(AEO_PATH.read_text(encoding="utf-8"))


def iso_modified(date_str: str) -> str:
    return f"{date_str}T12:00:00+00:00"


def format_display_date(date_str: str, locale: str) -> str:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    if locale.startswith("fr"):
        months = (
            "janvier",
            "février",
            "mars",
            "avril",
            "mai",
            "juin",
            "juillet",
            "août",
            "septembre",
            "octobre",
            "novembre",
            "décembre",
        )
        return f"{dt.day} {months[dt.month - 1]} {dt.year}"
    return dt.strftime("%d %B %Y")


def esc(text: str) -> str:
    return html.escape(text.strip(), quote=True)


def lang_text(block: dict | None, lang: str) -> str:
    if not block:
        return ""
    if isinstance(block, str):
        return block.strip()
    return (block.get(lang) or "").strip()


def linkify_urls(escaped_text: str) -> str:
    """Turn https:// URLs in already-escaped text into safe anchor tags."""

    def repl(match: re.Match[str]) -> str:
        url = match.group(0).rstrip(").,;")
        trail = match.group(0)[len(url) :]
        return f'<a href="{url}" rel="noopener noreferrer">{url}</a>{trail}'

    return re.sub(r"https://[^\s<]+", repl, escaped_text)


def linkify_contact_answer(escaped_text: str, lang: str) -> str:
    """Linkify URLs and add mailto for contact FAQ answers (plain escaped text only)."""
    text = escaped_text
    if lang == "en":
        text = text.replace(
            "https://cal.com/antoine-boucher-dev/30min",
            '<a href="https://cal.com/antoine-boucher-dev/30min" rel="noopener noreferrer">Cal.com</a>',
            1,
        )
        text = text.replace(
            "antoine@antoineboucher.info",
            '<a href="mailto:antoine@antoineboucher.info">antoine@antoineboucher.info</a>',
            1,
        )
        text = text.replace(
            "https://antoineboucher.info/CV/index-en.html",
            '<a href="https://antoineboucher.info/CV/index-en.html" rel="noopener noreferrer">'
            "antoineboucher.info/CV/index-en.html</a>",
            1,
        )
    else:
        text = text.replace(
            "https://cal.com/antoine-boucher-dev/30min",
            '<a href="https://cal.com/antoine-boucher-dev/30min" rel="noopener noreferrer">Cal.com</a>',
            1,
        )
        text = text.replace(
            "antoine@antoineboucher.info",
            '<a href="mailto:antoine@antoineboucher.info">antoine@antoineboucher.info</a>',
            1,
        )
        text = text.replace(
            "https://antoineboucher.info/CV/index-fr.html",
            '<a href="https://antoineboucher.info/CV/index-fr.html" rel="noopener noreferrer">'
            "antoineboucher.info/CV/index-fr.html</a>",
            1,
        )
    return text


def linkify_machine_readable(escaped_text: str, lang: str) -> str:
    text = escaped_text
    if lang == "en":
        replacements = [
            (
                "https://antoineboucher.info/CV/resume.json",
                '<a href="https://antoineboucher.info/CV/resume.json" rel="noopener noreferrer">resume.json</a>',
            ),
            (
                "https://antoineboucher.info/CV/resume.md",
                '<a href="https://antoineboucher.info/CV/resume.md" rel="noopener noreferrer">resume.md</a>',
            ),
            (
                "https://antoineboucher.info/CV/.well-known/",
                '<a href="https://antoineboucher.info/CV/.well-known/" rel="noopener noreferrer">.well-known</a>',
            ),
        ]
    else:
        replacements = [
            (
                "https://antoineboucher.info/CV/resume-fr.json",
                '<a href="https://antoineboucher.info/CV/resume-fr.json" rel="noopener noreferrer">resume-fr.json</a>',
            ),
            (
                "https://antoineboucher.info/CV/resume-fr.md",
                '<a href="https://antoineboucher.info/CV/resume-fr.md" rel="noopener noreferrer">resume-fr.md</a>',
            ),
            (
                "https://antoineboucher.info/CV/.well-known/",
                '<a href="https://antoineboucher.info/CV/.well-known/" rel="noopener noreferrer">.well-known</a>',
            ),
        ]
    for old, new in replacements:
        text = text.replace(old, new, 1)
    return text


def format_faq_answer(item_id: str, a_raw: str, lang: str) -> str:
    collapsed = " ".join(a_raw.split())
    escaped = esc(collapsed)
    if item_id == "contact":
        return linkify_contact_answer(escaped, lang)
    if item_id == "machine-readable":
        return linkify_machine_readable(escaped, lang)
    if item_id == "uml-mcp":
        escaped = escaped.replace(
            "https://github.com/antoinebou12/uml-mcp",
            '<a href="https://github.com/antoinebou12/uml-mcp" rel="noopener noreferrer">'
            "github.com/antoinebou12/uml-mcp</a>",
        )
        return escaped
    return linkify_urls(escaped)


PARTICLES_SCRIPT = """  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js" defer></script>
  <script>
    (function () {
      function initParticles() {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
        if (typeof particlesJS !== 'function') return;
        particlesJS('particles-js', {
        particles: {
          number: { value: 200, density: { enable: true, value_area: 2400 } },
          color: { value: "#ffffff" },
          shape: { type: "circle", stroke: { width: 1, color: "#000000" }, polygon: { nb_sides: 6 } },
          opacity: { value: 0.5, random: false, anim: { enable: false, speed: 1, opacity_min: 0.1, sync: false } },
          size: { value: 3, random: true, anim: { enable: false, speed: 40, size_min: 0.1, sync: false } },
          line_linked: { enable: true, distance: 150, color: "#ffffff", opacity: 0.4, width: 1 },
          move: { enable: true, speed: 6, direction: "none", random: false, straight: false, out_mode: "out", bounce: false, attract: { enable: false, rotateX: 600, rotateY: 1200 } }
        },
        interactivity: {
          detect_on: "canvas",
          events: { onhover: { enable: true, mode: "repulse" }, onclick: { enable: true, mode: "push" }, resize: true },
          modes: {
            grab: { distance: 140, line_linked: { opacity: 1 } },
            bubble: { distance: 400, size: 40, duration: 2, opacity: 8, speed: 3 },
            repulse: { distance: 200, duration: 0.4 },
            push: { particles_nb: 4 },
            remove: { particles_nb: 2 }
          }
        },
        retina_detect: true
      });
      }
      if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initParticles);
      } else {
        initParticles();
      }
    })();
  </script>"""


def faq_jsonld(
    faq: list,
    lang: str,
    page_url: str,
    page_title: str,
    knows_about: list[str] | None,
) -> dict:
    entities = []
    for item in faq:
        q = lang_text(item.get("question"), lang)
        a = lang_text(item.get("answer"), lang)
        if not q or not a:
            continue
        entities.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": " ".join(a.split())},
            }
        )
    person_id = f"{page_url}#person"
    webpage_id = f"{page_url}#webpage"
    faq_id = f"{page_url}#faq"
    person_node: dict = {
        "@type": "Person",
        "@id": person_id,
        "name": "Antoine Boucher",
        "url": page_url,
        "sameAs": [
            "https://github.com/antoinebou12",
            "https://www.linkedin.com/in/antoineboucher",
            "https://cal.com/antoine-boucher-dev/30min",
        ],
    }
    if knows_about:
        person_node["knowsAbout"] = knows_about
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": webpage_id,
                "url": page_url,
                "name": page_title,
                "inLanguage": lang,
                "dateModified": None,
                "datePublished": None,
                "mainEntity": {"@id": faq_id},
                "about": {"@id": person_id},
                "speakable": {
                    "@type": "SpeakableSpecification",
                    "cssSelector": [".aeo-about-intro", ".aeo-faq-answer"],
                },
            },
            {"@type": "FAQPage", "@id": faq_id, "mainEntity": entities},
            person_node,
        ],
    }


def build_hero_actions(hero: dict, lang: str) -> str:
    lines = []
    for action in hero.get("actions") or []:
        label = lang_text(action.get("label"), lang)
        href_block = action.get("href")
        if isinstance(href_block, dict):
            href = lang_text(href_block, lang)
        else:
            href = (href_block or "").strip()
        if not label or not href:
            continue
        btn = "btn btn-primary" if action.get("primary") else "btn btn-default"
        rel = ' rel="noopener noreferrer"' if action.get("external") else ""
        target = ' target="_blank"' if action.get("external") else ""
        lines.append(
            f'              <a href="{esc(href)}" class="{btn}"{rel}{target}>{esc(label)}</a>'
        )
    return "\n".join(lines)


def build_hero_tags(hero: dict, lang: str) -> str:
    tags = (hero.get("tags") or {}).get(lang) or []
    return "\n".join(
        f'            <span class="project-tag">{esc(tag)}</span>' for tag in tags
    )


def build_summary_list(cards: list, lang: str) -> str:
    parts = []
    for card in cards:
        title = lang_text(card.get("title"), lang)
        body = lang_text(card.get("body"), lang)
        parts.append(
            "          <li class=\"list-group-item\">"
            f"<strong>{esc(title)}:</strong> {esc(' '.join(body.split()))}</li>"
        )
    return "\n".join(parts)


def build_faq_details(faq: list, lang: str) -> str:
    lines = []
    for idx, item in enumerate(faq):
        q = esc(lang_text(item.get("question"), lang))
        item_id = item.get("id", "")
        a_html = format_faq_answer(
            item_id, lang_text(item.get("answer"), lang), lang
        )
        open_attr = " open" if idx == 0 else ""
        lines.append(
            f'          <details class="cv-faq-item"{open_attr}>\n'
            f'            <summary id="faq-{item_id}">{q}</summary>\n'
            f'            <p class="cv-faq-answer aeo-faq-answer">{a_html}</p>\n'
            f"          </details>"
        )
    return "\n".join(lines)


def build_cv_section(
    *,
    open_default: bool,
    icon: str,
    heading: str,
    subtitle: str,
    heading_id: str,
    body_html: str,
) -> str:
    open_attr = " open" if open_default else ""
    intro = (
        f'          <p class="section-intro">{esc(subtitle)}</p>\n'
        if subtitle
        else ""
    )
    return f"""        <details class="box cv-section"{open_attr}>
          <summary class="cv-section-summary"><h2 class="cv-section-heading" id="{heading_id}"><i class="fas {icon} ico"></i> {esc(heading)}</h2></summary>
          <div class="cv-section-body">
{intro}{body_html}
          </div>
        </details>"""


def cv_nav_about_block(locale: str) -> str:
    nav_aria = "Site and language" if locale == "en" else "Site et langue"
    lang_aria = "Language" if locale == "en" else "Langue"
    en_current = ' class="current"' if locale == "en" else ""
    fr_current = ' class="current"' if locale == "fr" else ""
    blog = LOCALES["en"]["blog_nav"] if locale == "en" else LOCALES["fr"]["blog_nav"]
    return f"""  <nav class="cv-site-nav" aria-label="{nav_aria}">
    <a class="cv-nav-pill cv-nav-blog" href="{BLOG_URL}">{blog}</a>
    <div class="cv-nav-pill cv-nav-lang" aria-label="{lang_aria}">
      <a href="about-en.html"{en_current}>EN</a><span class="sep" aria-hidden="true"> | </span><a href="about-fr.html"{fr_current}>FR</a>
    </div>
  </nav>"""


def build_about_html(locale: str, aeo: dict) -> str:
    cfg = LOCALES[locale]
    lang = cfg["lang"]
    lead = lang_text(aeo.get("lead"), lang)
    meta_desc = lang_text(aeo.get("metaDescription"), lang) or lead[:155]
    faq = aeo.get("faq") or []
    recognition = (aeo.get("recognition") or {}).get(lang) or []
    hero = aeo.get("hero") or {}
    summary_cards = aeo.get("summaryCards") or []
    tech = aeo.get("technicalProfile") or {}
    knows = (aeo.get("personKnowsAbout") or {}).get(lang)
    last = aeo.get("lastUpdated", "2026-05-21")
    published = aeo.get("datePublished", "2024-06-01")
    mod_iso = iso_modified(last)
    display = format_display_date(last, cfg["date_locale"])

    graph = faq_jsonld(
        faq, lang, cfg["page_url"], cfg["title"], knows if knows else None
    )
    for node in graph["@graph"]:
        if node.get("@type") == "WebPage":
            node["dateModified"] = mod_iso
            node["datePublished"] = iso_modified(published)

    jsonld = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))

    position = (
        "Software Engineer · Platform and graphics"
        if lang == "en"
        else "Ingénieur logiciel · Plateforme et infographie"
    )
    actions_html = build_hero_actions(hero, lang)
    tags_html = build_hero_tags(hero, lang)
    summary_list = build_summary_list(summary_cards, lang)
    faq_html = build_faq_details(faq, lang)
    rec_items = "\n".join(
        f'            <li class="list-group-item">{esc(line)}</li>' for line in recognition
    )
    tech_bullets = (tech.get("bullets") or {}).get(lang) or []
    tech_list = "\n".join(
        f'            <li class="list-group-item">{esc(line)}</li>' for line in tech_bullets
    )

    summary_heading = "At a glance" if lang == "en" else "En bref"
    summary_section = build_cv_section(
        open_default=True,
        icon="fa-compass",
        heading=summary_heading,
        subtitle="",
        heading_id="summary-heading",
        body_html=f"          <ul class=\"list-group\">\n{summary_list}\n          </ul>",
    )
    faq_section = build_cv_section(
        open_default=True,
        icon="fa-question-circle",
        heading=cfg["faq_heading"],
        subtitle=cfg["faq_subtitle"],
        heading_id="faq-heading",
        body_html=f"{faq_html}",
    )
    recognition_section = build_cv_section(
        open_default=True,
        icon="fa-award",
        heading=cfg["recognition_heading"],
        subtitle=cfg["recognition_subtitle"],
        heading_id="recognition-heading",
        body_html=f"          <ul class=\"list-group\">\n{rec_items}\n          </ul>",
    )
    tech_section = build_cv_section(
        open_default=False,
        icon="fa-code",
        heading=lang_text(tech.get("heading"), lang),
        subtitle=lang_text(tech.get("subtitle"), lang),
        heading_id="technical-profile-heading",
        body_html=f"          <ul class=\"list-group\">\n{tech_list}\n          </ul>",
    )

    skip = "Skip to main content" if lang == "en" else "Aller au contenu principal"
    nav_html = cv_nav_about_block(locale)
    agent_note = (
        "Structured profile for search agents and parsers. Human readers can use the interactive CV."
        if lang == "en"
        else "Profil structuré pour agents de recherche et parseurs. Les lecteurs humains peuvent utiliser le CV interactif."
    )

    return f"""<!DOCTYPE html>
<html lang="{cfg["html_lang"]}">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(cfg["title"])}</title>
  <meta name="description" content="{esc(meta_desc)}">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{esc(cfg["title"])}">
  <meta name="twitter:description" content="{esc(meta_desc)}">
  <link rel="canonical" href="{cfg["page_url"]}">
  <link rel="alternate" hreflang="en" href="{SITE_ROOT}/about-en.html">
  <link rel="alternate" hreflang="fr" href="{SITE_ROOT}/about-fr.html">
  <link rel="alternate" hreflang="x-default" href="{SITE_ROOT}/about-en.html">
  <meta property="og:title" content="{esc(cfg["title"])}">
  <meta property="og:description" content="{esc(meta_desc)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{cfg["page_url"]}">
  <meta property="article:modified_time" content="{mod_iso}">
  <meta property="article:published_time" content="{iso_modified(published)}">
{JSONLD_BEGIN}
  <script type="application/ld+json">
{jsonld}
  </script>
{JSONLD_END}
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css" rel="stylesheet">
  <link rel="stylesheet" href="css/cv-site-nav.css">
  <link rel="stylesheet" href="css/cv-main.css">
  <link rel="stylesheet" href="css/cv-aeo.css">
  <link rel="stylesheet" href="css/cv-about-page.css">
</head>

<body>
  <a class="skip-link" href="#main">{skip}</a>
{nav_html}
  <div id="particles-js"></div>
  <main id="main" class="container cv-about-page">
    <div class="row">
      <div class="col-xs-12">
        <div id="photo-header" class="text-center">
          <div id="photo">
            <img src="antoine.png" alt="{esc(cfg["person_name"])}" width="160" height="160" fetchpriority="high" decoding="async">
          </div>
          <div id="text-header">
            <h1>{esc(cfg["person_name"])}<br><span>{esc(position)}</span></h1>
            <p class="aeo-about-intro aeo-lead">{esc(" ".join(lead.split()))}</p>
            <div class="hero-actions">
{actions_html}
            </div>
            <div class="cv-about-tags project-tags" aria-label="{esc(cfg["tags_aria"])}">
{tags_html}
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-xs-12">
        <p class="section-intro">{esc(agent_note)}</p>
{summary_section}
{faq_section}
{recognition_section}
{tech_section}
      </div>
    </div>
    <p class="cv-last-updated">{esc(cfg["last_updated_label"])}: <time datetime="{last}">{display}</time></p>
  </main>
{PARTICLES_SCRIPT}
</body>
</html>
"""


def freshness_meta_block(last: str, published: str) -> str:
    mod = iso_modified(last)
    pub = iso_modified(published)
    return (
        f"{FRESHNESS_BEGIN}\n"
        f'  <meta property="article:modified_time" content="{mod}">\n'
        f'  <meta property="article:published_time" content="{pub}">\n'
        f"{FRESHNESS_END}"
    )


def lead_block(lead: str) -> str:
    text = esc(" ".join(lead.split()))
    return (
        f"{LEAD_BEGIN}\n"
        f'    <p class="aeo-about-intro aeo-lead aeo-agent-only">{text}</p>\n'
        f"{LEAD_END}"
    )


def last_updated_block(locale: str, last: str) -> str:
    cfg = LOCALES[locale]
    display = format_display_date(last, cfg["date_locale"])
    label = cfg["last_updated_label"]
    return (
        f"{UPDATED_BEGIN}\n"
        f'    <p class="cv-last-updated">{esc(label)}: '
        f'<time datetime="{last}">{display}</time></p>\n'
        f"{UPDATED_END}"
    )


def cv_nav_block(locale: str) -> str:
    cfg = LOCALES[locale]
    nav_aria = "Site and language" if locale == "en" else "Site et langue"
    lang_aria = "Language" if locale == "en" else "Langue"
    en_current = ' class="current"' if locale == "en" else ""
    fr_current = ' class="current"' if locale == "fr" else ""
    return f"""  <nav class="cv-site-nav" aria-label="{nav_aria}">
    <a class="cv-nav-pill cv-nav-blog" href="{BLOG_URL}">{cfg["blog_nav"]}</a>
    <div class="cv-nav-pill cv-nav-lang" aria-label="{lang_aria}">
      <a href="index-en.html"{en_current}>EN</a><span class="sep" aria-hidden="true"> | </span><a href="index-fr.html"{fr_current}>FR</a>
    </div>
  </nav>"""


def replace_block(html: str, begin: str, end: str, new: str) -> str:
    pattern = re.compile(rf"{re.escape(begin)}.*?{re.escape(end)}", re.DOTALL)
    if pattern.search(html):
        return pattern.sub(new, html, count=1)
    return html


def patch_cv_about_intro(html: str, locale: str) -> str:
    if locale == "en":
        old = (
            '          <p class="section-intro"><a href="about-en.html">About and FAQ</a> '
            "for platform focus, teaching context, and how to reach me.</p>"
        )
        new = (
            "          <p class=\"section-intro\">Platform and graphics focus; teaching context "
            "and contact are in the sections below.</p>\n"
            '          <a href="about-en.html" class="aeo-agent-only">About and FAQ for search agents</a>'
        )
    else:
        old = (
            '          <p class="section-intro"><a href="about-fr.html">À propos et FAQ</a> '
            ": orientation plateforme et infographie, enseignement et contact.</p>"
        )
        new = (
            "          <p class=\"section-intro\">Orientation plateforme et infographie ; "
            "enseignement et contact dans les sections ci-dessous.</p>\n"
            '          <a href="about-fr.html" class="aeo-agent-only">À propos et FAQ pour les agents de recherche</a>'
        )
    return html.replace(old, new, 1) if old in html else html


def patch_cv(locale: str, aeo: dict) -> None:
    cfg = LOCALES[locale]
    path = cfg["cv"]
    html = path.read_text(encoding="utf-8")
    lang = cfg["lang"]
    lead = lang_text(aeo.get("lead"), lang)
    last = aeo.get("lastUpdated", "2026-05-21")
    published = aeo.get("datePublished", "2024-06-01")
    html = patch_cv_about_intro(html, locale)

    if "cv-aeo.css" not in html:
        html = html.replace(
            '<link rel="stylesheet" href="css/cv-print.css" media="print">',
            '<link rel="stylesheet" href="css/cv-aeo.css">\n'
            '  <link rel="stylesheet" href="css/cv-print.css" media="print">',
            1,
        )

    fresh = freshness_meta_block(last, published)
    if FRESHNESS_BEGIN in html:
        html = replace_block(html, FRESHNESS_BEGIN, FRESHNESS_END, fresh)
    else:
        html = html.replace("</title>", f"</title>\n{fresh}", 1)

    nav_new = cv_nav_block(locale)
    skip_nav_pat = re.compile(
        r'(<a class="skip-link"[^>]*>.*?</a>)\s*<nav class="cv-site-nav"[^>]*>.*?</nav>',
        re.DOTALL,
    )
    html = skip_nav_pat.sub(rf"\1\n{nav_new}", html, count=1)

    lead_new = lead_block(lead) if lead.strip() else ""
    if LEAD_BEGIN in html and UPDATED_BEGIN in html:
        if lead_new:
            html = replace_block(html, LEAD_BEGIN, LEAD_END, lead_new)
        else:
            html = replace_block(html, LEAD_BEGIN, LEAD_END, "")
    elif lead_new:
        if UPDATED_BEGIN in html:
            html = html.replace(UPDATED_BEGIN, f"{lead_new}\n{UPDATED_BEGIN}", 1)
        else:
            html = html.replace("  </main>", f"{lead_new}\n  </main>", 1)

    updated = last_updated_block(locale, last)
    if UPDATED_BEGIN in html:
        html = replace_block(html, UPDATED_BEGIN, UPDATED_END, updated)
    else:
        html = html.replace("  </main>", f"{updated}\n  </main>", 1)

    html = re.sub(r"\n{4,}(?=<!-- AEO_LEAD:BEGIN -->)", "\n\n", html)

    path.write_text(html, encoding="utf-8", newline="\n")
    print(f"Updated {path}")


def process_locale(locale: str, aeo: dict) -> None:
    about_html = build_about_html(locale, aeo)
    about_path = LOCALES[locale]["about"]
    about_path.write_text(about_html, encoding="utf-8", newline="\n")
    print(f"Wrote {about_path}")
    patch_cv(locale, aeo)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--locale", choices=sorted(LOCALES))
    p.add_argument("--all", action="store_true")
    args = p.parse_args()
    if not args.all and not args.locale:
        p.error("Specify --locale or --all")
    try:
        aeo = load_aeo()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    locales = sorted(LOCALES) if args.all else [args.locale]
    for loc in locales:
        process_locale(loc, aeo)
    if "en" in locales:
        import subprocess

        sync = script_path("html", "sync_index_html.py")
        subprocess.run([sys.executable, str(sync)], cwd=REPO_ROOT, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

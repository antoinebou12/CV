#!/usr/bin/env python3
"""Apply CV index UX redesign (nav, flatten nests, domain competence cards)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable


def soup_file(path: Path) -> BeautifulSoup:
    return BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")


def find_section(soup: BeautifulSoup, heading_substr: str) -> Tag | None:
    for details in soup.select("details.cv-section"):
        h2 = details.find("h2", class_="cv-section-heading")
        if h2 and heading_substr.lower() in h2.get_text(" ", strip=True).lower():
            return details
    return None


def set_section_id(details: Tag | None, section_id: str) -> None:
    if details is not None:
        details["id"] = section_id


def add_nav(soup: BeautifulSoup, lang: str) -> None:
    nav = soup.select_one("nav.cv-site-nav")
    if not nav:
        return
    # Remove prior section links if re-run
    for a in list(nav.select("a.cv-nav-section")):
        a.decompose()
    labels = (
        [
            ("#work", "Work"),
            ("#projects", "Projects"),
            ("#skills", "Skills"),
            ("#contact", "Contact"),
        ]
        if lang == "en"
        else [
            ("#work", "Travail"),
            ("#projects", "Projets"),
            ("#skills", "Compétences"),
            ("#contact", "Contact"),
        ]
    )
    blog = nav.select_one("a.cv-nav-blog")
    for href, label in labels:
        a = soup.new_tag("a", href=href, attrs={"class": "cv-nav-section"})
        a.string = label
        if blog:
            blog.insert_before(a)
            blog.insert_before(NavigableString("\n    "))
        else:
            nav.append(a)


def unwrap_details_to_block(
    details: Tag,
    *,
    heading_tag: str,
    heading_class: str,
    body_class: str | None,
    title_from_summary: bool = True,
) -> Tag:
    """Replace a details with a static section: h* + body contents."""
    soup = details
    while not isinstance(soup, BeautifulSoup):
        soup = soup.parent  # type: ignore[assignment]
    summary = details.find("summary", recursive=False)
    title = ""
    if summary and title_from_summary:
        title = summary.get_text(" ", strip=True)
    body = None
    for child in list(details.children):
        if isinstance(child, Tag) and child.name != "summary":
            if body is None:
                body = child
            # keep first non-summary block as body container if class matches
    wrapper = soup.new_tag("div")
    if details.get("class"):
        # preserve semantic class hint without details behavior
        classes = [c for c in details.get("class", []) if c not in ("project-group", "project-subgroup")]
        if classes:
            wrapper["class"] = classes
    if details.get("id"):
        wrapper["id"] = details["id"]
    if title:
        h = soup.new_tag(heading_tag, attrs={"class": heading_class})
        h.string = title
        wrapper.append(h)
    # Move all non-summary children into wrapper
    for child in list(details.children):
        if isinstance(child, Tag) and child.name == "summary":
            continue
        if isinstance(child, Tag):
            # unwrap body divs with known classes
            cls = child.get("class") or []
            if any(
                c in cls
                for c in (
                    "project-group-body",
                    "project-subgroup-body",
                    "cv-course-body",
                    "project-preview-panel",
                    "skill-group-body",
                )
            ):
                for gc in list(child.children):
                    wrapper.append(gc.extract() if hasattr(gc, "extract") else gc)
                child.decompose()
            else:
                wrapper.append(child.extract())
        elif isinstance(child, NavigableString) and str(child).strip():
            wrapper.append(child.extract())
    if body_class:
        wrapper["class"] = list(wrapper.get("class") or []) + [body_class]
    details.replace_with(wrapper)
    return wrapper


def flatten_courses(soup: BeautifulSoup) -> None:
    for details in list(soup.select("details.cv-course")):
        summary = details.find("summary")
        body = details.find(class_="cv-course-body")
        block = soup.new_tag("div", attrs={"class": "cv-course"})
        title = soup.new_tag("p", attrs={"class": "cv-course-title"})
        if summary:
            # keep inner HTML of summary (links)
            for c in list(summary.contents):
                title.append(c.extract() if hasattr(c, "extract") else c)
        block.append(title)
        if body:
            p = soup.new_tag("p", attrs={"class": "cv-course-body"})
            p.extend(list(body.contents))
            block.append(p)
        details.replace_with(block)


def flatten_project_previews(soup: BeautifulSoup) -> None:
    for details in list(soup.select("details.project-preview")):
        # Keep publication video as details (optional) — only flatten project cards
        if "publication-video-preview" in (details.get("class") or []):
            continue
        summary = details.find("summary")
        panel = details.find(class_="project-preview-panel")
        block = soup.new_tag("div", attrs={"class": "project-preview-open"})
        if summary:
            label = soup.new_tag("p", attrs={"class": "project-preview-label"})
            label.string = summary.get_text(" ", strip=True)
            block.append(label)
        if panel:
            for c in list(panel.children):
                block.append(c.extract() if hasattr(c, "extract") else c)
        details.replace_with(block)


def flatten_projects(soup: BeautifulSoup, lang: str) -> None:
    section = find_section(soup, "selected projects" if lang == "en" else "projets")
    if not section:
        section = find_section(soup, "projets sélectionnés")
    if not section:
        return
    body = section.select_one(".cv-section-body")
    if not body:
        return

    # Personal group → static h3 + content
    for group in list(body.select(":scope > details.project-group")):
        summary = group.find("summary", class_="project-group-title")
        title = summary.get_text(" ", strip=True) if summary else "Projects"
        gbody = group.find(class_="project-group-body")
        block = soup.new_tag("div", attrs={"class": "project-group-static"})
        h = soup.new_tag("h3", attrs={"class": "project-group-heading"})
        h.string = title
        block.append(h)
        if gbody:
            for c in list(gbody.children):
                block.append(c.extract() if hasattr(c, "extract") else c)
        is_collab = "collabor" in title.lower() or "contribution" in title.lower()
        if is_collab:
            # Flatten subgroups inside collaborative block
            for sub in list(block.select("details.project-subgroup")):
                sub_summary = sub.find("summary", class_="project-subgroup-title")
                sub_title = sub_summary.get_text(" ", strip=True) if sub_summary else "Group"
                sub_body = sub.find(class_="project-subgroup-body")
                other = "other accepted" in sub_title.lower() or "autres contributions" in sub_title.lower()
                if other:
                    # Keep as one optional collapsed details
                    new_d = soup.new_tag("details", attrs={"class": "project-other"})
                    new_s = soup.new_tag("summary", attrs={"class": "project-other-summary"})
                    new_s.string = sub_title
                    new_d.append(new_s)
                    wrap = soup.new_tag("div", attrs={"class": "project-other-body"})
                    if sub_body:
                        for c in list(sub_body.children):
                            wrap.append(c.extract() if hasattr(c, "extract") else c)
                    new_d.append(wrap)
                    sub.replace_with(new_d)
                else:
                    sub_block = soup.new_tag("div", attrs={"class": "project-subgroup-static"})
                    sh = soup.new_tag("h3", attrs={"class": "project-subgroup-heading"})
                    sh.string = sub_title
                    sub_block.append(sh)
                    if sub_body:
                        for c in list(sub_body.children):
                            sub_block.append(c.extract() if hasattr(c, "extract") else c)
                    sub.replace_with(sub_block)
        group.replace_with(block)

    flatten_project_previews(soup)


def skill_row_to_chip(soup: BeautifulSoup, row: Tag) -> Tag | None:
    badge = row.select_one("a.skill.badge, span.skill.badge, a.badge, .skill.badge")
    if not badge:
        return None
    skill = row.get("data-skill") or badge.get_text(strip=True)
    tier = row.get("data-tier") or ""
    li = soup.new_tag("li", attrs={"class": "domain-chip", "data-skill": skill})
    if tier:
        li["data-tier"] = tier
    # clone badge link
    chip = soup.new_tag(
        badge.name,
        attrs={k: v for k, v in badge.attrs.items() if k != "class"},
    )
    chip["class"] = ["domain-chip-link"]
    chip.string = badge.get_text(strip=True)
    li.append(chip)
    if tier:
        tip = soup.new_tag("span", attrs={"class": "domain-chip-tier"})
        tip.string = tier.replace("-", " ").title() if tier == "intermediate" else tier.title()
        if tier == "intermediate":
            tip.string = "Intermediate"
        if tier == "advanced":
            tip.string = "Advanced"
        li.append(tip)
    return li


def convert_competences(soup: BeautifulSoup, lang: str) -> None:
    section = find_section(soup, "competences" if lang == "en" else "compétences")
    if not section:
        section = find_section(soup, "competen")
    if not section:
        return
    set_section_id(section, "skills")
    body = section.select_one(".cv-section-body")
    if not body:
        return

    intro = body.find("p", class_="section-intro")
    if intro:
        intro.string = (
            "Domains from the competence map. Evidence counts come from roles and Selected projects on this page; credentials include verification links where available."
            if lang == "en"
            else "Domaines de la carte de compétences. Les preuves viennent des postes et des projets sélectionnés sur cette page; les certificats incluent des liens de vérification lorsque disponibles."
        )

    # Convert major skill groups to domain cards
    for major in list(body.select(":scope > details.skill-group.skill-group--major, :scope > details.skill-group--major")):
        domain = major.get("data-domain") or ""
        summary = major.find("summary", class_="skill-group-summary")
        title = summary.get_text(" ", strip=True) if summary else domain
        card = soup.new_tag(
            "article",
            attrs={"class": ["domain-card"], "data-domain": domain},
        )
        h = soup.new_tag("h3", attrs={"class": "domain-card-title"})
        h.string = title
        card.append(h)
        evidence = soup.new_tag(
            "p",
            attrs={"class": "domain-card-evidence", "data-domain-evidence": True},
        )
        evidence.string = ""
        card.append(evidence)

        # subgroups
        for sub in list(major.select("details.skill-subgroup")):
            sub_sum = sub.find("summary", class_="skill-subgroup-summary")
            sub_title = sub_sum.get_text(" ", strip=True) if sub_sum else ""
            group = soup.new_tag("div", attrs={"class": "domain-chip-group"})
            if sub_title:
                lab = soup.new_tag("p", attrs={"class": "domain-chip-group-label"})
                lab.string = sub_title
                group.append(lab)
            ul = soup.new_tag("ul", attrs={"class": "domain-chip-list", "role": "list"})
            for row in sub.select("li.skill-row"):
                chip = skill_row_to_chip(soup, row)
                if chip:
                    # localize Intermediate/Advanced for FR
                    tier_el = chip.select_one(".domain-chip-tier")
                    if tier_el and lang == "fr":
                        t = (chip.get("data-tier") or "").lower()
                        if t == "intermediate":
                            tier_el.string = "Intermédiaire"
                        elif t == "advanced":
                            tier_el.string = "Avancé"
                    ul.append(chip)
            group.append(ul)
            card.append(group)

        # also handle skill rows directly under major (no subgroup)
        direct_rows = [
            r
            for r in major.select("li.skill-row")
            if not r.find_parent("details", class_="skill-subgroup")
        ]
        if direct_rows:
            group = soup.new_tag("div", attrs={"class": "domain-chip-group"})
            ul = soup.new_tag("ul", attrs={"class": "domain-chip-list", "role": "list"})
            for row in direct_rows:
                chip = skill_row_to_chip(soup, row)
                if chip:
                    ul.append(chip)
            group.append(ul)
            card.append(group)

        major.replace_with(card)

    # Certifications: static block
    for cert in list(body.select("details.skill-group")):
        # skip if already converted
        if "skill-group--major" in (cert.get("class") or []):
            continue
        summary = cert.find("summary", class_="skill-group-summary")
        title = summary.get_text(" ", strip=True) if summary else (
            "Certifications" if lang == "en" else "Certifications"
        )
        block = soup.new_tag("div", attrs={"class": "domain-certs", "id": cert.get("id") or "certifications"})
        h = soup.new_tag("h3", attrs={"class": "domain-card-title"})
        h.string = title
        block.append(h)
        for child in list(cert.children):
            if isinstance(child, Tag) and child.name == "summary":
                continue
            if isinstance(child, Tag):
                block.append(child.extract())
        cert.replace_with(block)


def localize_chip_tiers_pass(soup: BeautifulSoup, lang: str) -> None:
    if lang != "fr":
        return
    for tip in soup.select(".domain-chip-tier"):
        t = tip.get_text(strip=True).lower()
        if t == "intermediate":
            tip.string = "Intermédiaire"
        elif t == "advanced":
            tip.string = "Avancé"


def process(path: Path, lang: str) -> None:
    soup = soup_file(path)

    # Section IDs
    set_section_id(find_section(soup, "work experience" if lang == "en" else "expérience"), "work")
    if not soup.select_one("#work"):
        set_section_id(find_section(soup, "expérience professionnelle"), "work")
    set_section_id(find_section(soup, "selected projects" if lang == "en" else "projets"), "projects")
    if not soup.select_one("#projects"):
        set_section_id(find_section(soup, "projets sélectionnés"), "projects")
    set_section_id(find_section(soup, "contact"), "contact")
    # skills set in convert_competences

    add_nav(soup, lang)
    flatten_courses(soup)
    flatten_projects(soup, lang)
    convert_competences(soup, lang)
    localize_chip_tiers_pass(soup, lang)

    # lxml wraps html; serialize without adding extra html/body if possible
    # Prefer pretty but keep doctype from original
    original = path.read_text(encoding="utf-8")
    doctype = ""
    if original.lstrip().lower().startswith("<!doctype"):
        doctype = original.split("\n", 1)[0] + "\n"

    html = soup.find("html")
    out = doctype + str(html) if html else doctype + str(soup)
    # BeautifulSoup may alter void tags; acceptable for this pass
    path.write_text(out, encoding="utf-8", newline="\n")
    print(f"Updated {path}")


def main() -> None:
    process(ROOT / "index-en.html", "en")
    process(ROOT / "index-fr.html", "fr")


if __name__ == "__main__":
    main()

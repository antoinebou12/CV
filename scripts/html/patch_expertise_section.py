"""Replace Competences skill charts with Technical Expertise markup on index-en/fr."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _gen_expertise_snippet import render  # noqa: E402

BOOT = """  <script>
    (function () {
      try {
        var key = 'cv-theme';
        var stored = localStorage.getItem(key);
        var dark = stored ? stored === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.classList.toggle('dark', dark);
        document.documentElement.dataset.theme = dark ? 'dark' : 'light';
        if (matchMedia('(prefers-reduced-motion: reduce)').matches || localStorage.getItem('cv-motion-paused') === 'true')
          document.documentElement.dataset.motion = 'paused';
      } catch (e) {}
    })();
  </script>"""

BOOT_RE = re.compile(
    r"  <script>\s*\(function \(\) \{[\s\S]*?dataset\.motion = 'paused';[\s\S]*?\}\)\(\);\s*</script>",
    re.M,
)

# Only inside the Competences / Compétences section, up to Certifications.
SECTION_RE = re.compile(
    r"(<!--\s*COMP(?:É|E)TENCES\s*-->\s*"
    r'<details class="box cv-section"[^>]*>\s*'
    r'<summary class="cv-section-summary">.*?</summary>\s*'
    r'<div class="cv-section-body">\s*)'
    r'<p class="section-intro">.*?</p>\s*'
    r"(?:<details class=\"skill-group skill-group--major\".*?</details>\s*)+"
    r"(?=<details class=\"skill-group\")",
    re.S,
)

CERT_RE = re.compile(
    r'<details class="skill-group">\s*'
    r'<summary class="skill-group-summary">Certifications</summary>',
)


def patch(path: Path, lang: str) -> None:
    text = path.read_text(encoding="utf-8")
    intro = (
        "Parcourez les domaines avec la recherche et les filtres. "
        "Les pastilles mènent à la doc ; une petite marque ouvre la certification liée lorsqu'elle existe."
        if lang == "fr"
        else "Browse domains with search and filters. "
        "Pills link to docs; a small mark opens the related credential when available."
    )
    expertise = render(lang)
    repl = "\\1" + f'<p class="section-intro">{intro}</p>\n' + expertise + "\n"
    new, n = SECTION_RE.subn(repl, text, count=1)
    if n != 1:
        raise SystemExit(f"Failed to patch majors in {path}: matches={n}")

    new2, cn = CERT_RE.subn(
        '<details class="skill-group" id="certifications">\n'
        '            <summary class="skill-group-summary">Certifications</summary>',
        new,
        count=1,
    )
    if cn != 1:
        raise SystemExit(f"Failed to id certifications in {path}: matches={cn}")
    new = new2

    if "cv-expertise.css" not in new:
        # Match whatever editorial cache-bust query is present.
        new, ln = re.subn(
            r'(<link rel="stylesheet" href="css/cv-editorial\.css[^"]*">)',
            r'\1\n  <link rel="stylesheet" href="css/cv-expertise.css?v=20261024a">',
            new,
            count=1,
        )
        if ln != 1:
            raise SystemExit(f"Failed to link expertise CSS in {path}")

    new, bn = BOOT_RE.subn(BOOT, new, count=1)
    if bn != 1:
        raise SystemExit(f"Failed to patch theme boot in {path}: matches={bn}")

    new = re.sub(
        r"js/cv-interactions\.js\?v=[^\"]+",
        "js/cv-interactions.js?v=20261024o",
        new,
        count=1,
    )
    path.write_text(new, encoding="utf-8", newline="\n")
    print(f"patched {path.relative_to(ROOT)} lines={len(new.splitlines())}")


def main() -> None:
    patch(ROOT / "index-en.html", "en")
    patch(ROOT / "index-fr.html", "fr")


if __name__ == "__main__":
    main()

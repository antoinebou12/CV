from pathlib import Path

for name in ("index-en.html", "index-fr.html"):
    t = Path(name).read_text(encoding="utf-8")
    print(
        name,
        "expertise=",
        t.count("data-expertise"),
        "cert=",
        'id="certifications"' in t,
        "css=",
        "cv-expertise.css" in t,
        "majors=",
        t.count("skill-group--major"),
        "title=",
        ("Expertise technique" in t) or ("Technical Expertise" in t),
    )

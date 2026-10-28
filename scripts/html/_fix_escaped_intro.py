from pathlib import Path

bad = 'class=\\"section-intro\\"'
good = 'class="section-intro"'
for name in ("index-en.html", "index-fr.html", "index.html"):
    path = Path(name)
    text = path.read_text(encoding="utf-8")
    if bad not in text:
        print(f"{name}: no bad intro")
        continue
    path.write_text(text.replace(bad, good), encoding="utf-8", newline="\n")
    print(f"{name}: fixed")

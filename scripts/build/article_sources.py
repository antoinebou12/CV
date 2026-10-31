"""Inventory article images/tags and index existing Markdown source links.

No publication dates or authors are guessed. Repository ownership comes from URLs;
other sources retain the linked title and an unknown date unless curated separately.
"""
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]


def sources(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    records = []
    seen = set()
    for label, url in re.findall(r"(?<!!)\[([^\]]+)\]\((https?://[^\s)]+)\)", text):
        parts = urlsplit(url)
        host = parts.hostname or ""
        if (url in seen or host in {"example.com", "yourwebsite.com", "projecturl.com"}
                or host.startswith(("img.", "cdn.")) or '/recent-activity/' in url):
            continue
        seen.add(url)
        author, kind = "", "Web page"
        if host == "github.com":
            path = parts.path.strip('/').split('/')
            if len(path) >= 2:
                author, kind = path[0], "Software repository" if len(path) == 2 else "Source file or documentation"
                if len(path) == 2:
                    label = path[1]
        elif 'linkedin.com' in host:
            kind = "LinkedIn post"
        elif host == 'medium.com':
            kind = "Article"
        records.append({"title": re.sub(r'[*`]', '', label), "url": url,
                        "author": author, "type": kind, "publisher": host})
    return records


def main():
    output = {}
    for path in sorted((ROOT / 'hugo/content/posts').glob('*/index*.md')):
        text = path.read_text(encoding='utf-8')
        records = sources(text.split('---', 2)[-1])
        if not records:
            records = [{"title": "Article manuscript and bundled media", "author": "antoinebou12",
                        "type": "Article source", "publisher": "github.com",
                        "url": "https://github.com/antoinebou12/CV/tree/main/hugo/content/posts/" + path.parent.name}]
        output[path.relative_to(ROOT / 'hugo/content').as_posix()] = records
    target = ROOT / 'hugo/data/article_sources.json'
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Indexed sources for {len(output)} article translations')


if __name__ == '__main__':
    main()

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
    notes = json.loads((ROOT / 'hugo/data/repository_notes.json').read_text(encoding='utf-8'))['notes']
    notes = {note['slug']: note for note in notes}
    articles = json.loads((ROOT / 'hugo/data/repository_article_index.json').read_text(encoding='utf-8'))['repositories']
    projects = {}
    for path in sorted((ROOT / 'hugo/content/projects/notes').glob('*/index*.md')):
        slug = path.parent.name
        note = notes.get(slug)
        records = []
        if note:
            owner = note['url'].removeprefix('https://github.com/').split('/')[0]
            records = [
                {'author': owner, 'title': note['repo'], 'type': 'Software repository', 'publisher': 'github.com', 'url': note['url']},
                {'author': owner, 'title': note['repo'] + ': README', 'type': 'Repository documentation', 'publisher': 'github.com', 'url': note['url'] + '#readme'},
            ]
            records += [{'author': owner, 'title': entry['path'], 'type': 'Source file', 'publisher': 'github.com', 'url': entry['url']} for entry in note['sources']]
            lang = 'fr' if path.name == 'index.fr.md' else 'en'
            for article in articles.get(note['repo'], []):
                if article['lang'] != lang:
                    continue
                article_path = ROOT / 'hugo/content' / article['path']
                date = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', article_path.read_text(encoding='utf-8'), re.M)
                records.append({'author': 'Boucher, A.', 'title': article['title'], 'type': 'Project article',
                                'publisher': 'antoineboucher.info', 'date': date[1] if date else '',
                                'url': 'https://antoineboucher.info/CV/blog/' + ('fr/' if lang == 'fr' else '') + article['path'].rsplit('/', 1)[0] + '/'})
        else:
            records = sources(path.read_text(encoding='utf-8').split('---', 2)[-1])
        projects[path.relative_to(ROOT / 'hugo/content').as_posix()] = records
    (ROOT / 'hugo/data/project_sources.json').write_text(json.dumps(projects, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Indexed sources for {len(projects)} project translations')


if __name__ == '__main__':
    main()

# Article template and source audit

The article template uses a numbered table of contents, numbered second-level
sections and third-level subsections, topic tags, and a references section.
Heading numbers come from Hugo's parsed heading tree and retain the original
anchors. The English and French URLs therefore remain valid.

`scripts/build/article_sources.py` indexes Markdown source links outside fenced
code blocks. It excludes image links, example domains, CDN assets, duplicate URLs
and generic LinkedIn activity feeds. Repository ownership is read from the URL.
Unverified authors stay unspecified and publication dates use `n.d.` / `s. d.`.
Entries use APA-style author/title/date ordering with numbered cross-references;
they are not a claim that complete bibliographic metadata has been verified.

Articles with no external publication link reference their manuscript and media
bundle in the CV repository. Do not replace these with guessed LinkedIn post URLs.
The local publication script refreshes this index before building `docs/`.

## Image audit

The inventory contains 57 articles in both languages (114 translations). Every
translation declares existing local images and topic tags. AINewsTracker now uses
its repository logo and original processing diagram. Snapchat uses its existing
Lens Insights screenshot, captioned as an earlier snapshot. Dimension, ipc-toolkit
and the Hugo redesign article now display their existing architecture figures in
the body instead of leaving those assets accessible only to listing cards.

AINewsTracker's collection path is described as a short explanation followed by a
responsibility/source-file table. The repository diagram is credited and linked.
No measured trading accuracy or returns are added.

## Browser regression suite

`article-paper.spec.ts` visits all 114 translations in light/mobile and dark/desktop
layouts, checking displayed images, tags, heading sequences, reference counts and
page overflow. Focused checks exercise French anchors, ordered-list markers and
AINewsTracker image loading, and save screenshots of the header and bibliography.
`article-reading.spec.ts` covers three widths, both languages and themes, command
copying, captions, contents disclosures and diagram-renderer failure recovery.

Screenshots and reports are generated under the ignored
`tools/ux-audit/e2e-results/paper-*` directories.

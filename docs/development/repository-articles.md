# Repository architecture notes

## Reader guides and diagram controls

`hugo/data/repository_guides.json` holds the bilingual first task for each repository and selected project links. `repository_api_guides.json` holds reviewed API examples and error behaviour. Keep code-specific claims linked to the pinned analysis and distinguish a listed website from a working deployment. A fork's homepage may belong to its upstream project.

After refreshing source analysis, run:

```powershell
uv run --python 3.13 scripts/build/repository_handbooks.py
# Rebuild without network calls:
uv run --python 3.13 scripts/build/repository_handbooks.py --offline
# Explicitly render changed public architecture diagrams using UML-MCP:
uv run --python 3.13 scripts/build/repository_handbooks.py --render
```

The handbook generator reads up to 24 README/setup/API/contribution documents per repository from the recorded commit, checks blob hashes and preserves source links. Published excerpts retain the source language. Each repository gets only the guide categories found in its documentation. Missing sections, capped coverage and failed reads are not evidence of a complete operational manual. Installation commands remain untested source excerpts; no five-minute success promise is made.

The explicit render option sends only the public, curated Mermaid topology to `https://uml-mcp.vercel.app/mcp`, using `generate_uml`. Successful replies retain render and playground URLs plus a hash of the source. Normal builds reuse those results, invalidate changed diagram sources and make no rendering calls. Each published diagram starts with a local rendered image. The browser progressively replaces that image with strict Mermaid rendering and keyboard-operable zoom, fit and SVG export controls. If Mermaid or its CDN is unavailable, the local image remains visible. Visitors do not call MCP services automatically. Videos remain excluded.

Related articles and legacy project pages link to their repository guides through the article index. Preserve their narrative, images and original URLs.

Generated-page HTML validation allows explicit `role="list"`. The language and
download lists have CSS `list-style: none`; the explicit role preserves list
semantics in Safari and VoiceOver.

The projects directory links every public repository in `hugo/data/github_inventory.json` to a bilingual local note under `hugo/content/projects/notes/`. Existing project pages retain their original URLs and content.

## Automatic source documentation

```powershell
uv run --python 3.13 scripts/build/repository_docs.py
# Rebuild from cached inputs without contacting GitHub or GitDiagram:
uv run --python 3.13 scripts/build/repository_docs.py --offline
# Refresh one repository or newly created external exports:
uv run --python 3.13 scripts/build/repository_docs.py --repo uml-mcp
uv run --python 3.13 scripts/build/repository_docs.py --repo bloc --gitdiagram-only
```

The generator uses the existing GitHub CLI login (`gh`) and refuses private repositories. It resolves each default branch to a commit, reads its recursive tree, fetches public text blobs and checks their Git blob hashes. Source code is parsed, never imported or executed. Known dependency/build folders, symlinks, credential filenames and binary assets are excluded. The default reads every eligible file up to four megabytes; `--max-files` is an explicit optional cap. The published coverage includes skipped files, read failures and syntax diagnostics. A truncated GitHub tree is reported as incomplete.

Python 3.13, `tree-sitter-language-pack==0.13.0` and `tree-sitter==0.25.2` are pinned for the tested parser/runtime combination. A newer binding crashed on Windows during validation. This exception is limited to this documentation generator; it does not change the CV build runtime.

Generated outputs:

- `hugo/data/repository_analysis.json`: Linguist language bytes, commit references, README commands, manifest tasks, parsed type definitions and external-export status.
- `hugo/data/repository_article_index.json`: links between inventoried repositories and the local Markdown articles that reference them.
- `hugo/static/repository-docs/<slug>/`: JSON analysis, file maps, per-file class diagrams and original GitDiagram Mermaid exports when available.
- `_site/repository-docs-cache/`: ignored source snapshots and external-service responses for reproducible offline regeneration.

Language percentages are calculated from [GitHub's repository-languages endpoint](https://docs.github.com/en/rest/repos/repos#list-repository-languages), not from filename counts. Those statistics reflect GitHub Linguist's classification; the source-analysis file filter is a separate documented filter.

Class diagrams show declared types and method names. C/C++ type references do not create new definitions. Generic arguments are not extra base classes. Known interface realizations use a dotted UML arrow; unresolved base declarations remain labelled. The overview is intentionally small, while the JSON export and per-file Mermaid downloads retain the extracted definitions. File maps show membership only, not inferred imports or calls.

README shell blocks keep their source file, heading and line number. Credential assignments and remote pipe-to-shell recipes are omitted. The generator never tests an installation or runs manifest scripts. Review the original instructions before using commands from an archived or hardware-specific project.

GitDiagram imports use its public, read-only [MCP service](https://github.com/ahmedkhaleel2004/gitdiagram) as an analysis input. GitDiagram branding, controls and outbound diagram embeds are not published. Original Mermaid exports are preserved as build evidence. Preview copies drop click and style directives, switch tall top-to-bottom graphs to a horizontal layout, and use the site's strict renderer. Linked paths are checked against the recorded tree; missing paths flag an export for review instead of replacing the curated architecture. Path checks do not verify generated behavioural claims.

`scripts/build/render_repository_diagram_images.py` creates the local image fallback for each English and French overview. Repositories with a validated GitDiagram export also receive a system image. Type and file diagrams are added when source analysis finds those structures. The image manifest lives in `hugo/data/repository_diagram_images.json`; generated pages must contain both the local image and the Mermaid source so the same page works with or without client-side rendering.

Video imports and generation are excluded from this workflow. No payment or credential is stored by this site.

The **Repository documentation** GitHub workflow tests pull requests touching the generator. Its manual dispatch refreshes the public inputs and uploads the results as an artifact. It does not automatically commit, push, publish, create new videos or purchase anything.

```powershell
uv run --python 3.13 --with pytest --with tree-sitter-language-pack==0.13.0 --with tree-sitter==0.25.2 pytest scripts/tests/test_repository_docs.py -q
```

## Technical dossier per project

```powershell
uv run --python 3.13 scripts/build/repository_dossier.py --offline
# Also fetch small build/CI/deploy files the source scan skips (Dockerfile, *.csproj, workflows, compose):
uv run --python 3.13 scripts/build/repository_dossier.py --repo uml-mcp
```

Run it after `repository_docs.py`. It reads the cached, hash-checked snapshot and the GitDiagram export, then writes `hugo/data/repository_dossiers.json`. `repository-dossier.html` renders it on every project note under **Technical dossier / Dossier technique** with these sections: layers and modules, data flow, public interface, private interface, services and hosting, entities, business logic, database, external integrations, stack and dependencies, security and tests. Sections without evidence are omitted and listed once at the end.

The script also writes the Mermaid sources for five diagrams: the layered view, a sequence diagram of the GitDiagram calls in walk order, a route map grouped by path prefix, an entity class diagram whose arrows follow field types, and a system context diagram with callers on the left and dependencies on the right. Labels that the page translates are stored as `[en, fr]` pairs.

To avoid repeating other sections, the dossier leaves out languages (language panel), Compose services when the Deployment table lists them, MCP tool chips when an MCP tool contract exists, and Docker base images under Stack. Notes that have a dossier also skip the type index and file map in the Reference section.

Everything is pattern-based and read as text. Layers come from folder and file names, so they show where code sits and do not trace imports. Data flow only appears when GitDiagram has a path-checked export, because the Architecture section already draws the curated nodes. Security lists environment variable names only. Tighten a pattern in the script rather than hand-editing the JSON.

```powershell
uv run --no-project --python 3.13 --with pytest python -m pytest scripts/tests/test_repository_dossier.py -q
```

### UML diagrams through uml-mcp

```powershell
uv run --python 3.13 scripts/build/repository_uml.py
# Reuse stored SVG files only:
uv run --python 3.13 scripts/build/repository_uml.py --offline
```

Run it after `repository_dossier.py`. It writes PlantUML for up to four diagrams per project (use cases, components and interfaces, deployment, CI pipeline activity) in English and French, sends each source to the public uml-mcp REST endpoint (`/generate_diagram`, which encodes it for Kroki), and only accepts an SVG URL on kroki.io. Scripts, event handlers, `foreignObject`, comments and the embedded PlantUML source are stripped before the file is stored under `hugo/static/repository-docs/<slug>/uml/`, named by a hash of its source, so unchanged diagrams are not requested again. `hugo/data/repository_uml.json` lists the files and their sources.

Each diagram sits in the dossier section it explains. The component diagram replaces the Mermaid system context when both exist. `mermaid.html` inlines the SVG (ids prefixed, handlers removed again) into the same zoom, fit, fullscreen and export viewer as Mermaid; the `<img>` stays as the no-script fallback. PlantUML colours are fixed, so dark mode inverts them with a CSS filter.

## Curated architecture prose

Edit the prose, components, diagram nodes and connections in `hugo/data/repository_notes.json`. Each bilingual pair stores English first and French second. Component entries contain English and French headings followed by English and French paragraphs. Source records retain the inspected file's GitHub blob hash and a readable file link. The hash records the review evidence; the branch link opens the current source and can change later.

`repository-note.html` renders the article body. The shared `repository-diagram.html` partial builds Mermaid from explicit nodes and edges and provides a text alternative. Diagrams use the site palette, update when the reader changes theme, and retain their source when the renderer is unavailable. Diagram text is public; Mermaid is loaded from a versioned CDN.

Fork and archive labels come from the public inventory. Do not infer authorship, upstream acceptance, working hardware or performance from a repository's presence. Configuration repositories can describe a setup workflow instead of pretending to be an application.

Mermaid uses the root-level [htmlLabels setting](https://mermaid.js.org/config/schema-docs/config-properties-htmllabels.html) to render SVG text without HTML paragraphs. This avoids article paragraph margins clipping the labels inside SVG foreign objects.

After editing, build Hugo and run:

```powershell
node --test scripts/verify/repository-notes.test.mjs
```

To check a production build in `docs/blog`:

```powershell
$env:CV_NOTES_SITE = 'docs/blog'
node --test scripts/verify/repository-notes.test.mjs
Remove-Item Env:CV_NOTES_SITE
```

The checks require one note per inventoried public repository, English/French parity, connected diagram nodes, source evidence, working local card destinations and search entries. Validate generated HTML with `.htmlvalidate-generated.json`; it permits Hugo's valid unquoted attributes and lowercase doctype while retaining the other HTML checks. Also inspect rendered diagrams in a browser at desktop and mobile widths. On narrow screens the diagram scrolls horizontally to preserve legible labels, with a focusable container and text alternative. A static build test cannot establish rendering quality or current remote-project compatibility.

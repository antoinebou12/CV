# Project use cases

Every project page has a **Use cases** section after the overview: a one-line summary, a
use-case diagram, the same use cases as text, one end-to-end scenario and the files read.
The catalog card shows the one-line summary, and the Markdown brief (`…/index.md`,
`llms-full.txt`) lists the use cases and scenario.

## Data

`hugo/data/project_use_cases.json` → `repositories.<RepoName>`:

| Field | Content |
|-------|---------|
| `summary` | `[English, French]`, at most 140 characters each |
| `actors` | 1–3 items: `id`, `kind` (`person` drawn left, `system` drawn right), `label` `[en, fr]` ≤ 24 characters |
| `use_cases` | 3–6 items: `id`, `actors` (actor ids), `label` `[en, fr]` ≤ 32 characters, optional `detail` `[en, fr]`, `evidence` paths |
| `scenario` | `title` `[en, fr]` and 3–6 `steps`, each `[en, fr]` (plain text, so commands such as `--install` keep their dashes) |
| `evidence` | repository-relative paths that were read |

Facts come from the repository's README and source; nothing is inferred from the name.

## Updating

Write one `RepoName.json` per repository in a folder, then merge and validate:

```bash
python scripts/build/merge_use_cases.py path/to/folder
python scripts/build/merge_use_cases.py --check
```

The diagram is inline SVG drawn by `hugo/layouts/partials/repository-use-cases.html` with the
note colour tokens, so it follows light and dark mode and needs no JavaScript or external
renderer. Label limits keep the text inside the ovals and actor columns.

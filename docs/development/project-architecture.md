# Project architecture views

`scripts/build/repository_uml.py` renders bilingual diagrams through uml-mcp and
stores sanitized SVG files locally. Each project dossier presents four C4 levels:

1. System context: known callers, external integrations and stores.
2. Containers: Compose services or an application with entry-point or hosting evidence.
3. Components: source modules grouped within their classified layers.
4. Code: selected declarations and functions grouped by source file.

The component view describes source organization. Layer classification alone does
not establish a runtime boundary. Code views do not infer inheritance or calls
from names. Where evidence does not support a view, the page explains the gap.

Technology and testing badges link to dossier sections. Dependency badges link to
the source manifest and retain its version constraints. Framework detection lists
all matches; source scans may not cover every file in the upstream repository.

Coverage configuration identifies tooling. Measured percentages require a cached
coverage.py or Istanbul JSON report, Cobertura XML line totals, or LCOV line totals.
Thresholds and test-file counts never become coverage percentages. Results link
to the report at the analyzed commit.

Regenerate dossiers before diagrams, then build the site locally:

```text
python scripts/build/repository_dossier.py --offline
python scripts/build/repository_uml.py
python scripts/deploy/publish_site.py
```

The Mitsuba article uses existing report illustrations with captions identifying
their purpose. It documents the batch OBJ renderer separately from the simulation
recording helper and links to both source workflows.

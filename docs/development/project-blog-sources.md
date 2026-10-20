# Project article sources — October 20, 2026

Six bilingual articles were added for Artemis Switch, the Switch/New 3DS CoopDX
port, ComfyUI-UML, Serilog.Sinks.SentrySDK, Workshop1, and BatchBacktesting.
The existing UML-MCP and vector-search articles were expanded.

Repository creation dates, stars, forks, and inspected revisions are recorded in
`hugo/data/project_repositories.json`. Creation dates describe repositories, not
the start of upstream projects. New article dates describe publication; existing
articles retain their publication dates and update `lastmod`.

## Original media

- UML-MCP: `docs/assets/diagrams/client-server-chat.png` in antoinebou12/uml-mcp.
- Artemis: README attachment `8d5c5659-5331-451d-8690-ddab305036ab`.
- ComfyUI-UML: README attachment `c9fc5efa-ebd5-47ea-b5ab-86ac03dd92b5`.
- Serilog: `src/assets/serilog-sink-nuget.png` in antoinebou12/Serilog.Sinks.SentrySDK.
- Workshop1: `images/algoets.png` in AlgoETS/Workshop1.
- Vector-search GIFs: README attachments `2bd8ae0c-1b24-4774-865d-244b58a4f362`,
  `1f9a2fa3-b195-4f2d-bb38-eb4a218e2eaf`, and
  `e688a0dd-61e3-493e-aee1-b582f313c182`.
- BatchBacktesting: reused local `multiple-indicators-backtesting/img-001.png`,
  explicitly labeled as an existing illustration, not a new simulation.

All media are bundled beside the articles so rendering does not depend on GitHub
attachment requests. Mermaid diagrams summarize inspected code and retain their
source in expandable details. The shared partial also activates rendering for
older posts containing Mermaid fences without a front-matter flag.

## Scope of evidence

Articles link the inspected implementation and describe limitations explicitly.
No console gameplay, financial simulations, library tests, coverage percentages,
or new latency benchmarks are claimed. The New 3DS README and detailed port notes
give different levels of release/validation status; the article preserves that
distinction. NuGet's live download badge is distinct from dated GitHub statistics.

## Visitor map

The old JavaScript widget could leave its placeholder forever. The replacement
requests a ClustrMaps map image only after expansion, has load/error handling, a
10-second deadline, retry, and a direct provider link in both languages. Provider
requests failed from the verification environment; the unavailable state was
verified in-browser. Provider availability remains external to the site.

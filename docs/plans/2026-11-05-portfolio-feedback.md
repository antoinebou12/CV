# Portfolio feedback plan (2026-11-05)

Feedback from the review of antoineboucher.info on 2026-11-05, turned into one task per item.
Work happens on branch `claude/portfolio-feedback-20261105` (worktree `D:/Code/cv-feedback`), cut from `origin/main` at `eb7b5148`.

Status legend: `[x]` done on the branch, `[ ]` to do.

## How the project notes are built

Knowing this decides where each fix goes.

- **Note text** is hand-written Markdown in `hugo/content/projects/notes/<slug>/index.md` and `index.fr.md` (62 notes, EN/FR pairs).
- **Generated sections** come from JSON in `hugo/data/`, rendered by `hugo/layouts/_default/single.html` and the `repository-*` partials:
  - `repository_dossiers.json` drives the dossier (layers, modules, deployment, delivery pipelines, tests). Written by `scripts/build/repository_dossier.py`.
  - `repository_analysis.json` and `repository_diagram_images.json` drive the architecture and layered diagrams. Written by `scripts/build/repository_docs.py` and `render_repository_diagram_images.py`.
  - `repository_uml.json` drives the UML figures, including a deployment figure. Written by `scripts/build/repository_uml.py`.
  - `project_sources.json` drives the reference list. Written by `scripts/build/article_sources.py`.
- **Coverage gap.** 21 notes have no dossier at all: ainewstracker, batchbacktesting, bullets, hass-renpho, kelly-rm, legostracker, markokchainmontecarlo, mistubavideo, polyfemblenderplugin, salary, serilog-sinks-sentrysdk, similityvectorembedding, simulateur, sport-arbitrage, tradingviewbuilder, truemapdata, wearblender, wearmachine, wearsurfacesdatasets, weartrailsexperiments, workshop1. Several items below need a dossier for these first.
- **Deploy** rebuilds the blog from `hugo/` on every push to `main` (`.github/workflows/deploy.yml`). `docs/blog/` is a committed mirror and is not what gets published.

## Group A: site-wide fixes (shared templates, do first)

- [x] **A1. Replace every "(n.d.)" with a date.**
  - Found: 704 of 868 project-note references have no date, and `project-paper-references.html` printed "(n.d.)" / "(s. d.)" for them. Two AINewsTracker figure captions and the AI figurines post also had it.
  - Done: the partial now prints the `referencesChecked` date from `hugo/hugo.toml` (2026-11-05) as "(2026, November 5)" / "(2026, 5 novembre)". Dated sources use the same APA format. The note under the list now says undated sources show the date they were checked. Post captions fixed by hand. The AI figurines post was already pushed to `main` as `eb7b5148`.
  - Later: bump `referencesChecked` whenever references are re-verified.
- [x] **A2. Page loading animation.**
  - Ask: show a loading animation while a page loads.
  - Plan: a thin top progress bar plus a fade-in for the project-paper shell, in `hugo/layouts/partials/` and the site CSS. Keep it CSS-first, remove it on `DOMContentLoaded`, and skip it when `prefers-reduced-motion: reduce`. Add a spinner on Mermaid figures until they render, since those are the slow part.
  - Done when: a throttled load in Playwright shows the bar, and it never blocks content when JavaScript is off.
  - Done: `head.html` marks `html.page-loaded` on the window `load` event; `baseof.html` ships a `.page-load` bar that `motion.css` grows while loading and fades once loaded (hidden without JavaScript, under reduced motion and in print, and it hides itself after 12 s if `load` never fires). Project-note shells settle in from 35% opacity. Mermaid figures keep their spinner while rendering and stop it when rendering fails. Checked in Playwright with images delayed 2.5 s: the bar is visible at 55% during load, transparent after; with JavaScript off it never displays.
- [x] **A3. Project catalog card spacing** (screenshot 4).
  - Found: cards in one row stretch to the tallest card, leaving large empty areas under short cards (PolyFEMBlenderPlugin, AudioTranscript) and around the Serilog and TrueMapData cards.
  - Plan: pin "Updated" to the card bottom and drop the forced row height, or move to a masonry-style column layout. Check with `tools/ux-audit/e2e/project-polish.spec.ts`.
  - Done: the catalog grid is now balanced CSS columns (2, 3 from 1600 px, 1 on phones) in `projects-directory.css`, so each card keeps its own height and no empty block sits under short cards. Card cover images on phones stay inside the card border.
- [x] **A4. Diagram summary stats box** (screenshot 5).
  - Found: "Links supported by code or README 11/13" wraps and sits lower than "Components 17" and "Connections 13".
  - Plan: shorten the label to "Evidence-backed links" / "Liens appuyés par le code", and align all three values on one baseline in the stats grid CSS.
  - Done: label is now "Evidence-backed links" / "Liens appuyés par le code"; each stats cell is a flex column with the value pinned to the bottom, so the three values share one baseline even when a label wraps.
- [x] **A5. Layered view for this CV repository** (screenshot 6).
  - Found: the layer diagram counts `docs/blog` (1,120 built files) as source, shows `docs/blog` twice, and folds the rest into "+11".
  - Plan: exclude build output (`docs/blog`, `_site`, minified CSS, generated JSON mirrors) in `scripts/build/repository_dossier.py`, and show real source folders (`hugo/layouts`, `scripts/build`, `cv-en/latex`, `css`, `js`).
  - Done: `repository_dossier.py` drops build output before building any section: `_site`, `node_modules`, `vendor`, `dist`, coverage, `.min.js`/`.min.css`/`.map`, root `build`/`out`/`target`/`obj`, Hugo `public`/`resources`, and site files committed under `docs/` (HTML, XML, JS, CSS, JSON). LaTeX (`.tex`, `.cls`) now counts as source. The CV layer view went from 1,350 to 209 files and shows `hugo/layouts`, `css`, `scripts/build`, `scripts/verify`, `cv-en/latex`, `cv-fr/latex`; Kubernetes evidence now points at `helm/` instead of a built tag page. Vendored libraries also left ComfyUI-UML, WordsEnigma, linkshare and Serilog.Sinks.SentrySDK.
- [x] **A6. Architecture diagram readability** (screenshot 3, AINewsTracker).
  - Found: about 40 edges cross the whole canvas because every route links straight to every model and repository.
  - Plan: in the diagram generator, collapse "route uses model" edges into one edge per layer, cap edges per node, and draw routes, services, models and storage as left-to-right lanes. Keep the full graph in the text version.
  - Done: `repository_dossier.py` adds an `architecture` entry per dossier: GitDiagram edges between the same two groups (3 or more) become one edge, a node fanning out to one group or a group fanning in to one node does too, self-loops go, crossing edges are capped at 4 per node, and groups are ordered as left-to-right lanes (clients, entry points, services, domain, data). `repository-diagram.html` draws that overview and its text version now lists every original edge with "shows N of M". `render_repository_diagram_images.py` renders the same overview for the static preview; 12 repos changed (bloc 19 to 10 edges, Dimension 17 to 8, uml-mcp 21 to 16). The AINewsTracker note itself already used a hand-condensed 11-edge diagram; it gets the generated views through A7.
- [x] **A7. CI/CD pipeline and deployment diagram for every project.**
  - Ask: show the CI/CD pipeline and a deployment diagram on each project, with details when a pipeline exists.
  - Found: dossiers already list `deployment.pipelines` and tests workflows as text, and a UML deployment figure exists for some repos. 21 notes have no dossier.
  - Plan: in `repository_dossier.py`, parse `.github/workflows/*.yml` (triggers, jobs, `needs`, deploy targets) into a Mermaid flowchart, and add a deployment diagram from Dockerfiles, compose services and hosting targets. Render both in `repository-dossier.html`. For repos with no pipeline, state "No CI/CD pipeline in the repository" instead of hiding the section. Generate dossiers for the 21 missing notes first.
  - Done: `repository_docs.py` and `repository_dossier.py` now also read the 19 AlgoETS and ETSim repositories from `project_org_repositories.json` (owner per repository instead of a hard-coded `antoinebou12`), so all 65 notes have an analysis and a dossier (the 21 counted earlier included two notes whose dossier existed; 19 were really missing). The dossier gains `ci` (each `.github/workflows/*.yml` read line by line: triggers, jobs, `needs`, runner, steps, publish targets per job, plus GitLab/Azure/Travis/Jenkins/CircleCI files by name) with a Mermaid pipeline flow, and `deployment.mermaid` (repository, GitHub Actions, Docker image with its base, publish targets, configured hosts, Compose services, or "Local machine" when nothing deploys). Generated notes show a "CI/CD pipeline" part and the deployment diagram in their dossier; hand-written notes get "CI/CD pipeline" and "Deployment diagram" sections before the glossary (`repository-paper-delivery.html`). Repositories without workflows say "No CI/CD pipeline in the repository" (35 of 65). On phones the workflow table stacks. Also fixed: Mermaid subgraph titles were clipped on every diagram (prose margin on the `<p>` inside the label), and `.codex/config.toml` no longer counts as a static-site config. `scripts/verify/repository-notes.test.mjs` checks every note in both languages.
- [x] **A8. External libraries and dependencies on every project.**
  - Ask (from springbootfilesuploader): check the structure and list external libraries and dependencies on all notes.
  - Plan: read manifests already captured in `repository_analysis.json` (`manifests`) and render a dependency table (name, version, purpose, link to registry) per note. Re-check the springbootfilesuploader structure against the repo's `pom.xml` / `build.gradle` and source tree.
  - Done: `build_dependencies` lists every declared package from pyproject, requirements, package.json, Cargo, composer, Gemfile, Gradle, Maven, .csproj, go.mod, CMake and PlatformIO manifests: name, version, runtime or development, purpose, and a link to its registry (PyPI, npm, crates.io, Packagist, RubyGems, NuGet, pkg.go.dev, Maven Central). Purpose is a bilingual category for known kinds of package (web framework, testing, data access, charts, ML…), otherwise the registry's one-line summary, marked `lang="en"` on French pages. Generated notes show the table under "Stack and dependencies"; hand-written notes get an "External dependencies" section, which says so when the repository has no manifest. Tables over 20 rows start collapsed. SpringBootFilesUploader shows 26 packages from `build.gradle.kts`; correcting its described structure stays with C8.
- [x] **A9. Remove notes for repositories with no commits by the user.**
  - Plan: for each repo in `hugo/data/project_repositories.json` and `project_org_repositories.json`, query the GitHub commits API with `author=antoinebou12`. List repos with zero commits, confirm the list with the user, then remove their notes (EN and FR), data entries and catalog cards.
  - Needs a decision: forks where the user's work is in an upstream pull request (for example bloc) count as contributions only if the PR exists.
  - List (2026-11-06, GitHub commits API with `author=antoinebou12` on every branch, plus contributors and pull-request search). Nothing removed yet; waiting for confirmation.
    - No commits, no pull requests, nothing on any branch: `NX-Activity-Log` (fork of tallbl0nde/NX-Activity-Log), `donneesqc-mcp` (fork of Stefen-Taime/donneesqc-mcp), `BullETS` (AlgoETS, not a fork; not a listed contributor).
    - Work only on a side branch plus an upstream pull request: `ChitUI` (5+ commits on branch `changes`, open upstream PR jangrewe/ChitUI#5) and `hydra` (1 commit on `agent/better-menu-controller-support`, upstream PRs hydralauncher/hydra#2690 open and #2689 closed). Keep them under the rule above unless the user says otherwise.
    - Every other note repository has at least one commit by antoinebou12 on its default branch (bloc 10, nova-backtest 3, jsonresume-theme-kendall 1, Dimension 1).
  - Done (2026-11-06, user's choice): removed `BullETS` and `NX-Activity-Log`, keeping `donneesqc-mcp`, `ChitUI` and `hydra`. Both notes (EN and FR) and their `repository-docs` exports are gone, along with their entries in `github_inventory.json`, `project_org_repositories.json`, `competence_domains` (YAML and JSON), `repository_handbooks.py` and every generated data file, so the catalog drops from 65 to 63 repositories. Nothing linked to either note.
- [x] **A10. Interactive skill map** (screenshot 2).
  - Found: nodes overlap and are clipped at the edges ("Cloud and", "Backend and APIs" over ".NET", "Graphics and 3D" over "CUDA"). The component is not in this repository; it is most likely the JSON Resume rendering of `resume.json`. Confirm where it is served.
  - Plan: rebuild it as a SkillSet-style radial tree (https://jac21.github.io/SkillSet/) fed from `data/cv.yaml`, with categories as the inner ring and skills as leaves, labels that never overlap, and EN/FR parity. Use the `playwright-audit-fix` skill to verify both themes and phone width.
  - Where it was served: not found. Nothing in this repository, the live CV or the blog draws it, and registry.jsonresume.org has no profile for antoinebou12. Its labels ("Cloud and platform", "Backend and APIs", "Graphics and 3D") are the `skills` names in `resume.json`, so it is a third-party JSON Resume viewer. Still to confirm with the user.
  - Done: new page `/blog/skills/` and `/blog/fr/skills/` ("Skill map" / "Carte des compétences"). `scripts/build/generate_cv.py` writes `hugo/data/skill_tree.json` from the same `skill_groups` as the PDF Competences row (7 categories, 35 skills plus certifications, intermediate skills marked), and `--check` in CI now covers it. The `skill-map` shortcode draws a dependency-free SVG radial tree (`assets/skill-map.js`, `skill-map.css`): every visible skill gets an equal angular slot so leaf labels cannot collide, labels run along the radius and flip on the left half, the canvas is fitted to the measured labels so nothing is clipped, categories fold on click or Enter/Space, and a text version lists everything (also the no-JavaScript view). On phones the stage scrolls sideways at a readable size and opens centred. Checked in Playwright: light and dark, 1280 and 390 px, fold/unfold by mouse and keyboard, no-JS list. The script is not minified because Hugo's minifier turned a block-scoped variable into a "Cannot access before initialization" error.
  - Not done: no link to the page yet from the CV or blog navigation, pending where the old map was linked from.

## Group B: articles

- [ ] **B1. Reverse proxy article hero image** (screenshot 1).
  - Found: `hugo/content/posts/reverse-proxy-infrastructure/images/featured.png` is an unrelated 3D room render.
  - Plan: replace it with an image of the actual setup, such as the article's Terraform, Ansible and health-check flow rendered as a figure. Update `images:` in both EN and FR front matter.
- [ ] **B2. Medium articles.** All eight are already mirrored in `hugo/content/posts/` by `tools/medium-mirror`. One review task each: images present, code blocks intact, canonical link to Medium, FR version where one exists, tags.
  - [ ] Predicting Stock Prices with Monte Carlo Simulations (`predicting-stock-prices-monte-carlo`)
  - [ ] A Method to Install Python Packages for Add-ons & Plugins in Blender (`blender-python-packages`)
  - [ ] Economics of LEGO Sets with Data Science (`economics-lego-data-science`)
  - [ ] Multiple Technical Indicators Backtesting on Multiple Tickers (`multiple-indicators-backtesting`)
  - [ ] Using Vector Databases to Find Similar Movies, Part 1 (`vector-databases-similar-movies`)
  - [ ] A Journey to AWS Certified Cloud Practitioner (`aws-certified-cloud-practitioner`)
  - [ ] Making Caddy, AWS EC2, CloudWatch, Step Functions, and Lambda Work Together (`caddy-ec2-cloudwatch-lambda`)
  - [ ] Expérimentation des indicateurs techniques avec Python et Backtesting (`experimentation-indicateurs-backtesting`)
- [ ] **B3. Shadertoy posts.** One post per shader, EN and FR, each with the embedded shader, the GLSL source walked through step by step, and the math behind it. Fetch the source with the Shadertoy API (shaders are `public + api`).
  - [ ] Domain Wrapping, https://www.shadertoy.com/view/43f3z2 (2024-01-23)
  - [ ] Golden number spiral, https://www.shadertoy.com/view/lcjSR1 (2024-02-11)
  - [ ] Grid Line, https://www.shadertoy.com/view/43X3z2 (2024-02-11)
  - [ ] Sea and Stars, https://www.shadertoy.com/view/lcjXzh (2024-01-23)
  - [ ] Sun Ray Clockwise, https://www.shadertoy.com/view/X3f3z2 (2024-02-11)
  - [ ] Warping Mouse, https://www.shadertoy.com/view/McjSz1 (2024-01-23)
  - The URL-to-title pairing above follows the order given in the feedback. Confirm it against each shader's title when fetching.
- [ ] **B4. Salary results post.** See C4.

## Group C: individual project notes

Each task edits only that note's `index.md` and `index.fr.md`, plus its data entries.

- [ ] **C1. simulateur.** Improve the page from the code: the price engine noise models with a short explanation of each, the simulation lifecycle as a state diagram, the WebSocket flow, and screenshots from the repository.
- [ ] **C2. similityvectorembedding.** Explain the pipeline from the code (embedding model, pgvector schema, similarity query, ranking) and add images from the repo and the related Medium article.
- [ ] **C3. tch099.** Improve from the hosted documentation site: what the course project does, its architecture and the team workflow.
- [ ] **C4. salary.** Add the analysis results (charts and key numbers) to the note, and write a blog post about the results that links back to the note.
- [ ] **C5. wearmachine.** Add the images from the GitHub repo and an interactive 3D/CAD view of the machine with the existing `{{< modelviewer >}}` shortcode (convert STEP/STL to GLB).
- [ ] **C6. uml-mcp.** Add a demo video and images. Reuse the existing flow SVG and add a screen recording of Cursor generating a diagram.
- [ ] **C7. truemapdata.** Add the PyPI link (and NuGet if a .NET package exists), the install command, and a short usage example taken from the README and tests.
- [ ] **C8. springbootfilesuploader.** Verify the described structure against the code and correct it. Add the dependency table from A8.
- [ ] **C9. sport-arbitrage.** Explain the arbitrage algorithm: implied probability, the arbitrage condition, stake sizing, with a worked example and a flow diagram. Apply the same depth to the other algorithm repos (markokchainmontecarlo, batchbacktesting, nova-backtest, kelly-rm).
- [ ] **C10. mediaboxdockercompose** (project page `projects/mediaboxdockercompose/`). Explain what the code does service by service: what each container is for, how they connect, volumes, networks and the install script.

## Suggested order

1. Group A templates and generators (A2 to A8), because C tasks render through them.
2. A9 after the user confirms the list of repos to remove.
3. Group C notes, one at a time.
4. Group B posts, independent of everything else.
5. Run `scripts/ci/run-tests.ps1`, the Playwright audit, and a full Hugo build before pushing to `main`.

# Evaluation

## Hard gates

An experiment fails if any item below fails:

- Hugo and production builds complete without errors.
- Repository documentation tests and English/French parity pass.
- The page has one visible `h1` and the required project section order.
- No page-level horizontal overflow at 390, 768, or 1440 pixels.
- No visible text uses transparent color, zero opacity, or foreground/background contrast below 4.5:1 for normal text.
- Keyboard users can reach search, filters, tabs, disclosures, diagram controls, and links with a visible focus indicator.
- Theme, language, filtering, installation tabs, and diagram controls work without console errors.
- Reduced motion removes nonessential movement.
- Diagram labels are readable at their initial 100 percent scale.

## Fixed score

Score retained experiments out of 100:

| Area | Points | Evidence |
| --- | ---: | --- |
| Factual accuracy and source evidence | 25 | claims, source paths, generated-data checks |
| Structure and discoverability | 20 | section order, search, filters, TOC |
| Diagram comprehension | 20 | label size, node count, controls, text alternative |
| Accessibility and responsiveness | 15 | contrast, keyboard, zoom, overflow, themes |
| Task completion | 10 | requested surfaces and project types |
| Performance and maintainability | 10 | asset size, console, CSS reuse, build time |

Do not award points from visual impression alone. Record the check or measurement used.

## Browser capture matrix

For each required URL, capture:

- 390 x 844, light and dark
- 768 x 1024, light and dark
- 1440 x 1000, light and dark

Keep the same viewport, theme, scroll target, and seeded state for before and after images.

## Interaction checks

- Search for a repository by name and technology.
- Filter by primary language and project style, then reset.
- Switch Native and Docker installation tabs when both exist.
- Switch architecture views.
- Open the Mermaid view and use Zoom in, Zoom out, Fit, 100%, Fullscreen, and Export SVG.
- Change language and verify the corresponding translated route.
- Traverse the changed region with Tab and Shift+Tab.

## Experiment log entry

```markdown
## Experiment N: concise name

Hypothesis: Changing X should improve Y, measured by Z.

Files: `path`, `path`

Before: measurable defect and screenshot path.

Checks: commands and browser actions.

Result: kept or rejected, with the score change and reason.
```

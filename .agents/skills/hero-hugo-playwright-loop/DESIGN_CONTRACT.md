# Design contract

## Thesis

The site is a technical editorial portfolio. The CV introduces the person; the blog explains the work; project pages let readers inspect the evidence.

## Shared identity

- Slate canvas, light paper surfaces, and teal actions come from `design/tokens.json`.
- Fraunces is reserved for page and project titles. Open Sans or the system UI stack carries body text and controls.
- Thin rules and space establish hierarchy. Cards are used for discrete objects, not every paragraph.
- Motion is brief and optional. `prefers-reduced-motion` removes transforms and decorative animation.
- Focus remains visible. Controls have descriptive labels and comfortable targets.

## Wide layout

```text
[site header........................................]
[local navigation] [main reading column] [facts]
                   [title and badges]
                   [languages]
                   [overview]
                   [getting started]
                   [project-specific sections]
```

## Compact layout

```text
[site header]
[horizontal local navigation]
[title]
[badges]
[languages]
[overview]
[getting started]
[project-specific sections]
[facts]
```

## Accessibility floor

- Normal text contrast is at least 4.5:1.
- Large or bold text contrast is at least 3:1.
- Interactive targets are at least 44 CSS pixels on compact layouts.
- Text survives browser zoom to 200 percent without clipping or lost actions.
- Language and status are named in text. Color is supplementary.
- Dark and light modes expose the same information.

## CSS rules

- Add or change a semantic token before repeating a literal color.
- Prefer one scoped component selector over chains of specificity or new `!important` rules.
- Keep the CV and Hugo density different while reusing color, type, focus, radius, and spacing tokens.
- Remove a redundant wrapper, badge, card, or label when it adds no information.

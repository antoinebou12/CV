# Technical editorial design

Approved direction: asymmetric portrait-led hero, editorial typography, spacious
project cards and subtle motion. Preserve the slate-and-teal palette, page widths,
bilingual content and static rendering.

The Awwwards skill informed the hierarchy and polish pass. Its optional animation
frameworks are not required here: CSS handles interaction feedback, and content
remains visible with JavaScript disabled. Companion skills unavailable in this
environment were not claimed as executed.

## Implementation

- `css/cv-editorial.css`: screen-only CV and About design layer. Print retains the
  previous CV layout. Fraunces display type pairs with the existing Open Sans body.
- `scripts/build/generate_aeo_content.py`: generated About pages inherit the same
  styles and bilingual profile label. Do not edit generated About pages alone.
- `hugo/assets/editorial.css`: matching OKLCH role tokens, editorial blog opening,
  article titles, search headings and cards. Both light and dark modes are retained.
- Motion uses short color/border transitions and never hides content pending
  JavaScript. The original particle background is restored behind the CV and About
  pages, sized to the viewport and non-interactive so it cannot intercept links.
  Reduced-motion users receive the static background without particle initialization.
- The follow-up restraint pass removes the portrait grid frame and decorative
  arrows, uses straightforward location and blog labels, and replaces nested project
  card outlines with simple separators. Section headings use the body typeface;
  display typography is reserved for the main page title.
- Native details, focus outlines and mobile navigation remain in place.

## Local checks

Build Hugo and regenerate About/default HTML after source changes. Verify the CV,
About, blog home, article and search pages in both languages at 320, 768, 1280 and
1920 px, plus dark mode, keyboard navigation and reduced motion before publication.
The October 23 pass verified the CV at a measured 320 px content width, the
French search flow, the mobile blog menu and its Escape focus return, and the
46-entry project directory. Motion pause persists after reload. Native sections
remain usable without animation. HTML validation, EN/FR parity, data/schema,
generated LaTeX and meta-description checks pass. This is not a WCAG conformance
certification; assistive-technology testing remains useful.

## Public project review, October 23, 2026

The public GitHub user endpoint returned 46 repositories: 30 originals and 16
forks, with seven archived repositories across those categories. The directory
groups archived repositories separately and labels forks individually. Its data
is `hugo/data/github_inventory.json`; French descriptions are in
`hugo/data/github_descriptions_fr.json`. It includes no private repository data.

Dimension, DasherControl and bloc received bilingual articles after reading the
module entry points or request handlers. The bloc comparison was 10 commits
ahead and five behind its upstream; no claim of upstream acceptance is made.
Dimension's heightmap and DasherControl's original screenshot/GIF retain their
source links and MIT license notices in the article bundles. The GIF starts only
when the reader expands its disclosure.

The CV links use the current names Artemis-N3DS and sm64coopdx-switch-N3DS,
confirmed through GitHub redirects. Individual star badges were refreshed from
the public snapshot; profile-wide historical totals remain separate.

`js/cv-interactions.js` owns particle setup and the persisted pause control.
It honors the OS motion preference, suspends rendering in hidden tabs, and does
not animate content into an initially hidden state. Both publishing paths copy
the new `js` directory. Blog navigation prevents tabbing into a closed drawer,
contains keyboard focus while open, and returns focus on Escape.

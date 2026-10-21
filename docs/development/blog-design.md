# Blog design

The blog is Antoine Boucher's engineering notebook: help readers find a project,
then understand its code and decisions. The CV's slate-blue surround and teal
links are the identity; original project screenshots provide the visual interest.

The Apple design skill supplied for this revision informed accessibility,
hierarchy, spacing and adaptability. Native macOS navigation conventions do not
apply to this static website. References read from
https://github.com/dickwu/apple-design-skill/tree/main/references include
accessibility, layout, typography, color, designing-for-macos, collections,
dark-mode and cross-platform.

Design judgments: retain native HTML disclosures and selects, remove redundant
overlaid category badges, use a quiet two-column image grid and one column on
compact screens. Preserve full image contents instead of cropping diagrams.

Regular layout: navigation / introduction / filters / two-column articles.
Compact layout: name and menu / introduction / wrapping filters / one-column articles.
Article layout: back link / title and date / reading column / tags / adjacent posts.

The shell follows the CV's Bootstrap widths: 750, 970 and 1170 CSS pixels.
Article content is capped at 800 pixels; controls and headings use a sans-serif
stack, body text is 17px with 1.8 line height, titles scale from 29.6px to 44.8px.
Cards use 24px padding, tags use 8px gaps and 44px mobile hit targets.

Tokens live in `hugo/assets/editorial.css`, loaded after the theme and legacy
overrides. Light: canvas #334960, page #ffffff, inset #f2f6f7, text #363636,
muted #566573, accent #1a5f56. Dark: canvas #172735, page #203343,
inset #2a4052, text #e0e7ec, muted #b8c8d2, accent #91dbca.
Motion is disabled for reduced-motion users; no translucent content surfaces.

Measured contrast: muted text on white 5.99:1; teal tags on light inset 6.86:1;
dark muted text on cards 6.65:1; dark teal tags on inset 6.75:1.

Explicit component declarations override the precompiled theme's ID-specific
preflight. Do not rely on new utility class names without rebuilding Tailwind.
Keep the `[hidden]` rule so year filtering remains functional.

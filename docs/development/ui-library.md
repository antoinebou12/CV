# UI library (Hugo blog)

The blog has a small set of shared components in `hugo/assets/ui.css` and
`hugo/assets/ui.js`. Use them before writing a new style. The
`pick-ui-library` skill (`.claude/skills/` and `.cursor/skills/`) tells an
agent which component or library fits a task.

## Principles

- **Do not rebuild what exists.** A new button is `.ui-btn`, not a new class.
- **One standout per screen.** One element draws the eye. The rest is flat:
  1px borders, no gradients, no glow, no stacked shadows.
- **Tokens only.** Colours, radii and easing come from `design/tokens.json`
  (generated into `hugo/assets/design-tokens.css`) and the editorial variables
  in `hugo/assets/editorial.css`: `--brand-accent`, `--text-strong`,
  `--text-muted`, `--surface-border`, `--surface-1`, `--journal-soft`.
- **Motion is short and optional.** Hover and press use CSS transitions. All of
  it is switched off under `prefers-reduced-motion`.
- **No placeholder images.** If a post has no cover, show text.

## Components

### Button

```html
<a class="ui-btn ui-btn--primary" href="/projects/">Browse projects</a>
<a class="ui-btn" href="/posts/">Read the posts</a>
<button class="ui-btn ui-btn--quiet" type="button">Skip</button>
```

`ui-btn` is the bordered default, `--primary` is filled with the accent (one
per group), `--quiet` has no border. Minimum height is 44px.

### Chip

```html
<span class="ui-chip ui-chip--accent">Latest post</span>
<span class="ui-chip">Audio story · 2:42</span>
```

For short labels and counts. Not a link style.

### Stats

```html
<dl class="ui-stats">
  <div class="ui-stat"><dt>Posts</dt><dd data-count="59">59</dd></div>
</dl>
```

The number is in the HTML. `data-count` makes `ui.js` count up to it once, when
it scrolls into view. Load the script on pages that use it:

```go-html-template
{{- $js := resources.Get "ui.js" | minify | fingerprint -}}
<script defer src="{{ $js.RelPermalink }}" integrity="{{ $js.Data.Integrity }}"></script>
```

### Panel

`.ui-panel` is a flat bordered surface with a 14px radius.

### Home hero

`hugo/layouts/partials/home-hero.html`, used by `layouts/_default/list.html` on
the home page. It shows the headline, two buttons, three counted facts (posts,
documented projects, audio stories) and a panel with the newest post. The
panel shows the post's cover only when the post has a real image. Copy is
written in the partial, in English and French.

## Other building blocks

| Need | Use |
|---|---|
| Section intro | `.journal-intro`, `.journal-eyebrow` (`editorial.css`) |
| Post or project card | `partials/post-list-item.html` |
| Audio player | [podcasts.md](podcasts.md) |
| Live demo, 3D model | [blog-embeds.md](blog-embeds.md) |
| Scroll reveal | `data-reveal` (`motion.js`) |
| Header and navigation | [hugo-navigation.md](hugo-navigation.md) |

## Adding a component

1. Check the table in the `pick-ui-library` skill first.
2. Add the rule to `ui.css` under a comment header. Start selectors with
   `.blog-site` and use `!important`: the theme reset is boosted and wins
   otherwise.
3. Add `not-prose` to the root element when it sits inside article text.
4. Document it here and add a row to the skill.
5. Check light and dark themes and a phone width.

`ui.css` is part of the main bundle (`partials/head.html`), so it loads on
every blog page.

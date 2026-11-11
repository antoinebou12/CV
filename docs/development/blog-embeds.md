# Live demos and 3D models in posts

Two shortcodes put interactive content inside a post, a project page or a
project note. Both work in English and French pages and need no extra setup.

## Live demos: `demos`

A tabbed panel that runs a web demo inside the page. Nothing loads from the
demo host until the reader presses **Start the demo**. Switching tabs swaps the
running demo, **Stop** removes it, and each demo also has an "Open in a new
tab" link.

```markdown
{{< demos title="Dimension running in your browser" height="640" >}}
Render | https://antoinebou12.github.io/Dimension/render/ | A cube, a tetrahedron and a cylinder.
Geometry | https://antoinebou12.github.io/Dimension/geometry/ | Mesh demos from the geometry crate.
{{< /demos >}}
```

- One demo per line: `Label | https://url | short description`.
- `title` and `height` (pixels, default 600) are optional.
- Only `https://` addresses are accepted; the build fails on anything else.
- The frame is sandboxed (`allow-scripts allow-same-origin allow-popups
  allow-pointer-lock`). A demo hosted on the site's own origin loses
  `allow-same-origin`.
- The demo host must allow framing, and must be listed in `frame-src` in the
  three CSP copies: `hugo/static/_headers`, `vercel.json` and
  `cloudflare/workers/agent-ready-home/worker.mjs`.

Files: `hugo/layouts/shortcodes/demos.html`, `hugo/assets/live-demos.js`,
styles in `hugo/assets/editorial.css` (search for `live-demos`).

### Dimension demos

The Dimension repository publishes its WebAssembly demos at
`https://antoinebou12.github.io/Dimension/`. The blog embeds Render, Geometry,
Mathlib and the embeddings demo (`mathlib/recommendation/`). The 3D demos need
a browser with WebGPU. The kinematics and physics demos are linked rather than
embedded.

Project notes use a simpler "Try it" panel driven by
`hugo/data/project_demos.json` (one URL per repository).

## 3D models: `modelviewer`

Shows a GLB or glTF model the reader can rotate and zoom.

```markdown
{{< modelviewer src="models/part.glb" title="Printed parts" height="460" >}}
```

- `src` is required. Put the model in the page bundle, or under `hugo/static/`
  when French and English pages share it.
- `title` is the caption and the accessible description.
- `height` is in pixels (default 420). `poster` is an optional preview image.
- The model turns slowly until the reader touches it; `rotate="false"` turns
  that off.
- The shortcode loads the viewer script itself, once per page, from jsDelivr
  with an integrity hash. Do not add a second `<script>` tag for it.

Keep models small: the WearMachine model is the only one in the repository,
and the figurines post leaves its 20–75 MB GLBs out of git on purpose
(`.gitignore`).

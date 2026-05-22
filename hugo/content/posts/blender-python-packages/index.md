---
post_kind: tutorial
title: A Method to Install Python Packages for Add-ons & Plugins in Blender (Windows, Blender 4.2+)
date: 2025-02-08T12:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "Install pip packages into Blender’s embedded Python — user modules folder, background thread, popups — without breaking the core install."
translationKey: blender-python-packages
tags:
  - Blender
  - Python
  - pip
  - Addons
canonicalURL: "https://medium.com/@antoine.boucher012/a-method-to-install-python-packages-for-add-ons-plugins-in-blender-windows-blender-4-2-98bcbe10fa81"
images:
  - img-001.png
---

Blender add-ons that need **NumPy**, **meshio**, or **requests** hit the same wall: Blender ships its **own Python**, so system `pip` does nothing useful. I wrote a small installer that targets Blender’s `sys.executable`, drops wheels under `scripts/modules`, and runs in a **background thread** so the UI stays responsive (Blender 4.2+, Windows). **[Version française]({{< ref "/posts/blender-python-packages/index.fr.md" >}})**.

<!--more-->

![Blender Scripting workspace — Text Editor and Run Script](./img-001.png)

## The problem in one sentence

You cannot `pip install` globally and expect `import meshio` inside Blender — the interpreter path is Blender’s bundled runtime.

## Strategy

| Piece | Role |
|-------|------|
| `sys.executable` | Invoke **pip against Blender’s Python** |
| `bpy.utils.user_resource("SCRIPTS", path="modules")` | Writable install dir per user/version |
| `site.addsitedir` | Make imports resolve next launch |
| Background thread + `bpy.app.timers` | Avoid freezing the UI; show popups when done |

## The installer script (core idea)

```python
REQUIRED_PACKAGES = {
    "fileseq": "fileseq==1.15.2",
    "meshio": "meshio==5.3.4",
    "rich": "rich==13.7.0",
    "requests": "requests==2.31.0",
}

def install_package(package, modules_path):
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "--upgrade", "--target", modules_path, package,
    ])
```

Full script in the [Medium article](https://medium.com/@antoine.boucher012/a-method-to-install-python-packages-for-add-ons-plugins-in-blender-windows-blender-4-2-98bcbe10fa81) and my repo copies — includes progress bar hooks and `__import__` checks to skip already-installed wheels.

## How to run it

**Option A — Scripting workspace:** paste in Text Editor → Run Script → wait for popup.

**Option B — Add-on `register()`:**

```python
def register():
    modules_path = get_modules_path()
    append_modules_to_sys_path(modules_path)
    background_install_packages(REQUIRED_PACKAGES, modules_path)
```

Ship dependencies with your add-on so users are not guessing which Python to use.

## Troubleshooting

- Restart Blender after first install.
- `print(sys.path)` if imports fail — confirm `modules` is listed.
- Version pin wheels — Blender’s Python version is not your system 3.12.

## When not to use this pattern

| Case | Why |
|------|-----|
| Add-on targets many Blender versions | Pin and test per minor version |
| Heavy CUDA stacks | May exceed user GPU/driver setup |
| Corporate locked-down PCs | pip may be blocked — vendor wheels manually |

## Takeaway

Automate dependency install inside Blender’s sandbox; users stop emailing “which Python?” — you own the matrix in `REQUIRED_PACKAGES`.

## Related posts

- [Skate rack — CAD to plywood]({{< ref "/posts/skate-rack-cad-to-object/index.md" >}}) — physical maker pipeline
- [AI figurines / 3D print]({{< ref "/posts/ai-figurines-3d-printing/index.md" >}}) — mesh tools in another ecosystem

## References

- [Blender API](https://docs.blender.org/api/current/)
- [Managing Python in Blender](https://wiki.blender.org/wiki/Building_Blender/Python)
- [Python packaging guide](https://packaging.python.org/)

---

*Originally published on [Medium](https://medium.com/@antoine.boucher012/a-method-to-install-python-packages-for-add-ons-plugins-in-blender-windows-blender-4-2-98bcbe10fa81).*

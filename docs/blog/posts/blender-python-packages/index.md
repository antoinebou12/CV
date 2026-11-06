# A Method to Install Python Packages for Add-ons & Plugins in Blender (Windows, Blender 4.2+)

> Install pip packages into Blender’s embedded Python — user modules folder, background thread, popups — without breaking the core install.

- HTML page: https://antoineboucher.info/CV/blog/posts/blender-python-packages/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/posts/blender-python-packages/index.md
- Published: 2025-02-08
- Updated: 2026-11-05
- Tags: Blender, Python, Pip, Addons, Plugins
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)Blender add-ons that need **NumPy**, **meshio**, or **requests** hit the same wall: Blender ships its **own Python**, so system `pip` does nothing useful. I wrote a small installer that targets Blender’s `sys.executable`, drops wheels under `scripts/modules`, and runs in a **background thread** so the UI stays responsive (Blender 4.2+, Windows).

## The problem in one sentence

You cannot `pip install` globally and expect `import meshio` inside Blender — the interpreter path is Blender’s bundled runtime.

## Strategy

| Piece | Role |
|-------|------|
| `sys.executable` | Invoke **pip against Blender’s Python** |
| `bpy.utils.user_resource("SCRIPTS", path="modules")` | Writable install dir per user/version |
| `site.addsitedir` | Make imports resolve next launch |
| Background thread + `bpy.app.timers` | Avoid freezing the UI; show popups when done |

## The installer script

```python
import bpy
import sys
import site
import logging
import subprocess
import threading

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# List of packages required by the add-on/plugin
REQUIRED_PACKAGES = {
    "fileseq": "fileseq==1.15.2",
    "meshio": "meshio==5.3.4",
    "rich": "rich==13.7.0",
    "requests": "requests==2.31.0"
}

def get_blender_python_path():
    """Returns the path of Blender's embedded Python interpreter."""
    return sys.executable

def get_modules_path():
    """Return a writable directory for installing Python packages."""
    return bpy.utils.user_resource("SCRIPTS", path="modules", create=True)

def append_modules_to_sys_path(modules_path):
    """Ensure Blender can find installed packages."""
    if modules_path not in sys.path:
        sys.path.append(modules_path)
    site.addsitedir(modules_path)

def display_message(message, title="Notification", icon='INFO'):
    """Show a popup message in Blender."""
    def draw(self, context):
        self.layout.label(text=message)
    def show_popup():
        bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)
        return None  # Stops timer
    bpy.app.timers.register(show_popup)

def install_package(package, modules_path):
    """Install a single package using Blender's Python."""
    try:
        logger.info(f"Installing {package}...")
        subprocess.check_call([
            get_blender_python_path(),
            "-m",
            "pip",
            "install",
            "--upgrade",
            "--target",
            modules_path,
            package
        ])
        logger.info(f"{package} installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install {package}. Error: {e}")
        display_message(f"Failed to install {package}. Check console for details.", icon='ERROR')

def background_install_packages(packages, modules_path):
    """Install missing packages in a background thread."""
    def install_packages():
        wm = bpy.context.window_manager
        wm.progress_begin(0, len(packages))
        for i, (module_name, pip_spec) in enumerate(packages.items()):
            try:
                __import__(module_name)
                logger.info(f"'{module_name}' is already installed.")
            except ImportError:
                install_package(pip_spec, modules_path)
            wm.progress_update(i + 1)
        wm.progress_end()
        display_message("All required packages installed successfully.")
    threading.Thread(target=install_packages, daemon=True).start()

# Setup
modules_path = get_modules_path()
append_modules_to_sys_path(modules_path)

# Start package installation
background_install_packages(REQUIRED_PACKAGES, modules_path)
```

Four details do the work:

- `sys.executable` inside Blender is Blender’s own interpreter, so `pip` installs for the Python that will import the package.
- `--target` writes into the per-user `scripts/modules` folder, which is writable without admin rights and survives add-on reloads.
- The `__import__` check skips packages that are already importable, so a second run is quick.
- Popups go through `bpy.app.timers` because only the main thread may touch the UI, not the install thread.

## How to run it

**Option A — Scripting workspace:** paste in Text Editor → Run Script → wait for popup.

![Blender Scripting workspace with the installer in the Text Editor](https://antoineboucher.info/CV/blog/posts/blender-python-packages/images/img-001.png)

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

- [Skate rack — CAD to plywood](https://antoineboucher.info/CV/blog/posts/skate-rack-cad-to-object/) — physical maker pipeline
- [AI figurines / 3D print](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/) — mesh tools in another ecosystem

## References

- [Blender API](https://docs.blender.org/api/current/)
- [Managing Python in Blender](https://wiki.blender.org/wiki/Building_Blender/Python)
- [Python packaging guide](https://packaging.python.org/)

---

*Originally published on [Medium](https://medium.com/@antoine.boucher012/a-method-to-install-python-packages-for-add-ons-plugins-in-blender-windows-blender-4-2-98bcbe10fa81).*

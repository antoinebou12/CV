# Installer des paquets Python pour les add-ons Blender (Windows, Blender 4.2+)

> pip dans le Python embarqué de Blender — dossier modules utilisateur, thread d’arrière-plan, popups.

- Page HTML: https://antoineboucher.info/CV/blog/fr/posts/blender-python-packages/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/posts/blender-python-packages/index.md
- Publié: 2025-02-08
- Mis à jour: 2026-11-05
- Tags: Blender, Python, Pip, Addons, Plugins
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)Les add-ons Blender qui ont besoin de **NumPy**, **meshio** ou **requests** butent tous sur le même mur : Blender embarque **son propre Python**, donc le `pip` du système ne sert à rien. J’ai écrit un petit installateur qui cible le `sys.executable` de Blender, dépose les paquets dans `scripts/modules` et tourne dans un **thread d’arrière-plan** pour que l’interface reste réactive (Blender 4.2+, Windows).

## Le problème en une phrase

Un `pip install` global ne rend pas `import meshio` disponible dans Blender : l’interpréteur est celui fourni avec Blender.

## La stratégie

| Élément | Rôle |
|---------|------|
| `sys.executable` | Lancer **pip avec le Python de Blender** |
| `bpy.utils.user_resource("SCRIPTS", path="modules")` | Dossier d’installation accessible en écriture, par utilisateur et par version |
| `site.addsitedir` | Rendre les imports résolubles |
| Thread d’arrière-plan + `bpy.app.timers` | Ne pas figer l’interface ; afficher une fenêtre à la fin |

## Le script d’installation

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

Quatre détails font tout le travail :

- Dans Blender, `sys.executable` est l’interpréteur de Blender : `pip` installe donc pour le Python qui fera l’import.
- `--target` écrit dans le dossier utilisateur `scripts/modules`, accessible sans droits administrateur et conservé quand l’add-on est rechargé.
- La vérification `__import__` saute les paquets déjà importables ; une deuxième exécution est rapide.
- Les fenêtres passent par `bpy.app.timers`, car seule la boucle principale peut toucher l’interface, pas le thread d’installation.

## Comment l’exécuter

**Option A — espace Scripting :** coller le script dans l’éditeur de texte → Run Script → attendre la fenêtre de confirmation.

![Espace Scripting de Blender avec l’installateur dans l’éditeur de texte](https://antoineboucher.info/CV/blog/posts/blender-python-packages/images/img-001.png)

**Option B — dans le `register()` d’un add-on :**

```python
def register():
    modules_path = get_modules_path()
    append_modules_to_sys_path(modules_path)
    background_install_packages(REQUIRED_PACKAGES, modules_path)
```

Livrez les dépendances avec l’add-on : les utilisateurs n’ont plus à deviner quel Python utiliser.

## Dépannage

- Redémarrer Blender après la première installation.
- `print(sys.path)` si un import échoue, pour vérifier que `modules` figure dans la liste.
- Épingler les versions : le Python de Blender n’est pas le 3.12 de votre système.

## Quand ne pas utiliser ce modèle

| Cas | Pourquoi |
|-----|----------|
| L’add-on vise beaucoup de versions de Blender | Épingler et tester par version mineure |
| Piles CUDA lourdes | Peuvent dépasser la configuration GPU et pilotes de l’utilisateur |
| Postes d’entreprise verrouillés | pip peut être bloqué ; fournir les wheels à la main |

## À retenir

Automatisez l’installation des dépendances dans le bac à sable de Blender. Les utilisateurs arrêtent de demander « quel Python ? », et c’est vous qui maîtrisez la liste dans `REQUIRED_PACKAGES`.

## Articles liés

- [Support à planches : de la CAO au contreplaqué](https://antoineboucher.info/CV/blog/fr/posts/skate-rack-cad-to-object/) : chaîne de fabrication physique
- [Figurines IA et impression 3D](https://antoineboucher.info/CV/blog/fr/posts/ai-figurines-3d-printing/) : outils de maillage dans un autre écosystème

## Références

- [API Blender](https://docs.blender.org/api/current/)
- [Gérer Python dans Blender](https://wiki.blender.org/wiki/Building_Blender/Python)
- [Guide d’empaquetage Python](https://packaging.python.org/)

---

*Publié à l’origine sur [Medium](https://medium.com/@antoine.boucher012/a-method-to-install-python-packages-for-add-ons-plugins-in-blender-windows-blender-4-2-98bcbe10fa81) (en anglais).*

---
post_kind: tutorial
title: "Installer des paquets Python pour les add-ons Blender (Windows, Blender 4.2+)"
date: 2025-02-08T12:00:00-04:00
description: Script d’installation automatique des dépendances pip dans l’environnement Python embarqué de Blender — dossier utilisateur, thread d’arrière-plan, popups.
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

## Introduction

Blender offre une API Python puissante pour scripts, add-ons et plugins. Un point délicat : **installer des paquets Python tiers** dans l’**environnement Python isolé** de Blender.

Contrairement à une installation Python système, Blender embarque son propre interprète : `pip` « global » ne suffit pas toujours. Cet article propose une méthode **générale et robuste** pour installer les dépendances des add-ons tout en restant compatible entre versions.

![Espace Scripting de Blender avec l’éditeur de texte et Exécuter le script](./img-001.png)

*Lancer l’installateur depuis l’éditeur de texte (espace Scripting).*

## Pourquoi des paquets externes dans le Python de Blender ?

Beaucoup d’add-ons avancés reposent sur des bibliothèques comme :

*   **NumPy & SciPy** — calcul scientifique et maillages  
*   **Meshio** — conversion de formats de maillage  
*   **Pillow** — traitement d’image  
*   **Requests** — appels HTTP / APIs  
*   **PyTorch / TensorFlow** — ML  

Ces paquets doivent être installés **dans l’arborescence / l’environnement utilisés par Blender**, pas seulement dans le Python du système.

## Script Python généralisé pour add-ons

Le script ci-dessous **installe automatiquement** les paquets manquants via le Python de Blender (`sys.executable`), dans un répertoire utilisateur, avec retour utilisateur (logs + popups).

## Fonctionnalités

- Fonctionne **dans** Blender, sans ligne de commande obligatoire  
- Installe **plusieurs paquets** en une passe  
- Utilise un **répertoire utilisateur** plutôt que les fichiers cœur de Blender  
- S’exécute en **arrière-plan** pour ne pas bloquer l’UI  

## Script d’installation

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

## Découpage pas à pas

## 1️⃣ Chemin de l’interprète Blender

```python
def get_blender_python_path():
    return sys.executable
```

*   Utilise `sys.executable` pour que `pip` cible le bon Python.

## 2️⃣ Répertoire d’installation

```python
def get_modules_path():
    return bpy.utils.user_resource("SCRIPTS", path="modules", create=True)
```

*   Dossier typique sous Windows : `AppData\Roaming\Blender Foundation\Blender\<version>\scripts\modules`.

## 3️⃣ Rendre les paquets importables

```python
def append_modules_to_sys_path(modules_path):
    if modules_path not in sys.path:
        sys.path.append(modules_path)
    site.addsitedir(modules_path)
```

*   Ajoute le dossier à `sys.path` et `site.addsitedir` pour que Blender **trouve** les paquets.

## 4️⃣ Installer un paquet

```python
def install_package(package, modules_path):
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
```

*   Appelle `python -m pip install --target ...` avec l’exécutable Blender.

## 5️⃣ Plusieurs paquets

```python
def background_install_packages(packages, modules_path):
    threading.Thread(target=install_packages, daemon=True).start()
```

*   **Thread d’arrière-plan** pour éviter de figer l’interface.

## 6️⃣ Messages utilisateur

```python
def display_message(message, title="Notification", icon='INFO'):
    bpy.app.timers.register(show_popup)
```

*   Popups Blender pour succès / erreur.

## Utilisation

## Option 1 : exécuter dans Blender

1. Ouvrir **Blender** (4.2+).  
2. Espace de travail **Scripting**.  
3. **Éditeur de texte**.  
4. Coller le script et **Run Script**.  
5. Installation automatique + popup à la fin.

## Option 2 : intégrer à un add-on

*   Appelez la même logique depuis `register()` pour installer les dépendances au chargement.

```python
def register():
  """Register all classes and set up PointerProperties."""
  modules_path = get_modules_path()
  append_modules_to_sys_path(modules_path)
  # Install required packages in the background
  background_install_packages(REQUIRED_PACKAGES, modules_path)
  ...
```

## Dépannage

**Paquets introuvables après installation ?**

*   Redémarrer Blender.  
*   Vérifier `sys.path` :

```python
import sys
print(sys.path)
```

## En bref

Cette méthode permet d’**installer des paquets pip** proprement dans l’environnement sandboxé de Blender et d’**automatiser les dépendances** pour les utilisateurs d’add-ons.

## Pour aller plus loin

*   [Blender API Documentation](https://docs.blender.org/api/current/)
*   [Managing Python in Blender](https://wiki.blender.org/wiki/Building_Blender/Python)
*   [Python Package Installation Guide](https://packaging.python.org/)

---

*Publié à l’origine sur [Medium](https://medium.com/@antoine.boucher012/a-method-to-install-python-packages-for-add-ons-plugins-in-blender-windows-blender-4-2-98bcbe10fa81).*

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
---

## Introduction

Blender offre une API Python puissante pour scripts, add-ons et plugins. Un point délicat : **installer des paquets Python tiers** dans l’**environnement Python isolé** de Blender.

Contrairement à une installation Python système, Blender embarque son propre interprète : `pip` « global » ne suffit pas toujours. Cet article propose une méthode **générale et robuste** pour installer les dépendances des add-ons tout en restant compatible entre versions.

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

import bpy  
import sys  
import site  
import logging  
import subprocess  
import threading  
  
\# Set up logging  
logger = logging.getLogger(\_\_name\_\_)  
logging.basicConfig(level=logging.INFO)  
\# List of packages required by the add-on/plugin  
REQUIRED\_PACKAGES = {  
    "fileseq": "fileseq==1.15.2",  
    "meshio": "meshio==5.3.4",  
    "rich": "rich==13.7.0",  
    "requests": "requests==2.31.0"  
}  
def get\_blender\_python\_path():  
    """Returns the path of Blender's embedded Python interpreter."""  
    return sys.executable  
def get\_modules\_path():  
    """Return a writable directory for installing Python packages."""  
    return bpy.utils.user\_resource("SCRIPTS", path="modules", create=True)  
def append\_modules\_to\_sys\_path(modules\_path):  
    """Ensure Blender can find installed packages."""  
    if modules\_path not in sys.path:  
        sys.path.append(modules\_path)  
    site.addsitedir(modules\_path)  
def display\_message(message, title="Notification", icon='INFO'):  
    """Show a popup message in Blender."""  
    def draw(self, context):  
        self.layout.label(text=message)  
    def show\_popup():  
        bpy.context.window\_manager.popup\_menu(draw, title=title, icon=icon)  
        return None  \# Stops timer  
    bpy.app.timers.register(show\_popup)  
def install\_package(package, modules\_path):  
    """Install a single package using Blender's Python."""  
    try:  
        logger.info(f"Installing {package}...")  
        subprocess.check\_call(\[  
            get\_blender\_python\_path(),  
            "-m",  
            "pip",  
            "install",  
            "--upgrade",  
            "--target",  
            modules\_path,  
            package  
        \])  
        logger.info(f"{package} installed successfully.")  
    except subprocess.CalledProcessError as e:  
        logger.error(f"Failed to install {package}. Error: {e}")  
        display\_message(f"Failed to install {package}. Check console for details.", icon='ERROR')  
def background\_install\_packages(packages, modules\_path):  
    """Install missing packages in a background thread."""  
    def install\_packages():  
        wm = bpy.context.window\_manager  
        wm.progress\_begin(0, len(packages))  
        for i, (module\_name, pip\_spec) in enumerate(packages.items()):  
            try:  
                \_\_import\_\_(module\_name)  
                logger.info(f"'{module\_name}' is already installed.")  
            except ImportError:  
                install\_package(pip\_spec, modules\_path)  
            wm.progress\_update(i + 1)  
        wm.progress\_end()  
        display\_message("All required packages installed successfully.")  
    threading.Thread(target=install\_packages, daemon=True).start()  
\# Setup  
modules\_path = get\_modules\_path()  
append\_modules\_to\_sys\_path(modules\_path)  
\# Start package installation  
background\_install\_packages(REQUIRED\_PACKAGES, modules\_path)

## Découpage pas à pas

## 1️⃣ Chemin de l’interprète Blender

def get\_blender\_python\_path():  
    return sys.executable

*   Utilise `sys.executable` pour que `pip` cible le bon Python.

## 2️⃣ Répertoire d’installation

def get\_modules\_path():  
    return bpy.utils.user\_resource("SCRIPTS", path\="modules", create\=True)

*   Dossier typique sous Windows : `AppData\Roaming\Blender Foundation\Blender\<version>\scripts\modules`.

## 3️⃣ Rendre les paquets importables

def append\_modules\_to\_sys\_path(modules\_path):  
    if modules\_path not in sys.path:  
        sys.path.append(modules\_path)  
    site.addsitedir(modules\_path)

*   Ajoute le dossier à `sys.path` et `site.addsitedir` pour que Blender **trouve** les paquets.

## 4️⃣ Installer un paquet

def install\_package(package, modules\_path):  
    subprocess.check\_call(\[  
        get\_blender\_python\_path(),  
        "-m",  
        "pip",  
        "install",  
        "--upgrade",  
        "--target",  
        modules\_path,  
        package  
    \])

*   Appelle `python -m pip install --target ...` avec l’exécutable Blender.

## 5️⃣ Plusieurs paquets

def background\_install\_packages(packages, modules\_path):  
    threading.Thread(target=install\_packages, daemon=True).start()

*   **Thread d’arrière-plan** pour éviter de figer l’interface.

## 6️⃣ Messages utilisateur

def display\_message(message, title="Notification", icon='INFO'):  
    bpy.app.timers.register(show\_popup)

*   Popups Blender pour succès / erreur.

## Utilisation

## Option 1 : exécuter dans Blender

1. Ouvrir **Blender** (4.2+).  
2. Espace de travail **Scripting**.  
3. **Éditeur de texte**.  
4. Coller le script et **Run Script**.  
5. Installation automatique + popup à la fin.

![](./img-001.png)

## Option 2 : intégrer à un add-on

*   Appelez la même logique depuis `register()` pour installer les dépendances au chargement.

def register():  
  """Register all classes and set up PointerProperties."""  
  modules\_path = get\_modules\_path()  
  append\_modules\_to\_sys\_path(modules\_path)  
  \# Install required packages in the background  
  background\_install\_packages(REQUIRED\_PACKAGES, modules\_path)  
  ...

## Dépannage

**Paquets introuvables après installation ?**

*   Redémarrer Blender.  
*   Vérifier `sys.path` :

import sys  
print(sys.path)

## En bref

Cette méthode permet d’**installer des paquets pip** proprement dans l’environnement sandboxé de Blender et d’**automatiser les dépendances** pour les utilisateurs d’add-ons.

## Pour aller plus loin

*   [Blender API Documentation](https://docs.blender.org/api/current/)
*   [Managing Python in Blender](https://wiki.blender.org/wiki/Building_Blender/Python)
*   [Python Package Installation Guide](https://packaging.python.org/)

---

*Publié à l’origine sur [Medium](https://medium.com/@antoine.boucher012/a-method-to-install-python-packages-for-add-ons-plugins-in-blender-windows-blender-4-2-98bcbe10fa81).*

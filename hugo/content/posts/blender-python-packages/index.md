---
post_kind: tutorial
title: A Method to Install Python Packages for Add-ons & Plugins in Blender (Windows, Blender 4.2+)
date: 2025-02-08T12:00:00-04:00
description: Automatic pip installs into Blender’s embedded Python via a user-writable modules folder, background thread, and UI popups.
translationKey: blender-python-packages
tags:
    - Blender
    - Python
    - pip
    - Addons
canonicalURL: "https://medium.com/@antoine.boucher012/a-method-to-install-python-packages-for-add-ons-plugins-in-blender-windows-blender-4-2-98bcbe10fa81"
---

## Introduction

Blender is a powerhouse for 3D creation, offering a Python API that allows users to extend its functionality with scripts, add-ons, and plugins. However, one challenge developers face is **installing external Python packages** within Blender’s **isolated Python environment**.

## Get Antoine Boucher’s stories in your inbox

Unlike system-wide Python installations, Blender bundles its own Python interpreter, making standard package installations tricky. This article presents **a more general and robust method** to install Python dependencies for Blender add-ons and plugins — ensuring a smooth workflow across different versions.

## Why Install External Packages in Blender’s Python?

Many advanced Blender add-ons require external Python libraries, such as:

*   **NumPy & SciPy** — Scientific computing and mesh processing
*   **Meshio** — Converting mesh file formats
*   **Pillow** — Image processing
*   **Requests** — Handling HTTP requests for APIs
*   **PyTorch/TensorFlow** — Machine learning integration

Since Blender ships with its own Python environment, these packages **must be installed within Blender’s directory** rather than the system-wide Python installation.

## A Robust & Generalized Python Script for Add-ons

This script ensures the **automatic installation** of required packages inside Blender’s Python environment. It detects missing modules, and installs them using Blender’s `sys.executable`, and provides user feedback.

## 💡 Features

✔️ Works **inside** Blender without requiring terminal commands  
✔️ Installs **multiple packages** automatically  
✔️ Uses a **user-writable directory** instead of modifying Blender’s core files  
✔️ Runs **asynchronously** to keep Blender responsive

## 📜 The Installation Script

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

## 📌 Step-by-Step Breakdown

## 1️⃣ Identifying Blender’s Python Path

def get\_blender\_python\_path():  
    return sys.executable

*   Finds Blender’s Python interpreter (`python.exe`) to ensure `pip` installs packages correctly.

## 2️⃣ Choosing the Installation Directory

def get\_modules\_path():  
    return bpy.utils.user\_resource("SCRIPTS", path\="modules", create\=True)

*   Installs packages in Blender’s **user scripts directory** (`AppData\Roaming\Blender Foundation\Blender\<version>\scripts\modules`).

## 3️⃣ Ensuring Packages Are Found

def append\_modules\_to\_sys\_path(modules\_path):  
    if modules\_path not in sys.path:  
        sys.path.append(modules\_path)  
    site.addsitedir(modules\_path)

*   Adds the modules directory to Python’s search path (`sys.path`), ensuring that Blender can **find the installed packages**.

## 4️⃣ Installing a Single Package

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

*   Uses Blender’s **Python environment** to install the required package in the correct directory.

## 5️⃣ Handling Multiple Packages

def background\_install\_packages(packages, modules\_path):  
    threading.Thread(target=install\_packages, daemon=True).start()

*   Runs installation **in a background thread** to prevent Blender from freezing.

## 6️⃣ Displaying User Messages

def display\_message(message, title="Notification", icon='INFO'):  
    bpy.app.timers.register(show\_popup)

*   Provides **popup notifications** for a user-friendly installation experience.

## 🚀 How to Use This Script

## Option 1: Running Inside Blender

1.  Open **Blender** (Version 4.2+).
2.  Go to the **Scripting** workspace.
3.  Open the **Text Editor**.
4.  Paste the script and click **Run Script**.
5.  Blender will automatically **install the required packages** and display a popup when complete.

Press enter or click to view image in full size

![](./img-001.png)

## Option 2: Using as Part of an Add-on

*   Include this script inside your add-on to ensure required dependencies are installed automatically.

def register():  
  """Register all classes and set up PointerProperties."""  
  modules\_path = get\_modules\_path()  
  append\_modules\_to\_sys\_path(modules\_path)  
  \# Install required packages in the background  
  background\_install\_packages(REQUIRED\_PACKAGES, modules\_path)  
  ...

## 🛠️ Troubleshooting

**Packages Not Found After Installation?**

*   Restart Blender after running the script.
*   Manually check `sys.path` to ensure the correct directory is listed:

import sys  
print(sys.path)

## ✨ Final Thoughts

This **generalized method** allows Blender users and add-on developers to **install Python packages seamlessly** within Blender’s sandboxed environment. By automating dependency installation, you can ensure **maximum compatibility** without requiring users to install external tools manually.

## 🔗 Further Reading

*   [Blender API Documentation](https://docs.blender.org/api/current/)
*   [Managing Python in Blender](https://wiki.blender.org/wiki/Building_Blender/Python)
*   [Python Package Installation Guide](https://packaging.python.org/)

---

*Originally published on [Medium](https://medium.com/@antoine.boucher012/a-method-to-install-python-packages-for-add-ons-plugins-in-blender-windows-blender-4-2-98bcbe10fa81).*

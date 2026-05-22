---
post_kind: tutorial
title: "Installer des paquets Python pour les add-ons Blender (Windows, Blender 4.2+)"
date: 2025-02-08T12:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "pip dans le Python embarqué de Blender — dossier modules utilisateur, thread d’arrière-plan, popups."
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

Les add-ons qui demandent **NumPy**, **meshio** ou **requests** butent sur le **Python de Blender**. Petit installateur ciblant `sys.executable`, dossier `scripts/modules`, thread d’arrière-plan (Blender 4.2+, Windows). **[English version]({{< ref "/posts/blender-python-packages/index.md" >}})**.

<!--more-->

![Espace Scripting Blender](./img-001.png)

## Stratégie

| Élément | Rôle |
|---------|------|
| `sys.executable` | pip du Python Blender |
| `user_resource(..., path="modules")` | Répertoire writable |
| `site.addsitedir` | Imports au prochain lancement |
| Thread + timers | UI non gelée |

## Idée du script

```python
subprocess.check_call([
    sys.executable, "-m", "pip", "install",
    "--upgrade", "--target", modules_path, package,
])
```

Script complet : [Medium](https://medium.com/@antoine.boucher012/a-method-to-install-python-packages-for-add-ons-plugins-in-blender-windows-blender-4-2-98bcbe10fa81).

## Usage

Éditeur de texte ou `register()` d’add-on — redémarrer Blender après la première install.

## Bilan

Automatiser les dépendances ; fin des mails « quel Python ? ».

## Articles liés

- [Rack skate CAO → contreplaqué]({{< ref "/posts/skate-rack-cad-to-object/index.fr.md" >}})
- [Figurines IA]({{< ref "/posts/ai-figurines-3d-printing/index.fr.md" >}})

---

*Article [Medium](https://medium.com/@antoine.boucher012/a-method-to-install-python-packages-for-add-ons-plugins-in-blender-windows-blender-4-2-98bcbe10fa81).*

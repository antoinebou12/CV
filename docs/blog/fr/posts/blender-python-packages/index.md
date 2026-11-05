# Installer des paquets Python pour les add-ons Blender (Windows, Blender 4.2+)

> pip dans le Python embarqué de Blender — dossier modules utilisateur, thread d’arrière-plan, popups.

- Page HTML: https://antoineboucher.info/CV/blog/fr/posts/blender-python-packages/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/posts/blender-python-packages/index.md
- Publié: 2025-02-08
- Mis à jour: 2026-05-22
- Tags: Blender, Python, Pip, Addons
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)Les add-ons qui demandent **NumPy**, **meshio** ou **requests** butent sur le **Python de Blender**. Petit installateur ciblant `sys.executable`, dossier `scripts/modules`, thread d’arrière-plan (Blender 4.2+, Windows).

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

- [Rack skate CAO → contreplaqué](https://antoineboucher.info/CV/blog/fr/posts/skate-rack-cad-to-object/)
- [Figurines IA](https://antoineboucher.info/CV/blog/fr/posts/ai-figurines-3d-printing/)

---

*Article [Medium](https://medium.com/@antoine.boucher012/a-method-to-install-python-packages-for-add-ons-plugins-in-blender-windows-blender-4-2-98bcbe10fa81).*

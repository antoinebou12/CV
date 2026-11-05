# novatorem : Des données musicales à un widget SVG

> Ce fork novatorem produit des widgets musicaux depuis des services externes. Un orchestrateur Flask gère le rendu; Spotify et Last.fm ont des modules…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/novatorem/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/novatorem/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/antoinebou12/novatorem
- Licence: Unlicense
- Révision inspectée: 5496fe08e19da0da1042236b2600e77b6df39f5d

## Résumé

Ce fork novatorem produit des widgets musicaux depuis des services externes. Un orchestrateur Flask gère le rendu; Spotify et Last.fm ont des modules distincts. La pochette fournit une image et des couleurs au SVG.

**Pourquoi il existe:** Générateur dynamique mettant à jour le profil GitHub avec l'écoute Spotify en temps réel.

**Cas d’usage:** Personnalisation dynamique de profil GitHub via webhooks.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Python | 81.61 |
| Jinja | 16.06 |
| HTML | 1.64 |
| Dockerfile | 0.64 |
| Procfile | 0.04 |

## Fonctions et composants

- **Fournisseur et présentation** — api/orchestrator.py contient Flask et les fonctions de rendu. Les modules des fournisseurs sont à côté. La configuration pilote modèles et palettes, séparant l’accès propre au service de l’apparence du SVG.
- **Traitement de la pochette** — ImageData récupère la pochette une fois par objet et réutilise les octets pour le base64 et les palettes ColorThief. load_image_with_fallback essaie l’image, un remplacement, puis des couleurs par défaut en cas d’échec.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Spotify ou Last.fm → Données du fournisseur
- Données du fournisseur → Orchestrateur Flask
- Orchestrateur Flask → Pochette et palette de repli
- Pochette et palette de repli → Réponse SVG

```mermaid
flowchart LR
  n0["Spotify ou Last.fm"]
  n1["Données du fournisseur"]
  n2["Orchestrateur Flask"]
  n3["Pochette et palette de repli"]
  n4["Réponse SVG"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
```

**Un parcours dans le code:** Suivez ImageData._fetch vers get_base64 et get_palette. Réutiliser les octets évite des téléchargements répétés dans cet objet, sans constituer un cache persistant entre requêtes.

## Limites et points à vérifier

La récupération d’image désactive actuellement la vérification TLS avec verify=False. Ce point doit être corrigé avant de s’appuyer sur des pochettes distantes en production.

## Fichiers à lire

- [api/orchestrator.py](https://github.com/antoinebou12/novatorem/blob/master/api/orchestrator.py)
- [api/spotify.py](https://github.com/antoinebou12/novatorem/blob/master/api/spotify.py)
- [api/lastfm.py](https://github.com/antoinebou12/novatorem/blob/master/api/lastfm.py)



# FlashGames : Une page statique autour d’un lecteur Flash

> FlashGames conserve de petits jeux Flash dans une collection web. La page choisit un SWF et héberge Ruffle. Le fichier du jeu et l’interface HTML qui…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/flashgames/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/flashgames/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Dépôt: https://github.com/antoinebou12/FlashGames
- Licence: MIT
- Révision inspectée: 7ee14ee2c3029c3b797d22f7594d04c4c900441c

## Résumé

FlashGames conserve de petits jeux Flash dans une collection web. La page choisit un SWF et héberge Ruffle. Le fichier du jeu et l’interface HTML qui l’entoure restent deux éléments distincts.

**Pourquoi il existe:** Archive de préservation de jeux ActionScript/Flash des années 2010.

**Cas d’usage:** Préservation numérique de créations historiques.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| HTML | 100 |

## Fonctions et composants

- **Sélection et lecteur** — index.html inclut le script Ruffle, un sélecteur et un conteneur de lecture. La sélection modifie l’état de la page avant de charger le SWF choisi. Les styles et icônes viennent de CDN, sans compilation frontend locale.
- **Fichiers de jeux conservés** — Le dépôt conserve les SWF à côté de la page. Ruffle fournit la couche d’exécution compatible avec le navigateur; la page ne réécrit pas les jeux en source JavaScript.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Sélecteur de jeu → État de la page
- État de la page → Lecteur Ruffle
- SWF choisi → Lecteur Ruffle

```mermaid
flowchart LR
  n0["Sélecteur de jeu"]
  n1["État de la page"]
  n2["Lecteur Ruffle"]
  n3["SWF choisi"]
  n0 --> n1
  n1 --> n2
  n3 --> n2
```

**Un parcours dans le code:** Suivez updateHash depuis le sélecteur vers le lecteur. Cette distinction aide au diagnostic: un problème de sélection relève de la page, tandis qu’un comportement de jeu non pris en charge peut relever du lecteur.

## Limites et points à vérifier

La compatibilité doit être vérifiée jeu par jeu. Les scripts externes influencent aussi la disponibilité, même si la page est statique.

## Fichiers à lire

- [index.html](https://github.com/antoinebou12/FlashGames/blob/main/index.html)
- [README.md](https://github.com/antoinebou12/FlashGames/blob/main/README.md)


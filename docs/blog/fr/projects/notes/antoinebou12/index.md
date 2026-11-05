# antoinebou12 : Comment le profil GitHub est assemblé

> Ce dépôt contient le README de mon profil GitHub. Il combine du Markdown, des images, des widgets intégrés et des mises à jour planifiées. Le profil…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/antoinebou12/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/antoinebou12/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/antoinebou12/antoinebou12
- Licence: GPL-3.0
- Révision inspectée: c519c6b47b35d3d391167aa43b6cf6cafe7d0435

## Résumé

Ce dépôt contient le README de mon profil GitHub. Il combine du Markdown, des images, des widgets intégrés et des mises à jour planifiées. Le profil lui-même ne contient pas de serveur applicatif.

**Pourquoi il existe:** Workflow automatisé de rendu de métriques et SVG pour profil GitHub dynamique.

**Cas d’usage:** Génération automatique d'assets de profil.

## Fonctions et composants

- **README et ressources** — README.md est le document visible du profil. Les dossiers images, models et profile-3d-contrib regroupent des ressources associées. GitHub affiche le document, tandis que certains services liés produisent leurs propres images.
- **Modifications planifiées** — Le workflow update-readme récupère des statistiques LeetCode, construit des liens de badges et remplace le texte entre des marqueurs du README. D’autres workflows concernent le graphique de contributions, les liens et Pages.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Statistiques externes → GitHub Actions
- GitHub Actions → Section délimitée du README
- Section délimitée du README → Profil GitHub

```mermaid
flowchart LR
  n0["Statistiques externes"]
  n1["GitHub Actions"]
  n2["Section délimitée du README"]
  n3["Profil GitHub"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
```

**Un parcours dans le code:** Dans update-readme.yml, suivez la réponse HTTP jusqu’aux chaînes de badges, puis au remplacement entre marqueurs. Si un marqueur manque, ce remplacement n’a pas lieu.

## Limites et points à vérifier

Les services de badges peuvent tomber en panne ou devenir périmés. Un graphique de profil présente les données d’une source, sans mesurer indépendamment la qualité des contributions.

## Fichiers à lire

- [README.md](https://github.com/antoinebou12/antoinebou12/blob/master/README.md)
- [.github/workflows/update-readme.yml](https://github.com/antoinebou12/antoinebou12/blob/master/.github/workflows/update-readme.yml)
- [.github/workflows/github-profile-3d-contrib.yml](https://github.com/antoinebou12/antoinebou12/blob/master/.github/workflows/github-profile-3d-contrib.yml)



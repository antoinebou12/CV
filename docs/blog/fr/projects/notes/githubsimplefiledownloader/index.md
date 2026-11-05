# GithubSimpleFileDownloader : Une extension liée à la structure des pages

> Cette extension archivée tentait d’ajouter des boutons de téléchargement aux explorateurs de dépôts. Son implémentation GitHub montre la fragilité d’une…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/githubsimplefiledownloader/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/githubsimplefiledownloader/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/antoinebou12/GithubSimpleFileDownloader
- Révision inspectée: dfdd7966db41841e272eddfeefe80332feab161d

## Résumé

Cette extension archivée tentait d’ajouter des boutons de téléchargement aux explorateurs de dépôts. Son implémentation GitHub montre la fragilité d’une intégration fondée sur le DOM d’un autre site plutôt que sur une interface stable.

**Pourquoi il existe:** Extension de navigateur injectant un bouton de téléchargement direct de fichier unique dans GitHub et GitLab.

**Cas d’usage:** Téléchargement immédiat d'un fichier isolé sans cloner le dépôt entier.

## Cas d’utilisation

Une extension Chrome qui ajoute un lien de téléchargement et la taille de chaque fichier dans GitHub, GitLab et Bitbucket.

- **Ajouter des icônes aux listes** (Visiteur de dépôt, Site d’hébergement Git): manifest.json injecte inject_github.js, inject_gitlab.js ou inject_bitbucket.js selon le site ; chaque script ajoute une icône-lien à chaque ligne (td.content, td.tree-item-file-name ou tr.iterable-item).
- **Télécharger un seul fichier** (Visiteur de dépôt, Site d’hébergement Git): Le script réécrit le lien blob en URL brute (raw.githubusercontent.com sur GitHub, /raw/ sur GitLab), récupère le texte et pose une URL d’objet Blob avec l’attribut download.
- **Afficher la taille du fichier** (Visiteur de dépôt, Site d’hébergement Git): Sur GitHub, getFileURLDocument() charge la page du fichier avec XMLHttpRequest et changeFileSize() copie la ligne Bytes/KB/MB dans un span près de l’icône.
- **Ouvrir un dossier par l’icône** (Visiteur de dépôt, Site d’hébergement Git): Les chemins sans extension sont traités comme des dossiers : l’icône renvoie alors à la page du dossier au lieu de télécharger.

### Scénario : Récupérer un seul fichier de config sur GitHub

1. Charger l’extension dans Chrome (Manifest V2, scripts de contenu pour github.com, gitlab.com et bitbucket.org).
2. Ouvrir la liste de fichiers d’un dépôt sur github.com ; inject_github.js attend que document.readyState soit complete.
3. Une petite icône GitHub et une taille s’affichent à côté de chaque fichier.
4. Cliquer sur l’icône du fichier : le contenu brut est enregistré sous le nom du fichier.
5. Si les icônes n’apparaissent pas, actualiser la page comme le conseille le README ; son titre signale aussi que l’extension ne fonctionne plus.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| JavaScript | 97.74 |
| CSS | 2.26 |

## Fonctions et composants

- **Injection dans la page** — Le script GitHub attend que le document soit prêt, trouve les cellules td.content et insère icônes, liens et tailles. Des scripts distincts visent GitLab et Bitbucket. Chaque adaptateur dépend du balisage du site.
- **Téléchargement du fichier brut** — Le script transforme un lien de fichier en lien brut, récupère le texte et crée un téléchargement Blob. Ce parcours textuel ne doit pas être supposé préserver tous les fichiers binaires.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Page du dépôt → Script injecté
- Script injecté → Extraction des liens du DOM
- Extraction des liens du DOM → Requête du fichier brut
- Requête du fichier brut → Lien de téléchargement Blob

```mermaid
flowchart LR
  n0["Page du dépôt"]
  n1["Script injecté"]
  n2["Extraction des liens du DOM"]
  n3["Requête du fichier brut"]
  n4["Lien de téléchargement Blob"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
```

**Un parcours dans le code:** Partez de querySelectorAll('td.content') et examinez les positions des nœuds utilisés pour trouver le lien. Une modification du tableau peut casser ce parcours avant toute requête réseau.

## Limites et points à vérifier

Le README indique explicitement que l’extension ne fonctionne pas. Il s’agit d’une implémentation historique, sans recommandation d’usage actuelle.

## Fichiers à lire

- [manifest.json](https://github.com/antoinebou12/GithubSimpleFileDownloader/blob/master/manifest.json)
- [src/inject/inject_github.js](https://github.com/antoinebou12/GithubSimpleFileDownloader/blob/master/src/inject/inject_github.js)
- [src/inject/inject_gitlab.js](https://github.com/antoinebou12/GithubSimpleFileDownloader/blob/master/src/inject/inject_gitlab.js)



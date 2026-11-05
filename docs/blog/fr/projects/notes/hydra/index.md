# hydra : Une application Electron entre plusieurs processus

> Ce fork Hydra est un lanceur desktop avec Electron et React. Sa compilation comprend aussi un module natif et un composant RPC Python. Ces frontières…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/hydra/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/hydra/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/antoinebou12/hydra
- Licence: MIT
- Révision inspectée: e769e3b398c039a9e3d9977dbb1e5aa70776732e

## Résumé

Ce fork Hydra est un lanceur desktop avec Electron et React. Sa compilation comprend aussi un module natif et un composant RPC Python, chacun avec sa chaîne d’outils.

**Pourquoi il existe:** Application de bureau orchestrant métadonnées et gestion de ludothèque.

**Cas d’usage:** Lanceur et gestionnaire de jeux open source.

## Cas d’utilisation

Une copie de Hydra Launcher, ludothèque Electron qui télécharge, lance, compte le temps de jeu et synchronise les sauvegardes.

- **Constituer sa ludothèque** (Joueur, API et nuage Hydra): Les gestionnaires IPC de src/main/events/library (add-game-to-library, add-custom-game-to-library, assign-game-to-collection) gèrent la ludothèque locale ; les événements catalogue récupèrent fiches et illustrations.
- **Télécharger et mettre en file** (Joueur, Torrents et hébergeurs): Les torrents passent par python_rpc/main.py avec libtorrent, tandis que services/hosters gère des hébergeurs directs comme Gofile, Mediafire et Pixeldrain ; les événements torrenting gèrent la file.
- **Ajouter des sources** (Joueur, Torrents et hébergeurs): Les événements download-sources ajoutent, retirent et synchronisent les listes de sources qui alimentent les options de téléchargement.
- **Lancer et mesurer le temps** (Joueur): process-watcher.ts compare les processus en cours aux exécutables connus pour noter le temps de jeu ; sous Linux, umu.ts et wine-prefix.ts préparent Proton ou Wine.
- **Sauvegarder dans le nuage** (Joueur, API et nuage Hydra): Ludusavi.backupGame() exécute le binaire ludusavi fourni pour réunir les sauvegardes, et les services cloud-save les téléversent, les comparent et les restaurent avec Hydra Cloud.
- **Débloquer des succès** (Joueur, API et nuage Hydra): services/achievements repère et lit les fichiers de succès locaux, les fusionne avec les données distantes et affiche des notifications.

### Scénario : De la fiche du catalogue à la sauvegarde dans le nuage

1. Installer Node.js avec Yarn, Python 3.9+ (pip install -r requirements.txt) et Rust, puis lancer yarn ; postinstall compile hydra-native.
2. Ouvrir un jeu dans le catalogue et l’ajouter à la ludothèque.
3. Choisir une option de téléchargement ; le processus RPC Python lance le torrent et la page des téléchargements affiche la progression.
4. Lancer le jeu ; la surveillance des processus repère l’exécutable et compte le temps de jeu.
5. Fermer le jeu et synchroniser ; ludusavi copie les fichiers de sauvegarde et le service cloud-save les téléverse.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| TypeScript | 81.85 |
| SCSS | 10.64 |
| Rust | 6.46 |
| Python | 0.55 |
| JavaScript | 0.49 |
| HTML | 0.01 |
| NSIS | 0 |

## Fonctions et composants

- **Processus principal et affichage** — package.json dirige Electron vers out/main/index.js. Des vérifications TypeScript distinctes couvrent les parties node et web. Electron-Vite compile l’application, tandis que React et ses bibliothèques appartiennent à l’affichage.
- **Modules natifs et Python** — build:native lance un script de module natif. build:python-rpc prépare python_rpc séparément et les paquets de plateforme utilisent ces parcours. Installer les dépendances JavaScript ne constitue donc pas toute la compilation de livraison.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Interface React → Frontière Electron
- Frontière Electron → Services du processus principal
- Services du processus principal → Module natif
- Services du processus principal → Composant RPC Python

```mermaid
flowchart LR
  n0["Interface React"]
  n1["Frontière Electron"]
  n2["Services du processus principal"]
  n3["Module natif"]
  n4["Composant RPC Python"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n2 --> n4
```

**Un parcours dans le code:** Partez des scripts et distinguez compilation de l’interface, module natif et paquet Python. Examinez ensuite l’API entre processus pour une fonction donnée; les dépendances seules n’indiquent pas son propriétaire.

## Limites et points à vérifier

Cette note décrit la structure d’un fork et conserve le crédit d’origine. Elle ne revendique pas la création du lanceur et ne vérifie pas ses sources de téléchargement.

## Fichiers à lire

- [package.json](https://github.com/antoinebou12/hydra/blob/main/package.json)
- [electron.vite.config.ts](https://github.com/antoinebou12/hydra/blob/main/electron.vite.config.ts)
- [README.md](https://github.com/antoinebou12/hydra/blob/main/README.md)



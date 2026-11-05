# retroarch-web-games : Préparer un émulateur pour un serveur web statique

> retroarch-web-games est une ancienne configuration conteneur autour de RetroArch web. Le dépôt réunit des fichiers d’exécution navigateur, des scripts…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/retroarch-web-games/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/retroarch-web-games/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/antoinebou12/retroarch-web-games
- Licence: MIT
- Révision inspectée: 71b41f91e252873023336b14d4582aa1ac5e2b44

## Résumé

retroarch-web-games est une ancienne configuration conteneur autour de RetroArch web. Le dépôt réunit des fichiers d’exécution navigateur, des scripts et une image conteneur. Héberger le lecteur et fournir les jeux sont deux responsabilités distinctes.

**Pourquoi il existe:** Émulateur RetroArch conteneurisé en WebAssembly exécutable dans tout navigateur moderne.

**Cas d’usage:** Émulation de jeux rétro dans le navigateur sans installation.

## Cas d’utilisation

Image Docker qui héberge le lecteur web RetroArch derrière nginx, avec des dossiers de jeux récupérés à la construction.

- **Installer RetroArch web** (Auto-hébergeur, Sources de fichiers): setup_retroarch.sh télécharge la version emscripten de la veille sur buildbot.libretro.com, l’extrait dans /var/www/html et décompresse le bundle du frontend.
- **Télécharger les jeux** (Auto-hébergeur, Sources de fichiers): InternetArchive.py (typer, rich, requests) parcourt en parallèle les pages d’archives listées pour les fichiers .zip et .7z et les range sous downloads/<nom du système>.
- **Trier les jeux par lettre** (Auto-hébergeur): sort_mkdir.sh déplace chaque fichier dans un sous-dossier 0-9 ou A-Z ; le Dockerfile l’exécute pour chaque dossier de système Nintendo.
- **Lancer le conteneur** (Auto-hébergeur): docker-compose up -d construit l’image et relie le port 8080 à nginx ; entrypoint.sh régénère les listes .index-xhr avant de lancer nginx.
- **Jouer dans le navigateur** (Joueur web): Le joueur ouvre http://localhost:8080, choisit un cœur et charge un jeu dans la page RetroArch Web Player fournie par la version nightly (le dépôt en garde une copie, index.html, que le Dockerfile ne copie pas).
- **Publier l’image multi-arch** (Auto-hébergeur): .github/workflows/retroarch-web-games.yaml construit avec Docker Buildx pour amd64, arm64 et arm/v7 et pousse antoinebou12/retroarch-web-games sur Docker Hub.

### Scénario : Héberger un lecteur rétro sur un serveur maison

1. Cloner le dépôt et prévoir la place pour une image d’environ 10 Go, comme le prévient le README.
2. Lancer docker-compose up -d ; la construction exécute setup_retroarch.sh, InternetArchive.py et sort_mkdir.sh.
3. Au démarrage du conteneur, entrypoint.sh indexe les cœurs et le bundle, puis nginx sert le site.
4. Ouvrir http://localhost:8080 et charger un jeu depuis les dossiers downloads triés.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| HTML | 46.67 |
| JavaScript | 23.61 |
| Python | 13.72 |
| Shell | 11.62 |
| Dockerfile | 4.38 |

## Démarrage (commandes du dépôt, non exécutées ici)

### README.md · Warning 

```bash
docker-compose up -d
```


## Fonctions et composants

- **Assemblage du conteneur** — Le Dockerfile prépare l’environnement web et les éléments d’installation. entrypoint.sh pilote le démarrage du conteneur, tandis qu’index.html et libretro.js appartiennent au parcours navigateur.
- **Exécution et contenu** — Le navigateur charge l’émulateur et ses ressources. Les jeux doivent correspondre au cœur et au format attendus. Les scripts de téléchargement constituent un parcours d’acquisition séparé de l’interface web.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Compilation Docker → Fichiers du serveur statique
- Fichiers du serveur statique → Émulateur dans le navigateur
- Jeu fourni par l’utilisateur → Émulateur dans le navigateur

```mermaid
flowchart LR
  n0["Compilation Docker"]
  n1["Fichiers du serveur statique"]
  n2["Émulateur dans le navigateur"]
  n3["Jeu fourni par l’utilisateur"]
  n0 --> n1
  n1 --> n2
  n3 --> n2
```

**Un parcours dans le code:** Lisez Dockerfile avec entrypoint.sh pour distinguer les téléchargements de compilation du service à l’exécution. Une image compilée peut encore manquer du cœur ou des ressources nécessaires au jeu choisi.

## Limites et points à vérifier

Cette archive demande une revue des dépendances et du navigateur. Utilisez seulement des jeux que vous avez le droit d’utiliser; aucun téléchargement de jeu n’est nécessaire pour examiner l’architecture.

## Fichiers à lire

- [Dockerfile](https://github.com/antoinebou12/retroarch-web-games/blob/master/Dockerfile)
- [entrypoint.sh](https://github.com/antoinebou12/retroarch-web-games/blob/master/entrypoint.sh)
- [index.html](https://github.com/antoinebou12/retroarch-web-games/blob/master/index.html)



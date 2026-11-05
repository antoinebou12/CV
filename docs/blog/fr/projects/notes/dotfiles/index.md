# .dotfiles : Un environnement shell en scripts

> Ces dotfiles regroupent la configuration de shell et d’éditeur que j’utilisais sur plusieurs machines. L’installateur transforme ces préférences en…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/dotfiles/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/dotfiles/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Dépôt: https://github.com/antoinebou12/.dotfiles
- Licence: MIT
- Révision inspectée: 52ff3c19bdebfbebf1d9e320fff199044bdf5e13

## Résumé

Ces dotfiles regroupent la configuration de shell et d’éditeur que j’utilisais sur plusieurs machines. L’installateur gère les paquets, les fichiers de configuration et les projets externes.

**Pourquoi il existe:** Installateur idempotent multi-distribution supportant apt, dnf, pacman avec configuration modulaire Zsh et Vim.

**Cas d’usage:** Reproduction instantanée d'un environnement shell optimisé sur tout système Unix.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Shell | 100 |

## Démarrage (commandes du dépôt, non exécutées ici)

### README.md · Installation

```bash
bash install.sh
source install.sh
install_vimrc
```


## Fonctions et composants

- **Installation des paquets** — install.sh lit la distribution dans /etc/os-release, puis choisit apt, pacman, dnf ou yum. exec_root regroupe les commandes nécessitant des privilèges élevés. L’installation des paquets et les changements de configuration se trouvent donc dans le même script.
- **Configuration de l’éditeur et du shell** — Le parcours Vim installe amix/vimrc et applique des réglages locaux, dont les numéros de ligne et la position de l’arborescence. D’autres fonctions installent Oh My Zsh. update.sh et uninstall.sh proposent des points d’entrée de maintenance distincts.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- install.sh → Détection de la distribution
- Détection de la distribution → Paquets système
- Paquets système → Configuration Vim et Zsh

```mermaid
flowchart LR
  n0["install.sh"]
  n1["Détection de la distribution"]
  n2["Paquets système"]
  n3["Configuration Vim et Zsh"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
```

**Un parcours dans le code:** Suivez install_vimrc depuis sa demande de paquets jusqu’au clonage externe, puis aux modifications dans ~/.vim_runtime. Ce parcours distingue les fichiers modifiés par l’installateur de ceux fournis par un autre projet.

## Limites et points à vérifier

Le script modifie des fichiers personnels et exécute des commandes privilégiées. Sauvegardez votre configuration et inspectez chaque fonction avant de l’exécuter sur une machine actuelle.

## Fichiers à lire

- [install.sh](https://github.com/antoinebou12/.dotfiles/blob/main/install.sh)
- [update.sh](https://github.com/antoinebou12/.dotfiles/blob/main/update.sh)
- [uninstall.sh](https://github.com/antoinebou12/.dotfiles/blob/main/uninstall.sh)


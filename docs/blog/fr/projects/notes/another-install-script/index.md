# another-install-script : Un menu d’installation pour le homelab

> another-install-script propose un menu shell pour choisir des opérations système et installer des conteneurs. Les menus et les définitions de services…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/another-install-script/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/another-install-script/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/antoinebou12/another-install-script
- Licence: GPL-3.0
- Révision inspectée: 6e1e193260504106593f6b92bb799aacafdf0e2b

## Résumé

another-install-script propose un menu shell pour choisir des opérations système et installer des conteneurs. Les menus et les définitions de services sont séparés, ce qui évite de placer toutes les commandes dans setup.sh.

**Pourquoi il existe:** Installateur shell interactif (TUI) automatisant le déploiement de conteneurs Docker et de configurations serveur.

**Cas d’usage:** Déploiement rapide de serveurs et d'environnements homelab en une commande.

## Cas d’utilisation

Menu whiptail en Bash qui installe des outils de base et des services Docker Compose sur un serveur Ubuntu personnel.

- **Installer les outils de base** (Admin du serveur): L’entrée Installation de main_setup_menu (src/menu.sh) affiche une liste à cocher : paquets de base, Docker, Cockpit, LXDE, Ansible, Dokku, Vagrant, etc. ; src/install.sh exécute les choix.
- **Déployer des conteneurs** (Admin du serveur, Moteur Docker): Add Container liste les dossiers de containers/ ; chaque <nom>.sh lance docker-compose up -d sur le docker-compose.yml voisin (par exemple containers/gogs/).
- **Ouvrir les ports au pare-feu** (Admin du serveur, Pare-feu UFW): Après l’ajout de conteneurs, manage_firewall_ports_allow_list (src/firewall.sh) lit leurs ports dans config.yml et les autorise ; si system.firewall vaut yes, ufw refuse le reste du trafic entrant sauf SSH, 2222, HTTP et HTTPS.
- **Retirer des conteneurs** (Admin du serveur, Moteur Docker): remove_container_menu affiche les conteneurs installés ; chaque fonction remove_docker_<nom> lance docker-compose down sur ce service.
- **Tout désinstaller** (Admin du serveur, Moteur Docker, Pare-feu UFW): L’entrée Uninstall lance uninstall.sh, qui charge les modules de src/ pour défaire l’installation. L’entrée Backup appelle pour l’instant le même script ; les fonctions de src/backup.sh ne sont pas reliées au menu.

### Scénario : Préparer un VPS avec quelques services auto-hébergés

1. Cloner le dépôt et lancer sudo bash setup.sh ; main_setup_menu s’ouvre car bashmenu vaut yes dans config.yml.
2. Choisir Installation et garder basic et docker cochés ; le choix de docker ouvre ensuite la liste des conteneurs.
3. Cocher des services comme gogs et bookstack ; chaque script lance docker-compose up -d.
4. Laisser l’étape pare-feu autoriser les ports listés dans config.yml et activer ufw.
5. Plus tard, utiliser Remove Container pour arrêter un service avec docker-compose down.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Shell | 93.8 |
| Dockerfile | 3.12 |
| Python | 3.07 |

## Démarrage (commandes du dépôt, non exécutées ici)

### README.md · How to install

```bash
git clone https://github.com/antoinebou13/another-install-script.git
cd another-install-script
sudo bash setup.sh
```

### README.md · Project Structure

```bash
+-- docs
|   +-- vendor
|       +-- ...
|   +-- docs.md
|   +-- generate_docs.md
|   +-- ...
+-- containers
|   +-- $container_name
|   |   |   +-- docker-compose.yml
|   |   |   +-- $container_name.sh
|   |   |   +-- ...
+-- src
```

### README.md · How to run coverage and tests

```bash
cd tests
bash test.sh
```

### README.md · How to run coverage and tests

```bash
cd tests
bash coverage.sh
```

### README.md · How to generate the documentation

```bash
git submodule update --init --recursive
git pull --recurse-submodules
git submodule update --remote
cd docs/generator
chmod +x generate_docs.sh
bash generate_docs.sh ../docs.md
```


## Fonctions et composants

- **Point d’entrée et menus** — setup.sh charge src/menu.sh et appelle main_setup_menu. Le script racine traite les arguments, tandis que le module chargé pilote la navigation. config.yml constitue le fichier de configuration placé à côté du lanceur.
- **Définitions des services** — Le dossier containers contient les éléments d’installation propres aux services. Cette séparation facilite l’ajout de services, mais chaque installation modifie tout de même l’hôte ou son environnement Docker.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- setup.sh → src/menu.sh
- src/menu.sh → Configuration et sélection
- Configuration et sélection → Installation du conteneur

```mermaid
flowchart LR
  n0["setup.sh"]
  n1["src/menu.sh"]
  n2["Configuration et sélection"]
  n3["Installation du conteneur"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
```

**Un parcours dans le code:** Partez de l’appel à main_setup_menu, puis inspectez le service choisi dans containers avant de l’exécuter. Le menu distribue les actions; le service choisi détermine les changements réels.

## Limites et points à vérifier

Le README présente le projet comme un travail en cours et mentionne une ancienne version d’Ubuntu. Ces notes ne prouvent pas sa compatibilité avec un serveur actuel.

## Fichiers à lire

- [setup.sh](https://github.com/antoinebou12/another-install-script/blob/master/setup.sh)
- [src/menu.sh](https://github.com/antoinebou12/another-install-script/blob/master/src/menu.sh)
- [config.yml](https://github.com/antoinebou12/another-install-script/blob/master/config.yml)



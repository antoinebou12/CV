# TCH099 : Un routeur PHP pour les pages et l’API

> TCH099 est une application PHP de démonstration avec un routeur écrit à la main, une API de connexion par session, un client Android et un guide de déploiement Azure, documentés sur son propre site GitHub Pages.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/tch099/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/tch099/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-11-05
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/antoinebou12/TCH099
- Licence: MIT
- Révision inspectée: a7323c88b2ae6c12d89ef685c6a4cf4325218afc

## Résumé

TCH099 est un projet pédagogique qui combine pages frontend statiques et API PHP. Les routes exposent la frontière: certains chemins retournent du HTML, tandis que d’autres appellent des scripts serveur.

**Pourquoi il existe:** Environnement multi-conteneurs isolé avec réseau bridge, persistance MariaDB et interface web.

**Cas d’usage:** Référence d'architecture conteneurisée pour application et base de données.

## Cas d’utilisation

Application web de démonstration en PHP et MariaDB, avec client Android, pour enseigner le routage, les sessions et Azure.

- **Créer un compte** (Utilisateur web/mobile, Base MariaDB): La page d'inscription ou SignupActivity sur Android envoie les données à /api/signup ; api/signup.php appelle registerUser(), qui ajoute le compte à la table Clients créée par db/1create.sql.
- **Se connecter (session)** (Utilisateur web/mobile, Base MariaDB): login.html et LoginActivity envoient le nom d'utilisateur et le mot de passe à /api/login ; api/login.php les vérifie avec loginUser() et ouvre une session PHP, que /api/logout ferme.
- **Afficher une image au hasard** (Utilisateur web/mobile): random-image.html appelle /api/random-image, qui renvoie l'URL d'un chat venant de TheCatAPI ou celle de thispersondoesnotexist.com selon imageType.
- **Saluer selon la langue** (Utilisateur web/mobile): /api/hello-world/$langue répond par une salutation en français, anglais, espagnol ou allemand ; c'est l'exemple d'API minimal.
- **Lister les clients (admin)** (Administrateur, Base MariaDB): La route /admin ne sert admin.html que si isAdmin() est vrai ; la page charge /api/clients, qui lit la table Clients lorsque la session a le rôle admin.

### Scénario : Lancer la démo en local jusqu'à la page admin

1. Remplir DB_HOST et les variables MYSQL_* indiquées dans le README, puis lancer docker-compose up -d --build.
2. Charger le schéma et les données avec python3 db/db.py, ou importer db/1create.sql, 2contraines.sql et 3insert.sql dans phpMyAdmin sur le port 8060.
3. Ouvrir http://localhost:8001/signup, créer un compte, puis se connecter sur /login.
4. Avec un compte admin, ouvrir /admin pour voir la table Clients chargée par /api/clients.
5. Pousser sur main pour que .github/workflows/main_tch099antoine.yml zippe l'application et la déploie sur Azure Web App.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| HTML | 30.29 |
| PHP | 24.43 |
| Java | 24.06 |
| Jupyter Notebook | 9.1 |
| Shell | 7.27 |
| Python | 3.99 |
| Dockerfile | 0.7 |
| CSS | 0.15 |

## Technologies vérifiées

- Docker Compose — docker-compose.yml
- MariaDB — Service image mariadb:latest in docker-compose.yml
- Azure — README and .github/workflows/README.md describe Azure deployment
- REST API — routes.php API routes

## Démarrage (commandes du dépôt, non exécutées ici)

### README.md · Utilisation de Docker

```bash
docker-compose up -d --build
```

### README.md · Initialisation de la base de données

```bash
cd db
python3 -m pip install mysql-connector-python python-dotenv
python3 db.py
```

### scripts/README.md · Ubuntu/Debian

```bash
sudo usermod -aG docker $USER
newgrp docker  # or log out and back in
```

### scripts/README.md · Installing Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
sudo chmod +x /usr/local/bin/docker-compose
```

### scripts/README.md · Verifying Installation

```bash
docker --version
docker run hello-world
docker-compose --version
```

### scripts/README.md · Automated Installation

```bash
curl -fsSL https://raw.githubusercontent.com/yourusername/docker-install/main/install-docker.sh -o install-docker.sh
chmod +x install-docker.sh
sudo ./install-docker.sh
```


## Fonctions et composants

- **Routes des pages** — routes.php charge router.php, associe accueil et connexion aux fichiers frontend et définit les pages 403 et 404. Le callback /admin vérifie explicitement isAdmin avant de choisir la réponse.
- **Scripts API** — Connexion, inscription, déconnexion et user_details ont leurs scripts API. Des routes de démonstration incluent une langue et une image aléatoire. Les scripts traitent les requêtes; le routeur choisit leur destination.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Navigateur ou client mobile → Routeur PHP
- Routeur PHP → Page HTML
- Routeur PHP → Script API
- Script API → Données applicatives

```mermaid
flowchart LR
  n0["Navigateur ou client mobile"]
  n1["Routeur PHP"]
  n2["Page HTML"]
  n3["Script API"]
  n4["Données applicatives"]
  n0 --> n1
  n1 --> n2
  n1 --> n3
  n3 --> n4
```

**Un parcours dans le code:** Comparez GET /login et POST /api/login. Le premier choisit une page; le second lance l’authentification. Les contrôles doivent protéger les opérations API autant que la page administrative.

## Services Compose

| Service | Runtime | Ports | Dépend de |
| --- | --- | --- | --- |
| web | Build from Dockerfile | 8001:80 | db, startup order only |
| db | mariadb:latest | 3306:3306 |  |
| phpmyadmin | phpmyadmin/phpmyadmin | 8060:80 | db, startup order only |

## API


- `POST /api/login`
- `POST /api/signup`
- `POST /api/logout`
- `GET /api/user_details`
- `GET /api/clients`
- `GET /admin`
- `GET, POST /api/hello-world/$langue`
- `GET, POST /api/random-image`

## Limites et points à vérifier

Une démonstration de routes ne constitue pas une revue de sécurité. Sessions, requêtes et secrets de déploiement demandent une inspection distincte avant hébergement public.

## Fichiers à lire

- [routes.php](https://github.com/antoinebou12/TCH099/blob/main/routes.php)
- [router.php](https://github.com/antoinebou12/TCH099/blob/main/router.php)
- [README.md](https://github.com/antoinebou12/TCH099/blob/main/README.md)



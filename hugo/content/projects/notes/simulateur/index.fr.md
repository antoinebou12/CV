---
title: "Simulateur : un jeu de simulation boursière en Django"
date: 2026-11-05T12:00:00-05:00
description: "Simulateur est une plateforme Django où des admins scénarisent un marché et où des équipes échangent des actions simulées en direct."
translationKey: repository-note-simulateur
repository_note: "Simulateur"
---

# Simulateur

<div class="repo-status-row"><span class="repo-badge kind">Application web</span><span class="repo-badge api">API</span><span class="repo-badge docker">Docker</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">Django</span><span class="tag tool">Django REST framework</span><span class="tag tool">Channels</span><span class="tag tool">Daphne</span><span class="tag tool">Celery</span><span class="tag tool">PostgreSQL</span><span class="tag tool">Redis</span><span class="tag tool">MinIO</span><span class="tag tool">Ollama</span><span class="tag tool">Wagtail</span></div>

Simulateur est une plateforme de simulation boursière construite avec Django : un administrateur prépare un scénario avec des entreprises fictives, des actualités et des événements, puis des équipes de joueurs échangent les actions simulées pendant que les cours bougent en temps réel. C’est un dépôt [AlgoÉTS](https://github.com/AlgoETS) pour les groupes qui veulent animer un jeu de marché, avec une interface d’administration qui règle les paramètres et le déroulement de chaque simulation.

## Aperçu {#overview}

Le projet Django se trouve dans `simulateur/`. `simulateur/settings.py` déclare deux applications locales, `simulation` et `backtesting`, et utilise SQLite sauf si `DATABASE_ENGINE=postgresql` est défini.

- **Moteur de prix.** `simulation/logic/simulation_manager.py` garde un `SimulationManager` par simulation. Tant que l’état est `ongoing`, il attend le pas de temps configuré, saute au besoin les heures de fermeture de la Bourse de New York et écrit une chandelle OHLC par action à partir du modèle de bruit choisi (`brownian`, `perlin`, `random_walk`, `fbm`, `random` ou `monte_carlo` dans `logic/noise_patterns/`). Chaque chandelle est enregistrée dans `StockPriceHistory` puis poussée vers la couche WebSocket.
- **Cycle de vie.** `manage.py start_simulation <ids>` passe les simulations à l’état `ongoing`, vérifie leur état toutes les cinq secondes et applique les réglages modifiés. Les états sont initialized, created, published, ongoing, stopped et finished.
- **Mises à jour en direct.** `simulation/channels/consumers.py` sert `ws/simulation/<room>/` et relaie cours, actualités, événements et déclencheurs vers le tableau de jeu.
- **Échanges.** `simulation/api/portfolio.py` traite les ordres d’achat et de vente selon le dernier prix et le solde du portefeuille, et expose positions, rendement et classements.
- **Création de scénarios.** Le tableau de bord admin suit cinq étapes (réglages, entreprises et actions, équipes, événements, révision). `simulation/api/ai_llm.py` peut rédiger actualités, événements, déclencheurs, entreprises ou scénarios complets avec un modèle Ollama (`OLLAMA_MODEL`, `llama3` par défaut).
- **Application de backtesting.** `backtesting/` ajoute une recherche de graphiques, la gestion de stratégies et une page bac à sable, des points d’accès de données nommés pour FMP, CoinGecko et yfinance, ainsi que des tâches Celery pour exécuter les stratégies.

`run.py` relie le tout : il installe les dépendances, applique les migrations, crée un superadmin, charge les CSV de `data/`, puis démarre Daphne (et, au besoin, les simulations et le CMS Wagtail sur le port 8001) dans des fils d’exécution séparés. Dans l’image Docker, `run.sh` exécute les mêmes étapes de migration, de chargement et de superadmin avant `run.py --start-simulation 1`.

## Démarrage {#installation}

Le parcours Docker Compose du README lance Django, Celery, PostgreSQL, un serveur Dragonfly compatible Redis et MinIO. Le fichier Compose et son `.env` se trouvent dans `simulateur/` :

```shell
cd simulateur
cp env-default .env
docker compose --profile all down
docker compose --profile all up -d --build
```

Sans Docker, passez par `run.py` (le README écrit `python3 -m run.py`, mais le script se lance directement) :

```shell
cd simulateur
python3 run.py --install
python3 run.py --start-simulation 1
```

`--install` crée un superadmin de développement local avec l’identifiant d’exemple du README (`admin`/`admin`) et remplit la base ; changez-le avant d’exposer l’application. Pour créer un autre superadmin avec vos propres valeurs :

```shell
python3 manage.py createsuperadmin --username=<nom> --password=<mot-de-passe> --email=<courriel>
```

Les tests Django de `simulation/tests/` se lancent avec `python3 manage.py test`. Les pages Swagger et ReDoc sont servies à `/swagger/` et `/redoc/`.

## Guide du dépôt {#reader-guide}

- `simulateur/run.py` : installation, migrations, données initiales et démarrage de Daphne, des simulations ou du CMS.
- `simulateur/simulateur/` : réglages, routes racines, point d’entrée ASGI (`asgi.py`) et application Celery.
- `simulateur/simulation/logic/` : boucle de simulation, modèles de bruit, courtier et file d’achat et de vente.
- `simulateur/simulation/api/` : vues REST des entreprises, actions, scénarios, gestionnaires de simulation, actualités, événements, déclencheurs, équipes, portefeuilles et génération par IA.
- `simulateur/simulation/channels/` : consommateur WebSocket et routage.
- `simulateur/simulation/models/` : modèles de scénario, entreprise, action, équipe, portefeuille, ordre et réglages.
- `simulateur/simulation/management/commands/` : `start_simulation`, `seed_database` et `createsuperadmin`.
- `simulateur/simulation/templates/` : tableaux de bord admin, jeu, équipe et utilisateur, composés de gabarits partiels.
- `simulateur/simulation/tests/` : tests de l’API, des modèles, de la logique, des canaux et des commandes.
- `simulateur/backtesting/` : vues, API de données, modèles et tâches Celery de backtesting.
- `simulateur/cms/` : un projet Wagtail distinct.
- `simulateur/data/` : données initiales en CSV (entreprises, actions, scénarios, équipes, utilisateurs, événements, déclencheurs …).
- `notebooks/` : prototypes du courtier, des agents, du bruit, des graphiques et des stratégies.
- `docs/diagrams/` : diagrammes PlantUML de cas d’utilisation et de séquence.

## Fonctionnalités {#features}

- créer des entreprises avec leur historique, des actions, des équipes et des profils de joueurs ;
- régler par simulation le pas de temps, le taux de fluctuation, la fermeture hors séance et le modèle de bruit ;
- démarrer, arrêter et terminer les simulations depuis le tableau admin ou en ligne de commande ;
- diffuser chandelles OHLC, actualités, événements et déclencheurs aux joueurs par WebSocket ;
- acheter et vendre des actions selon le solde du portefeuille, puis suivre positions et rendement ;
- classer joueurs et équipes et inviter des joueurs avec un lien d’équipe ;
- rédiger le contenu d’un scénario avec un modèle Ollama local ;
- se connecter avec un compte local ou Google, GitHub, Microsoft et Notion grâce à django-allauth ;
- exposer des vérifications de santé, des métriques Prometheus et une description OpenAPI.

## Limites {#limits}

- Le README indique Django 4.2.13 ; `requirements.txt` fixe Django 5.0.8. Le badge du README annonce Python 3.12, alors que l’image Docker utilise Python 3.10.
- Les cours sont diffusés dans la salle WebSocket `1`, quel que soit l’identifiant de simulation : tel qu’écrit, seule la simulation 1 reçoit les mises à jour en direct.
- Le mode d’échange `dynamic` s’appuie sur `logic/broker.py`, qui importe le module `BuySellQueue` au lieu de la classe et omet l’argument `simulation_manager` ; ce chemin semble inachevé. Le mode par défaut est `static`.
- `logic/noise_patterns/` contient aussi des modèles GBM, Heston, Ornstein-Uhlenbeck et Vasicek que le gestionnaire de simulation ne propose pas.
- `backtesting/batchbacktesting.py` importe des modules `src.data` et `strategies` absents du dépôt.
- Les points d’accès IA exigent un serveur Ollama joignable ; `entrypoint.sh` en démarre un et télécharge un modèle, mais ni le Dockerfile ni le fichier Compose ne l’utilisent.
- Les valeurs par défaut reposent sur des identifiants de démonstration faibles (`admin`/`admin`, `minioadmin`, `postgres`), et `scripts/` contient un certificat et une clé pour localhost.

## Sources {#sources}

- [Dépôt GitHub](https://github.com/AlgoETS/Simulateur)
- [README](https://github.com/AlgoETS/Simulateur/blob/main/README.md)
- [`simulateur/run.py`](https://github.com/AlgoETS/Simulateur/blob/main/simulateur/run.py)
- [`simulateur/simulation/logic/simulation_manager.py`](https://github.com/AlgoETS/Simulateur/blob/main/simulateur/simulation/logic/simulation_manager.py)
- [`simulateur/simulation/urls.py`](https://github.com/AlgoETS/Simulateur/blob/main/simulateur/simulation/urls.py)
- [`simulateur/simulation/api/portfolio.py`](https://github.com/AlgoETS/Simulateur/blob/main/simulateur/simulation/api/portfolio.py)
- [`simulateur/docker-compose.yml`](https://github.com/AlgoETS/Simulateur/blob/main/simulateur/docker-compose.yml)

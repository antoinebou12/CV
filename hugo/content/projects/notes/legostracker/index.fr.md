---
title: "LegosTracker : catalogue LEGO et historique des prix des ensembles"
date: 2026-11-05T12:00:00-05:00
description: "LegosTracker réunit les exports du catalogue Rebrickable, un collecteur Playwright des prix BrickEconomy et des carnets qui modélisent la valeur des sets LEGO."
translationKey: repository-note-legostracker
repository_note: "LegosTracker"
---

# LegosTracker

<div class="repo-status-row"><span class="repo-badge kind">Carnets et données</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">Jupyter</span><span class="tag tool">Playwright</span><span class="tag tool">Pydantic</span><span class="tag tool">pandas</span><span class="tag tool">scikit-learn</span><span class="tag tool">Matplotlib</span><span class="tag tool">BeautifulSoup</span></div>

LegosTracker est un projet de données d’AlgoÉTS qui traite les ensembles LEGO comme un marché : le catalogue Rebrickable dit quels sets, pièces et thèmes existent, et un collecteur BrickEconomy ajoute les prix atteints au fil du temps. Il s’adresse aux collectionneurs et aux curieux de science des données qui veulent explorer le catalogue ou essayer des modèles de prix simples sur un set. L’article [Économie des boîtes LEGO avec science des données]({{< ref "/posts/economics-lego-data-science/index.fr.md" >}}) raconte la démarche avec des graphiques.

## Aperçu {#overview}

`brickeconomy.py` lit les numéros de sets dans `set_list.txt` et pilote une fenêtre Chromium visible avec Playwright. Pour chaque set, il cherche sur BrickEconomy, ouvre la page correspondante et extrait les lignes de graphique intégrées au script de la page : l’historique de valeur va dans `<set>_history.csv` et, s’il existe, la série à quatre bandes de prix dans `<set>_new.csv`. Il lit ensuite les panneaux détails, prix, achat rapide, prédictions, faits et analyse de sous-thème dans des modèles Pydantic et les ajoute à `lego_sets.csv`. `brickeconomy.ipynb` contient le même code avec les commandes d’installation.

`general.ipynb` charge les tables Rebrickable de `datasets/` (couleurs, inventaires, pièces, sets, thèmes et leurs liens) et trace des décomptes groupés. `analyse.ipynb` nettoie `data/lego_sets.csv` et les fichiers `data/001-1_*.csv` du set 001-1, sorti en 1965, ajuste des régressions linéaire et gradient boosting sur l’historique, les projette jusqu’en 2030, lance une simulation Monte Carlo sur les rendements logarithmiques et trace les gains annuels et les quatre bandes de prix. `price.ipynb` part d’un fichier personnel `mycollection.csv`, cherche le prix de détail et la valeur actuelle sur BrickEconomy avec requests et BeautifulSoup, puis écrit `updated_mycollection.csv`.

## Démarrage {#installation}

`brickeconomy.ipynb` installe les dépendances du collecteur :

```shell
pip install playwright asyncio pydantic aiohttp
playwright install
python brickeconomy.py
```

Le script écrit ses CSV dans le répertoire courant ; `analyse.ipynb` les lit dans `data/`. Les carnets ont besoin de pandas, NumPy, Matplotlib, seaborn et scikit-learn (installés par la première cellule d’`analyse.ipynb`), ainsi que de requests et BeautifulSoup pour `price.ipynb` :

```shell
pip install pandas matplotlib seaborn scikit-learn numpy
jupyter notebook
```

## Guide du dépôt {#reader-guide}

- `brickeconomy.py` est le collecteur Playwright des pages de sets BrickEconomy.
- `set_list.txt` liste les numéros de sets à collecter (001-1 à 0016-1 et 002-1).
- `data/` contient les résultats collectés : `lego_sets.csv`, un `_history.csv` par set et `001-1_new.csv`.
- `datasets/` contient les exports Rebrickable en CSV et `.csv.gz` ; le README décrit leurs colonnes et `images/downloads_schema_v3.webp` montre le schéma.
- `general.ipynb` explore le catalogue Rebrickable.
- `analyse.ipynb` nettoie les prix collectés et modélise l’historique du set 001-1.
- `price.ipynb` met à jour la valeur des sets de `mycollection.csv`.

## Fonctionnalités {#features}

- collecter l’historique de valeur, les bandes de prix et les panneaux BrickEconomy d’une liste de sets ;
- explorer les couleurs, inventaires, pièces, sets et thèmes de Rebrickable ;
- comparer les prix collectés entre sets (plus bas, plus haut, moyenne) ;
- ajuster des régressions linéaire et gradient boosting sur l’historique d’un set et les projeter ;
- simuler les prix futurs avec un modèle Monte Carlo sur les rendements logarithmiques ;
- mettre à jour la valeur actuelle d’une collection personnelle.

## Limites {#limits}

- Aucun fichier de dépendances : elles viennent des cellules `!pip install` des carnets.
- Le collecteur dépend de la structure des pages et des sélecteurs CSS de BrickEconomy, ouvre un navigateur visible et s’arrête sur une erreur quand une recherche ne renvoie aucun lien.
- Les fichiers produits sont écrits dans le répertoire courant, pas dans `data/` : il faut les déplacer avant d’exécuter `analyse.ipynb`.
- Les données collectées couvrent neuf sets ; les modèles de prix portent sur un seul set (001-1) et servent d’illustration, pas de prévision.
- `price.ipynb` ne lit que le premier tableau de la page de recherche BrickEconomy et définit une constante `TAX_RATE` qu’il n’utilise jamais.
- Les exports Rebrickable sont un instantané daté ; aucun script ne les met à jour.

## Sources {#sources}

- [Dépôt GitHub](https://github.com/AlgoETS/LegosTracker)
- [README](https://github.com/AlgoETS/LegosTracker/blob/main/README.md)
- [`brickeconomy.py`](https://github.com/AlgoETS/LegosTracker/blob/main/brickeconomy.py)
- [`analyse.ipynb`](https://github.com/AlgoETS/LegosTracker/blob/main/analyse.ipynb)
- [`general.ipynb`](https://github.com/AlgoETS/LegosTracker/blob/main/general.ipynb)
- [`price.ipynb`](https://github.com/AlgoETS/LegosTracker/blob/main/price.ipynb)
- [Exploring the data of LEGO history](https://github.com/hevalhazalkurt/exploring_the_data_of_LEGO_history), cité dans le README

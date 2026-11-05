---
title: "Kelly_RM : expériences sur le critère de Kelly pour dimensionner les positions"
date: 2026-11-05T12:00:00-05:00
description: "Kelly_RM regroupe des carnets d’AlgoÉTS qui simulent les mises de Kelly et estiment les chances de gain d’un backtest RSI pour en tirer une fraction de Kelly."
translationKey: repository-note-kelly-rm
repository_note: "Kelly_RM"
---

# Kelly_RM

<div class="repo-status-row"><span class="repo-badge kind">Carnets</span><span class="repo-badge algorithm">Critère de Kelly</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">Jupyter</span><span class="tag tool">backtesting.py</span><span class="tag tool">pandas</span><span class="tag tool">NumPy</span><span class="tag tool">httpx</span><span class="tag tool">Altair</span><span class="tag tool">seaborn</span></div>

Kelly_RM est un dépôt de recherche d’AlgoÉTS sur la gestion du risque avec le critère de Kelly, la règle qui fixe la taille d’une mise à partir de la probabilité de gain et du rapport de gain. Le README à la racine est vide ; le code associe une simulation de pile ou face à un carnet qui backteste une stratégie RSI, mesure les chances de gain par titre et en tire une fraction de Kelly. Il s’adresse à qui veut voir le comportement de la formule avant de l’appliquer à une stratégie.

## Aperçu {#overview}

`Kelly_game/betting_strategies.py` définit `BaseGame`, un jeu répété de pile ou face avec une pièce biaisée. Les sous-classes ne décident que de la mise : `Kelly` mise la fraction optimale de la richesse, `KellyWithAnEstimate` attend dix lancers puis mise selon la fréquence observée, `ConstantDollar` mise un montant fixe et `BetLikeADummy` mise gros après trois piles. La classe trace l’évolution de la richesse, simule la distribution des taux de croissance et compare la croissance espérée selon la fraction misée, avec le point de Kelly en repère. `Kelly_game/Playing the Game.ipynb` fait jouer les quatre stratégies côte à côte ; il se présente comme le code d’accompagnement d’une vidéo sur le critère de Kelly.

`sandbox/Main strategy.ipynb` transpose l’idée au trading. Il télécharge des historiques de prix avec `src/data.py` (fonctions Financial Modeling Prep et Binance appuyées sur `src/request_api.py`), coupe chaque série en trois ans d’entraînement et une suite inédite, puis optimise `RsiOscillator` (`src/strategy.py`) avec backtesting.py. À partir des transactions obtenues, il calcule par titre la probabilité de gain ainsi que la moyenne et la variance des gains et des pertes, garde les titres présents dans les deux périodes et applique f* = (p·b − q)/b avec b = gain moyen / perte moyenne.

## Démarrage {#installation}

La description du projet en français, `docs/README.md`, donne l’étape d’installation :

```shell
pip install -r requirements.txt
jupyter notebook
```

Définissez `FMP_API_KEY` (et `BINANCE_API_KEY` pour la fonction Binance) dans l’environnement ; `src/config.py` les lit. Les carnets importent aussi des paquets absents de `requirements.txt`, comme `pandas_ta`, `scipy`, `sympy` et `altair` ; `environment.yml` est un export conda complet qui ajoute `pandas-ta` et SciPy, sans couvrir tous les imports.

## Guide du dépôt {#reader-guide}

- `Kelly_game/betting_strategies.py` contient le jeu de pile ou face et ses stratégies de mise.
- `Kelly_game/Playing the Game.ipynb` compare les stratégies avec des graphiques Altair.
- `sandbox/Main strategy.ipynb` enchaîne l’optimisation RSI, l’estimation des chances et la fraction de Kelly.
- `src/data.py`, `src/request_api.py` et `src/config.py` récupèrent les prix chez FMP et Binance.
- `src/strategy.py` définit les stratégies backtesting.py `Ema` et `RsiOscillator`.
- `src/signal.py` trace des lignes de support et de résistance avec trendln et un seuil de R².
- `docs/README.md` est la description du projet ; `docs/Kelle_complement.pdf` est un article de référence sur la stratégie optimale en incertitude de paramètres, par approche Monte Carlo.
- `docs/notebook/strategy.ipynb` est un carnet vide.

## Fonctionnalités {#features}

- stratégies Kelly, Kelly estimé, montant constant et « mise forte après des piles » sur une pièce simulée ;
- graphiques de richesse, histogrammes de taux de croissance et croissance espérée selon la fraction misée ;
- historiques d’actions et de cryptomonnaies FMP et chandelles de contrats à terme Binance avec httpx ;
- recherche par grille des paramètres RSI avec carte de chaleur seaborn ;
- statistiques de probabilité de gain et de taille des gains et pertes par titre, en entraînement et en données inédites ;
- fraction de Kelly pour chaque titre retenu.

## Limites {#limits}

- Le `README.md` à la racine est vide. `docs/README.md` décrit des limites de risque dans `config.py`, un ajustement à la volatilité, une interface utilisateur et un script principal ; rien de cela n’existe dans le code, et `src/config.py` ne contient que les clés d’API et les URL de base.
- Les dépendances sont incomplètes : `pandas_ta`, `trendln`, `fmp_python`, `scikit-learn`, `scipy`, `sympy` et `altair` sont importés sans figurer dans `requirements.txt`.
- `sandbox/Main strategy.ipynb` ajoute un chemin Windows codé en dur à `sys.path` et appelle la fonction de prix des cryptomonnaies pour des symboles d’actions du S&P 500. Il utilise `DataFrame.append`, retiré de pandas 2, et ses filtres de cohérence valent −1, ce qui les désactive.
- Dans `src/strategy.py`, la stratégie `Ema` calcule sa moyenne à 150 périodes avec le paramètre de 80 périodes.
- Aucun test n’existe, même si `pytest` figure dans `requirements-dev.txt`.
- Les résultats dépendent de l’état des carnets et de données d’API en direct ; le dépôt ne les conserve pas.

## Sources {#sources}

- [Dépôt GitHub](https://github.com/AlgoETS/Kelly_RM)
- [Description du projet (`docs/README.md`)](https://github.com/AlgoETS/Kelly_RM/blob/main/docs/README.md)
- [`Kelly_game/betting_strategies.py`](https://github.com/AlgoETS/Kelly_RM/blob/main/Kelly_game/betting_strategies.py)
- [`sandbox/Main strategy.ipynb`](https://github.com/AlgoETS/Kelly_RM/blob/main/sandbox/Main%20strategy.ipynb)
- [`src/data.py`](https://github.com/AlgoETS/Kelly_RM/blob/main/src/data.py)
- [`src/strategy.py`](https://github.com/AlgoETS/Kelly_RM/blob/main/src/strategy.py)

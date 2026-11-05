# Kelly_RM : expériences sur le critère de Kelly pour dimensionner les positions

> Kelly_RM regroupe des carnets d’AlgoÉTS qui simulent les mises de Kelly et estiment les chances de gain d’un backtest RSI pour en tirer une fraction de Kelly.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/kelly-rm/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/kelly-rm/index.md
- Publié: 2026-11-05
- Mis à jour: 2026-11-05
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/AlgoETS/Kelly_RM


## Cas d’utilisation

Carnets et utilitaires pour estimer les chances de gain par backtest et dimensionner les positions selon Kelly.

- **Simuler le jeu de Kelly** (Chercheur quantitatif): BaseGame (Kelly_game/betting_strategies.py) joue des lancers de pièce biaisée ; Kelly, KellyWithAnEstimate, ConstantDollar et BetLikeADummy fixent la mise, et Playing the Game.ipynb trace richesse et taux de croissance avec Altair.
- **Télécharger l’historique** (Chercheur quantitatif, API de données marché): src/data.py encapsule les points d’accès historical-price-full de Financial Modeling Prep et les chandelles Binance ; src/request_api.py envoie les requêtes avec httpx et src/config.py lit les clés dans l’environnement.
- **Optimiser une stratégie RSI** (Chercheur quantitatif): sandbox/Main strategy.ipynb sépare chaque série en trois ans d’entraînement et une suite inédite, puis balaie les bornes et la fenêtre de RsiOscillator avec backtesting.py et affiche une carte de chaleur seaborn.
- **Estimer les chances par titre** (Chercheur quantitatif): À partir des transactions de chaque backtest, le carnet calcule par titre la probabilité de gain, la moyenne et la variance des gains et des pertes, sur les deux périodes, et garde les titres présents dans les deux.
- **Calculer la fraction de Kelly** (Chercheur quantitatif): La section Kelly Criterion applique f* = (p·b − q)/b avec b = gain moyen / perte moyenne et enregistre le résultat dans une colonne Kelly_Fraction.

### Scénario : Dimensionner des positions RSI selon Kelly

1. Lancer pip install -r requirements.txt, ajouter les paquets manquants du carnet (pandas_ta, scipy, sympy) et définir FMP_API_KEY dans l’environnement.
2. Ouvrir sandbox/Main strategy.ipynb ; il lit les symboles du S&P 500 sur Wikipédia et télécharge dix historiques avec src/data.py.
3. Séparer chaque série en trois ans d’entraînement et une période inédite.
4. Optimiser RsiOscillator avec Backtest.optimize et lire la carte de chaleur des paramètres.
5. Calculer par titre la probabilité de gain et la taille des gains et pertes sur les deux périodes, puis la fraction de Kelly des titres retenus.



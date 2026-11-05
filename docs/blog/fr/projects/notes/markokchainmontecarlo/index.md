# MarkokChainMonteCarlo : backtests par Monte Carlo et chaîne de Markov

> Carnets d’AlgoÉTS qui simulent les prix d’AAPL par Monte Carlo et chaîne de Markov, puis backtestent une stratégie qui s’en sert face à l’achat-conservation.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/markokchainmontecarlo/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/markokchainmontecarlo/index.md
- Publié: 2026-11-05
- Mis à jour: 2026-11-05
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/AlgoETS/MarkokChainMonteCarlo


## Cas d’utilisation

Carnets qui simulent les prix d’AAPL par Monte Carlo et chaîne de Markov, puis backtestent une stratégie qui s’en sert.

- **Séparer les prix en 2023** (Chercheur quantitatif, API de marché FMP): mcmc.ipynb et backtest.ipynb téléchargent l’historique complet d’AAPL avec get_historical_price_full_stock et le coupent au 2023-01-01 en prices_before_january_2023 et prices_after_january_2023.
- **Simuler des trajectoires** (Chercheur quantitatif): monte_carlo_simulation tire des chocs quotidiens à partir de la dérive et de la volatilité des rendements logarithmiques ; mcmc.ipynb ajoute des variantes à volatilité glissante et à chocs extrêmes, sur 364 jours et 1 000 ou 10 000 trajectoires.
- **Simuler une chaîne de Markov** (Chercheur quantitatif): Les clôtures d’entraînement sont réparties en tranches de 10 $ de 0 à 200 ; pandas.crosstab construit la matrice de transition normalisée et markov_chain_simulation tire une suite de tranches.
- **Backtester MCMCStrategy** (Chercheur quantitatif): backtest.ipynb exécute MCMCStrategy (stop de 5 %, prise de profit tirée d’une trajectoire simulée) et BuyAndHoldStrategy avec backtesting.py : 10 000 en encaisse, commission de 0,2 %, ordres exclusifs, sur les deux périodes.
- **Ajuster une tendance linéaire** (Chercheur quantitatif): La section Linear Regression de mcmc.ipynb ajuste une LinearRegression scikit-learn sur l’indice des jours des deux périodes avec un train_test_split 80/20.

### Scénario : Comparer MCMCStrategy et l’achat-conservation sur AAPL

1. Installer les paquets de la commande pip du README et mettre sa propre clé dans la cellule FMP_API_KEY.
2. Ouvrir backtest.ipynb et télécharger l’historique d’AAPL avec get_historical_price_full_stock.
3. Couper les données au 2023-01-01 et construire la matrice de transition des tranches de prix sur la première partie.
4. Créer les objets Backtest de MCMCStrategy et BuyAndHoldStrategy sur les deux périodes et appeler run().
5. Tracer le résultat ; output/MCMCStrategy.html est un graphique backtesting.py enregistré pour MCMCStrategy.



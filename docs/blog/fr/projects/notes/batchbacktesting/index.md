# BatchBacktesting : comparer des simulations de stratégie

> BatchBacktesting exécute des backtests Python sur plusieurs instruments en conservant les hypothèses et les résultats visibles.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/batchbacktesting/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/batchbacktesting/index.md
- Publié: 2026-10-24
- Mis à jour: 2026-10-24
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/AlgoETS/BatchBacktesting


## Cas d’utilisation

Carnets d'AlgoÉTS qui testent en parallèle des stratégies d'indicateurs sur le S&P 500 et des cryptos, avec CSV et graphiques.

- **Constituer l'univers de titres** (Chercheur en stratégie, Liste S&P 500 (Wiki)): get_SP500() lit la table des symboles du S&P 500 sur Wikipédia avec pandas.read_html, et get_all_crypto() renvoie une liste fixe de paires crypto comme BTCUSD et ETHUSD.
- **Télécharger les cours** (Chercheur en stratégie, API de cours FMP): process_instrument appelle le point historical-price-full de FMP pour les actions, ou sa variante crypto, avec la clé FMP_API_KEY lue dans l'environnement par src/config.py.
- **Tester une stratégie en lot** (Chercheur en stratégie, API de cours FMP): run_backtests(tickers, strategy=EMA, num_threads=12, generate_plots=True) lance backtesting.py sur chaque titre dans un pool de fils et écrit output/raw/<Stratégie>/<titre>-<début>-<fin>.csv.
- **Toutes stratégies, un titre** (Chercheur en stratégie): run_backtests_strategies(["BMO"], STRATEGIES_STR) soumet chaque stratégie définie dans src/strategies.py (EMA, RSI, MACD, bandes de Bollinger, ADX, TRIX…) pour les instruments donnés.
- **Comparer au buy & hold** (Chercheur en stratégie): analyse.ipynb charge output/raw/<Stratégie>/*.csv, classe les instruments selon Return [%] et trace les cinq meilleurs face au Buy & Hold Return [%] avec matplotlib.
- **Ouvrir les graphiques HTML** (Chercheur en stratégie): Avec generate_plots=True, plot_results enregistre chaque graphique backtesting.py dans output/charts/<Stratégie>/<titre>-<début>-<fin>.html ; le dépôt contient déjà ceux de 23 stratégies.

### Scénario : Tester l'EMA sur le S&P 500

1. Installer les dépendances avec pip install -r requirements.txt et définir FMP_API_KEY dans l'environnement (voir .env.exemple).
2. Lancer jupyter notebook et ouvrir batch.ipynb.
3. Exécuter la cellule tickers = get_SP500() puis run_backtests(tickers, strategy=EMA, num_threads=12, generate_plots=True).
4. Consulter output/EMA-<début>-<fin>.csv pour les résultats combinés et output/charts/EMA/ pour un graphique HTML par titre.
5. Ouvrir analyse.ipynb et exécuter la section EMA pour voir les meilleurs rendements et les comparer au buy and hold.



# BullETS : une bibliothèque Python pour backtester des stratégies

> BullETS est une bibliothèque Python d’AlgoÉTS pour écrire des stratégies boursières et les backtester sur les données de Financial Modeling Prep.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/bullets/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/bullets/index.md
- Publié: 2026-11-05
- Mis à jour: 2026-11-05
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/AlgoETS/BullETS


## Cas d’utilisation

Bibliothèque Python pour écrire et backtester des stratégies boursières sur les données de Financial Modeling Prep.

- **Écrire une stratégie** (Auteur de stratégie): On hérite de Strategy (src/bullets/strategy.py) et on redéfinit on_start, on_resolution et on_finish ; le constructeur valide les dates, la résolution, le solde, le glissement et les frais.
- **Lancer un backtest** (Auteur de stratégie, API de marché FMP): Runner.start (src/bullets/runner.py) parcourt les moments de marché ouverts (fins de semaine, fériés américains et hors-heures exclus), appelle la stratégie et les ordres en attente, puis journalise solde final, frais et profit.
- **Passer des ordres** (Auteur de stratégie, API de marché FMP): Portfolio (src/bullets/portfolio/portfolio.py) exécute les ordres au marché à un prix ajusté selon le haut du jour, plus des frais fixes, et vérifie les ordres stop et à cours limité à chaque résolution.
- **Lire cours et états financiers** (Auteur de stratégie, API de marché FMP): FmpDataSource (src/bullets/data_source/data_source_fmp.py) met en cache les cours quotidiens, horaires ou à la minute et lit les états financiers et listes de symboles de l’API FMP.
- **Calculer des indicateurs** (Auteur de stratégie, API de marché FMP): Indicators (src/bullets/data_indicators/indicators.py) calcule SMA, WMA, EMA, MACD, RSI, écart type et bandes de Bollinger à partir des cours des jours de marché.
- **Tester et publier le paquet** (GitHub Actions, API de marché FMP): python-pr.yml et python-merge.yml lancent flake8 et unittest avec le secret FMP_TOKEN (couverture envoyée à Codecov après fusion) ; python-publish.yml publie le paquet sur PyPI avec twine à chaque version.

### Scénario : Backtester un achat quotidien d’AAPL

1. Créer un environnement virtuel, lancer pip install BullETS et obtenir une clé d’API Financial Modeling Prep.
2. Hériter de Strategy et faire appeler self.portfolio.market_order("AAPL", 5) dans on_resolution.
3. Créer FmpDataSource(clé, Resolution.DAILY) et la stratégie du 2019-03-05 au 2019-04-22 avec un solde de départ de 5 000, comme dans le README.
4. Appeler Runner(strategy).start() ; chaque jour ouvert exécute l’ordre au prix avec glissement, plus les frais.
5. Lire le journal : encaisse initiale, solde final, encaisse finale, frais payés, profit en pourcentage et appels FMP restants.



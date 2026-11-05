# Prévoir des cours boursiers avec des simulations Monte Carlo

> Bandes Monte Carlo forward sur AAPL — couverture hold-out, percentiles, différence avec MCMC.

- Page HTML: https://antoineboucher.info/CV/blog/fr/posts/predicting-stock-prices-monte-carlo/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/posts/predicting-stock-prices-monte-carlo/index.md
- Publié: 2024-05-14
- Mis à jour: 2026-05-22
- Tags: Python, Finance, Monte Carlo, Backtesting
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)En trading, on raisonne en **fourchettes**. Monte Carlo **forward** sur clôtures Apple : dérive et vol avant 2023, bande 5e–95e vs hold-out 2023.

## Monte Carlo forward vs MCMC

| Outil | Question |
|-------|----------|
| Monte Carlo ici | « Quelle ampleur de swing sous GBM simple ? » |
| MCMC | « Quelle loi colle aux prix observés ? » |

Repo : [AlgoETS/MarkokChainMonteCarlo](https://github.com/AlgoETS/MarkokChainMonteCarlo).

## Split train / hold-out

Couper au **2023-01-01**, estimer rendements log sur train, simuler chemins.

![Séries train et hold-out](images/img-001.png)

## Cœur de simulation

Rendements log → drift/vol → chocs gaussiens → `exp(...)`.

Code complet : [Medium](https://medium.com/@antoine.boucher012/predicting-stock-prices-with-monte-carlo-simulations-0884ef32c35b).

![Bande de percentiles](images/img-005.png)

## Limites

Vol constante, pas de sauts, une seule action — pas un signal d’achat.

## Bilan

Monte Carlo = largeur du **risque modèle** ; backtest = PnL d’une règle.

## Articles liés

- [MarketWatch Python](https://antoineboucher.info/CV/blog/fr/posts/marketwatch-python-trading/)
- [Backtesting multi-indicateurs](https://antoineboucher.info/CV/blog/fr/posts/multiple-indicators-backtesting/)

---

*[Medium](https://medium.com/@antoine.boucher012/predicting-stock-prices-with-monte-carlo-simulations-0884ef32c35b).*

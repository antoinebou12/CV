# Expérimentation des indicateurs technique avec Python et Backtesting

> BatchBacktesting EMA/MACD — lecture des extrêmes, pas conseil de trading.

- Page HTML: https://antoineboucher.info/CV/blog/fr/posts/experimentation-indicateurs-backtesting/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/posts/experimentation-indicateurs-backtesting/index.md
- Publié: 2024-05-14
- Mis à jour: 2026-05-22
- Tags: Python, Trading, Backtesting
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)Batch **EMA** et **MACD** avec [BatchBacktesting](https://github.com/AlgoETS/BatchBacktesting) — FMP et Binance. Ce billet explique le runner et comment lire des rendements extrêmes sans les prendre pour une stratégie live.

## Rôle du projet

Screening massif : CSV + graphiques optionnels sous `output/`. Pas un gestionnaire de portefeuille.

## Exemple de lecture

| Ticker | Rendement | Réflexion |
|--------|-----------|-----------|
| BTCBUSD | +293 % | Vol crypto |
| BTTBUSD | -99 % | Liquidité non modélisée |

![Graphique exemple](images/img-001.png)

Code détaillé : [GitHub BatchBacktesting](https://github.com/AlgoETS/BatchBacktesting) et [Medium FR](https://medium.com/@antoine.boucher012/exp%C3%A9rimentation-des-indicateurs-technique-avec-python-et-backtesting-828bf93e92cc).

## Bilan

Utile pour l’**humilité**, dangereux en pilote auto.

## Articles liés

- [Backtesting multi-tickers](https://antoineboucher.info/CV/blog/fr/posts/multiple-indicators-backtesting/)
- [Monte Carlo](https://antoineboucher.info/CV/blog/fr/posts/predicting-stock-prices-monte-carlo/)

---

*[Medium](https://medium.com/@antoine.boucher012/exp%C3%A9rimentation-des-indicateurs-technique-avec-python-et-backtesting-828bf93e92cc).*

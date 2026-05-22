---
post_kind: article
title: Expérimentation des indicateurs technique avec Python et Backtesting
date: 2024-05-14T20:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "BatchBacktesting EMA/MACD — lecture des extrêmes, pas conseil de trading."
translationKey: experimentation-indicateurs-backtesting
tags:
  - Python
  - Trading
  - Backtesting
canonicalURL: "https://medium.com/@antoine.boucher012/exp%C3%A9rimentation-des-indicateurs-technique-avec-python-et-backtesting-828bf93e92cc"
---

Batch **EMA** et **MACD** avec [BatchBacktesting](https://github.com/AlgoETS/BatchBacktesting) — FMP et Binance. Ce billet explique le runner et comment lire des rendements extrêmes sans les prendre pour une stratégie live. **[English version]({{< ref "/posts/experimentation-indicateurs-backtesting/index.md" >}})**.

<!--more-->

## Rôle du projet

Screening massif : CSV + graphiques optionnels sous `output/`. Pas un gestionnaire de portefeuille.

## Exemple de lecture

| Ticker | Rendement | Réflexion |
|--------|-----------|-----------|
| BTCBUSD | +293 % | Vol crypto |
| BTTBUSD | -99 % | Liquidité non modélisée |

![Graphique exemple](./img-001.png)

Code détaillé : [GitHub BatchBacktesting](https://github.com/AlgoETS/BatchBacktesting) et [Medium FR](https://medium.com/@antoine.boucher012/exp%C3%A9rimentation-des-indicateurs-technique-avec-python-et-backtesting-828bf93e92cc).

## Bilan

Utile pour l’**humilité**, dangereux en pilote auto.

## Articles liés

- [Backtesting multi-tickers]({{< ref "/posts/multiple-indicators-backtesting/index.fr.md" >}})
- [Monte Carlo]({{< ref "/posts/predicting-stock-prices-monte-carlo/index.fr.md" >}})

---

*[Medium](https://medium.com/@antoine.boucher012/exp%C3%A9rimentation-des-indicateurs-technique-avec-python-et-backtesting-828bf93e92cc).*

---
post_kind: article
title: "Prévoir des cours boursiers avec des simulations Monte Carlo"
date: 2024-05-14T09:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "Bandes Monte Carlo forward sur AAPL — couverture hold-out, percentiles, différence avec MCMC."
translationKey: predicting-stock-prices-monte-carlo
tags:
  - Python
  - Finance
  - Monte Carlo
  - Backtesting
canonicalURL: "https://medium.com/@antoine.boucher012/predicting-stock-prices-with-monte-carlo-simulations-0884ef32c35b"
---

En trading, on raisonne en **fourchettes**. Monte Carlo **forward** sur clôtures Apple : dérive et vol avant 2023, bande 5e–95e vs hold-out 2023. **[English version]({{< ref "/posts/predicting-stock-prices-monte-carlo/index.md" >}})**.

<!--more-->

## Monte Carlo forward vs MCMC

| Outil | Question |
|-------|----------|
| Monte Carlo ici | « Quelle ampleur de swing sous GBM simple ? » |
| MCMC | « Quelle loi colle aux prix observés ? » |

Repo : [AlgoETS/MarkokChainMonteCarlo](https://github.com/AlgoETS/MarkokChainMonteCarlo).

## Split train / hold-out

Couper au **2023-01-01**, estimer rendements log sur train, simuler chemins.

![Séries train et hold-out](./img-001.png)

## Cœur de simulation

Rendements log → drift/vol → chocs gaussiens → `exp(...)`.

Code complet : [Medium](https://medium.com/@antoine.boucher012/predicting-stock-prices-with-monte-carlo-simulations-0884ef32c35b).

![Bande de percentiles](./img-005.png)

## Limites

Vol constante, pas de sauts, une seule action — pas un signal d’achat.

## Bilan

Monte Carlo = largeur du **risque modèle** ; backtest = PnL d’une règle.

## Articles liés

- [MarketWatch Python]({{< ref "/posts/marketwatch-python-trading/index.fr.md" >}})
- [Backtesting multi-indicateurs]({{< ref "/posts/multiple-indicators-backtesting/index.fr.md" >}})

---

*[Medium](https://medium.com/@antoine.boucher012/predicting-stock-prices-with-monte-carlo-simulations-0884ef32c35b).*

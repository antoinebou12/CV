---
post_kind: article
title: "Backtest d’indicateurs techniques sur plusieurs tickers avec Python"
date: 2024-05-30T15:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "BatchBacktesting à l’échelle — lire les classements agrégés sans confondre criblage et stratégie."
translationKey: multiple-indicators-backtesting
tags:
  - Python
  - Trading
  - Backtesting
  - Crypto
canonicalURL: "https://medium.com/@antoine.boucher012/multiple-technical-indicators-backtesting-on-multiple-tickers-using-python-a5c933d3f1bf"
---

Même moteur **[BatchBacktesting](https://github.com/AlgoETS/BatchBacktesting)** que l’[expérience indicateurs]({{< ref "/posts/experimentation-indicateurs-backtesting/index.fr.md" >}}), accent sur **beaucoup de tickers** actions + crypto. **[English version]({{< ref "/posts/multiple-indicators-backtesting/index.md" >}})**.

<!--more-->

## Pourquoi beaucoup de symboles

Un seul backtest flatte. Une grille répond : la règle ne marche que sur un héros ?

## Exécution

```python
run_backtests(get_SP500(), strategy=EMA, num_threads=12, generate_plots=True)
run_backtests(get_all_crypto(), strategy=MACD, num_threads=12, generate_plots=True)
```

Résultats locaux dans `output/` — pas versionnés par défaut.

## Lire les extrêmes

Comparer **médiane** et extrêmes avant de dire « MACD bat EMA ».

![Sortie graphique](./img-001.png)

## Bilan

Smoke test de règles — pas déploiement de capital.

## Articles liés

- [Expérimentation indicateurs]({{< ref "/posts/experimentation-indicateurs-backtesting/index.fr.md" >}})
- [MarketWatch Python]({{< ref "/posts/marketwatch-python-trading/index.fr.md" >}})

---

*[Medium](https://medium.com/@antoine.boucher012/multiple-technical-indicators-backtesting-on-multiple-tickers-using-python-a5c933d3f1bf).*

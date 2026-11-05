# Backtest d’indicateurs techniques sur plusieurs tickers avec Python

> BatchBacktesting à l’échelle — lire les classements agrégés sans confondre criblage et stratégie.

- Page HTML: https://antoineboucher.info/CV/blog/fr/posts/multiple-indicators-backtesting/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/posts/multiple-indicators-backtesting/index.md
- Publié: 2024-05-30
- Mis à jour: 2026-05-22
- Tags: Python, Trading, Backtesting, Crypto
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)Même moteur **[BatchBacktesting](https://github.com/AlgoETS/BatchBacktesting)** que l’[expérience indicateurs](https://antoineboucher.info/CV/blog/fr/posts/experimentation-indicateurs-backtesting/), accent sur **beaucoup de tickers** actions + crypto.

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

![Sortie graphique](https://antoineboucher.info/CV/blog/posts/multiple-indicators-backtesting/images/img-001.png)

## Bilan

Smoke test de règles — pas déploiement de capital.

## Articles liés

- [Expérimentation indicateurs](https://antoineboucher.info/CV/blog/fr/posts/experimentation-indicateurs-backtesting/)
- [MarketWatch Python](https://antoineboucher.info/CV/blog/fr/posts/marketwatch-python-trading/)

---

*[Medium](https://medium.com/@antoine.boucher012/multiple-technical-indicators-backtesting-on-multiple-tickers-using-python-a5c933d3f1bf).*

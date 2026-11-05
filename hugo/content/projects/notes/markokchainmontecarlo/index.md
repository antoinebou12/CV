---
title: "MarkokChainMonteCarlo: Monte Carlo and Markov chain backtests"
date: 2026-11-05T12:00:00-05:00
description: "AlgoÉTS notebooks that simulate AAPL prices with Monte Carlo paths and a Markov chain, then backtest a strategy built on them against buy and hold."
translationKey: repository-note-markokchainmontecarlo
repository_note: "MarkokChainMonteCarlo"
---

# MarkokChainMonteCarlo

<div class="repo-status-row"><span class="repo-badge kind">Notebooks</span><span class="repo-badge algorithm">Monte Carlo</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">Jupyter</span><span class="tag tool">backtesting.py</span><span class="tag tool">pandas</span><span class="tag tool">NumPy</span><span class="tag tool">SciPy</span><span class="tag tool">httpx</span><span class="tag tool">scikit-learn</span></div>

MarkokChainMonteCarlo is an AlgoÉTS research repository that backtests investment strategies with stochastic price simulations. Its notebooks estimate Apple (AAPL) price paths with a forward Monte Carlo model and a Markov chain over price ranges, then use those simulations inside a backtesting.py strategy compared with buy and hold. The forward Monte Carlo part is explained step by step in [Predicting Stock Prices with Monte Carlo Simulations]({{< ref "/posts/predicting-stock-prices-monte-carlo/index.md" >}}).

## Overview {#overview}

`mcmc.ipynb` and `backtest.ipynb` share the same opening: an httpx helper downloads the full AAPL daily history from Financial Modeling Prep, and the data is split at 2023-01-01 into a training part and a hold-out part. `monte_carlo_simulation` estimates drift and volatility from log returns and propagates prices with random shocks; `mcmc.ipynb` adds variants with rolling volatility, occasional extreme moves and an optional stochastic drift, and plots 364-day projections with 1,000 or 10,000 paths. A Markov chain is built by cutting training closes into $10 bins from 0 to 200, counting bin-to-bin moves with `pandas.crosstab` and sampling a sequence with `markov_chain_simulation`. The notebook ends with a linear regression on the day index.

`backtest.ipynb` defines `MCMCStrategy`: it simulates paths and Markov states when the backtest starts, buys when the last simulated state is 0, and exits on a 5 % stop loss or when the close reaches a take-profit price drawn from a simulated path. `BuyAndHoldStrategy` serves as the baseline. Both run with 10,000 in cash, a 0.2 % commission and exclusive orders on the two periods. `proto.ipynb` is the first prototype on randomly generated prices, and `output/MCMCStrategy.html` is a saved backtesting.py chart.

## Getting started {#installation}

The README installs the libraries with:

```bash
pip install panda lxml bs4 httpx backtesting yfinance pandas_ta scipy rich TA-Lib
```

`requirements.txt` pins a smaller set (`backtesting`, `httpx`, `numpy`, `pandas`, `pandas-ta`). The notebooks also use Matplotlib and scikit-learn. Put your own Financial Modeling Prep key in the `FMP_API_KEY` cell, then open the notebooks:

```bash
jupyter notebook backtest.ipynb
```

## Repository guide {#reader-guide}

- `mcmc.ipynb` covers data split, Monte Carlo variants, the Markov chain, plots and the linear regression.
- `backtest.ipynb` repeats the simulations and runs `MCMCStrategy` and `BuyAndHoldStrategy`.
- `proto.ipynb` is the prototype on synthetic prices.
- `output/MCMCStrategy.html` is a saved backtest chart.
- `images/` holds the README illustrations.
- `Algo Markov Chain Monte Carlo (MCMC)_.pdf` is a PDF document stored with the code.

## Features {#features}

- AAPL daily history from Financial Modeling Prep, split at 2023-01-01;
- forward Monte Carlo price paths, with rolling-volatility and extreme-move variants;
- Markov chain over $10 price bins with an empirical transition matrix;
- backtesting.py strategy using simulated states and take-profit levels;
- buy and hold baseline on the same periods;
- linear trend fit on the day index.

## Limits {#limits}

- Despite the name, there is no Markov chain Monte Carlo sampler (such as Metropolis–Hastings) in the code; the notebooks combine a forward Monte Carlo simulation with a separate Markov chain.
- `MCMCStrategy` simulates once, at the start of the backtest, over the full series and reads the last element of a fixed state list, so its entry condition does not change from bar to bar. It also starts the chain from a hard-coded state 0.
- The transition matrix only covers closes from 0 to 200, with one open bin above.
- An FMP API key is written in the notebooks; replace it with your own.
- The README install line contains `panda` instead of `pandas`, and `requirements.txt` does not list every import.
- The notebooks do not keep their backtest outputs, and the results depend on random draws without a fixed seed (except in `proto.ipynb`).

## Sources {#sources}

- [GitHub repository](https://github.com/AlgoETS/MarkokChainMonteCarlo)
- [README](https://github.com/AlgoETS/MarkokChainMonteCarlo/blob/main/README.md)
- [`mcmc.ipynb`](https://github.com/AlgoETS/MarkokChainMonteCarlo/blob/main/mcmc.ipynb)
- [`backtest.ipynb`](https://github.com/AlgoETS/MarkokChainMonteCarlo/blob/main/backtest.ipynb)
- [`proto.ipynb`](https://github.com/AlgoETS/MarkokChainMonteCarlo/blob/main/proto.ipynb)

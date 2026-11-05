---
title: "BullETS: a Python library for backtesting trading strategies"
date: 2026-11-05T12:00:00-05:00
description: "BullETS is an AlgoÉTS Python library for writing stock trading strategies and backtesting them on Financial Modeling Prep data."
translationKey: repository-note-bullets
repository_note: "BullETS"
---

# BullETS

<div class="repo-status-row"><span class="repo-badge kind">Library</span><span class="repo-badge workflow">CI</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">aiohttp</span><span class="tag tool">python-dotenv</span><span class="tag tool">unittest</span><span class="tag tool">GitHub Actions</span><span class="tag tool">PyPI</span></div>

BullETS is a Python package for developing algorithmic trading strategies: you subclass a strategy, attach a data source and let a runner replay the market. It is an AlgoÉTS project, published on PyPI under that name, for Python developers who want to test a trading idea on historical prices without first writing the market replay, order handling and data access themselves.

## Overview {#overview}

A strategy extends `Strategy` (`src/bullets/strategy.py`) and overrides three hooks: `on_start`, `on_resolution` and `on_finish`. `Runner` (`src/bullets/runner.py`) builds the list of moments between the start and end dates at daily, hourly or minute resolution, skipping weekends, US market holidays (`src/bullets/utils/holiday_date_util.py`) and hours outside 9:30 to 16:00. At each moment it updates the shared timestamp, calls the strategy, then lets the portfolio check pending orders.

`Portfolio` (`src/bullets/portfolio/portfolio.py`) holds cash, holdings and the transaction log. A market order is filled at a simulated price: at daily resolution the price moves toward the day's high by the slippage percentage (25 % by default), and a flat transaction fee (1 by default) is added. Each `Transaction` records its status (successful, insufficient funds or symbol not found) and logs itself.

Prices and fundamentals come from `FmpDataSource` (`src/bullets/data_source/data_source_fmp.py`), which calls the Financial Modeling Prep API with aiohttp, caches price points per symbol and also reads income statements, balance sheets, cash flow statements and symbol lists. `Indicators` (`src/bullets/data_indicators/indicators.py`) computes moving averages and oscillators from the same source.

## Getting started {#installation}

Register at Financial Modeling Prep for an API key, then install the package in a virtual environment:

```shell
python3 -m venv bot-env
source bot-env/bin/activate
pip install BullETS
```

The README's minimal strategy buys five AAPL shares at each resolution:

```python
from bullets.strategy import Strategy, Resolution
from bullets.runner import Runner
from bullets.data_source.data_source_fmp import FmpDataSource
from datetime import datetime

class MyStrategy(Strategy):
    def on_resolution(self):
        self.portfolio.market_order("AAPL", 5)

resolution = Resolution.DAILY
data_source = FmpDataSource("Insert your key here", resolution)
strategy = MyStrategy(resolution=resolution,
                      start_time=datetime(2019, 3, 5),
                      end_time=datetime(2019, 4, 22),
                      starting_balance=5000,
                      data_source=data_source)
Runner(strategy).start()
```

To work on the library itself, clone it, install it in editable mode and copy `.env.sample` to `.env` with your `FMP_TOKEN`:

```shell
git clone https://github.com/AlgoETS/BullETS
cd BullETS
pip install -e .
python -m unittest discover src/test
```

## Repository guide {#reader-guide}

- `src/bullets/strategy.py` defines the `Strategy` base class and input validation.
- `src/bullets/runner.py` replays market moments and prints the end-of-backtest summary.
- `src/bullets/portfolio/` holds `Portfolio`, `Holding` and `Transaction`.
- `src/bullets/data_source/` contains the data source interface, the FMP implementation and the records for prices and financial statements.
- `src/bullets/data_indicators/indicators.py` implements the technical indicators.
- `src/bullets/utils/` computes US market holidays and market-day offsets.
- `src/bullets/logger.py` provides coloured console logging with adjustable levels.
- `src/test/` contains unittest suites for market hours, holidays, the portfolio and a full strategy run.
- `.github/workflows/` runs lint and tests on pull requests and merges, and publishes to PyPI on release.

## Features {#features}

- strategy hooks for start, each resolution and finish;
- daily, hourly and minute resolutions with US market hours and holidays;
- market, stop and limit orders with slippage and transaction fees;
- end-of-run log with final balance, cash, fees, profit percentage and remaining FMP calls;
- price history, income statements, balance sheets, cash flow statements and symbol lists from FMP, cached per symbol;
- SMA, WMA, EMA, MACD, RSI, standard deviation and Bollinger Bands;
- flake8, unittest and Codecov in CI; PyPI release workflow.

## Limits {#limits}

- The README lists data retrieval, portfolio management and backtesting as "upcoming features", and the version in `setup.py` is 0.1.1; the latest commit in the repository dates from March 2022.
- Slippage only applies at daily resolution; the strategy logs a warning otherwise.
- `buy_limit_order` and `sell_limit_order` add their orders to the stop-order lists, and filled stop or limit orders are not removed from their lists, so they can trigger again at later resolutions.
- The runner loop stops only when it lands exactly on `end_time`, so the end date must be reachable in whole resolution steps.
- Most tests call the live FMP API with `FMP_TOKEN`, so they need a key and network access.
- Only Financial Modeling Prep is implemented as a data source.

## Sources {#sources}

- [GitHub repository](https://github.com/AlgoETS/BullETS)
- [README](https://github.com/AlgoETS/BullETS/blob/develop/README.md)
- [`src/bullets/runner.py`](https://github.com/AlgoETS/BullETS/blob/develop/src/bullets/runner.py)
- [`src/bullets/strategy.py`](https://github.com/AlgoETS/BullETS/blob/develop/src/bullets/strategy.py)
- [`src/bullets/portfolio/portfolio.py`](https://github.com/AlgoETS/BullETS/blob/develop/src/bullets/portfolio/portfolio.py)
- [`src/bullets/data_source/data_source_fmp.py`](https://github.com/AlgoETS/BullETS/blob/develop/src/bullets/data_source/data_source_fmp.py)
- [`src/bullets/data_indicators/indicators.py`](https://github.com/AlgoETS/BullETS/blob/develop/src/bullets/data_indicators/indicators.py)

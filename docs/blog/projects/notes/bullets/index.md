# BullETS: a Python library for backtesting trading strategies

> BullETS is an AlgoÉTS Python library for writing stock trading strategies and backtesting them on Financial Modeling Prep data.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/bullets/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/bullets/index.md
- Published: 2026-11-05
- Updated: 2026-11-05
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/AlgoETS/BullETS


## Use cases

Python library for writing and backtesting stock trading strategies on Financial Modeling Prep data.

- **Write a strategy** (Strategy author): Subclass Strategy in src/bullets/strategy.py and override on_start, on_resolution and on_finish; the constructor validates dates, resolution, balance, slippage and fees.
- **Run a backtest** (Strategy author, FMP market data API): Runner.start in src/bullets/runner.py steps through open market moments (weekends, US holidays and off-hours skipped), calls the strategy and pending orders, then logs final balance, fees and profit.
- **Place market and stop orders** (Strategy author, FMP market data API): Portfolio in src/bullets/portfolio/portfolio.py fills market orders at a slippage price derived from the daily high plus a flat fee, and checks stop and limit orders at each resolution.
- **Fetch prices and statements** (Strategy author, FMP market data API): FmpDataSource in src/bullets/data_source/data_source_fmp.py caches daily, hourly or minute prices and reads income, balance sheet and cash flow statements plus symbol lists from the FMP API.
- **Compute indicators** (Strategy author, FMP market data API): Indicators in src/bullets/data_indicators/indicators.py computes SMA, WMA, EMA, MACD, RSI, standard deviation and Bollinger Bands from data source prices on open market days.
- **Test and publish the package** (GitHub Actions, FMP market data API): python-pr.yml and python-merge.yml run flake8 and unittest with an FMP_TOKEN secret (coverage goes to Codecov on merge); python-publish.yml uploads the sdist to PyPI with twine on release.

### Scenario: Backtest buying AAPL every trading day

1. Create a virtual environment, run pip install BullETS and get an API key from Financial Modeling Prep.
2. Subclass Strategy and make on_resolution call self.portfolio.market_order("AAPL", 5).
3. Build FmpDataSource(key, Resolution.DAILY) and the strategy from 2019-03-05 to 2019-04-22 with a 5,000 starting balance, as in the README.
4. Call Runner(strategy).start(); each open day fills the order at the slippage price plus the transaction fee.
5. Read the log: initial cash, final balance, final cash, fees paid, profit percentage and remaining FMP calls.



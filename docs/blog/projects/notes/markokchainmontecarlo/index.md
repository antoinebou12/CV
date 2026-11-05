# MarkokChainMonteCarlo: Monte Carlo and Markov chain backtests

> AlgoÉTS notebooks that simulate AAPL prices with Monte Carlo paths and a Markov chain, then backtest a strategy built on them against buy and hold.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/markokchainmontecarlo/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/markokchainmontecarlo/index.md
- Published: 2026-11-05
- Updated: 2026-11-05
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/AlgoETS/MarkokChainMonteCarlo


## Use cases

Notebooks that simulate AAPL prices with Monte Carlo and a Markov chain, then backtest a strategy built on them.

- **Split prices at 2023** (Quant researcher, FMP market data API): mcmc.ipynb and backtest.ipynb download the full AAPL history with get_historical_price_full_stock and split it at 2023-01-01 into prices_before_january_2023 and prices_after_january_2023.
- **Simulate Monte Carlo paths** (Quant researcher): monte_carlo_simulation draws daily shocks from the drift and volatility of log returns; mcmc.ipynb adds variants with rolling volatility and occasional extreme moves, run for 364 days with 1,000 or 10,000 paths.
- **Simulate a Markov chain** (Quant researcher): Training closes are cut into $10 bins from 0 to 200; pandas.crosstab builds the normalized transition matrix and markov_chain_simulation samples a sequence of bins.
- **Backtest MCMCStrategy** (Quant researcher): backtest.ipynb runs MCMCStrategy (5% stop loss, take profit drawn from a simulated path) and BuyAndHoldStrategy with backtesting.py: 10,000 cash, 0.2% commission, exclusive orders, on both periods.
- **Fit a linear trend** (Quant researcher): The Linear Regression section of mcmc.ipynb fits scikit-learn LinearRegression on the day index of both periods with an 80/20 train_test_split.

### Scenario: Compare MCMCStrategy with buy and hold on AAPL

1. Install the packages from the README pip command and put your own key in the FMP_API_KEY cell.
2. Open backtest.ipynb and download the AAPL history with get_historical_price_full_stock.
3. Split the data at 2023-01-01 and build the price-bin transition matrix from the earlier part.
4. Create Backtest objects for MCMCStrategy and BuyAndHoldStrategy on both periods and call run().
5. Plot the result; output/MCMCStrategy.html is a saved backtesting.py chart of MCMCStrategy.



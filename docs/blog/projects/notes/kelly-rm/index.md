# Kelly_RM: Kelly criterion experiments for trade sizing

> Kelly_RM holds AlgoÉTS notebooks that simulate Kelly betting and estimate trade odds from RSI backtests to compute a Kelly fraction.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/kelly-rm/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/kelly-rm/index.md
- Published: 2026-11-05
- Updated: 2026-11-06
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/AlgoETS/Kelly_RM
- Inspected revision: faf4eebf51c2b7e00b1ce6ff2fdf4400b63a9bd6


## Use cases

Notebooks and helpers to estimate trade odds from backtests and size positions with the Kelly criterion.

- **Simulate the Kelly coin game** (Quant researcher): BaseGame in Kelly_game/betting_strategies.py plays biased coin flips; Kelly, KellyWithAnEstimate, ConstantDollar and BetLikeADummy set the wager, and Playing the Game.ipynb plots wealth paths and growth rates with Altair.
- **Download price history** (Quant researcher, Market data APIs): src/data.py wraps Financial Modeling Prep historical-price-full endpoints and Binance futures klines; src/request_api.py sends the requests with httpx and src/config.py reads the API keys from the environment.
- **Optimize an RSI strategy** (Quant researcher): sandbox/Main strategy.ipynb splits each series into three training years and an unseen remainder, then grid-searches RsiOscillator bounds and window with backtesting.py and shows a seaborn heatmap.
- **Estimate win odds per ticker** (Quant researcher): From each backtest trade table the notebook computes win probability, mean and variance of win and loss sizes per ticker, on training and unseen data, and keeps tickers present in both.
- **Compute the Kelly fraction** (Quant researcher): The Kelly Criterion section applies f* = (p·b − q)/b with b = mean win size / mean loss size and stores the result in a Kelly_Fraction column.

### Scenario: Size RSI trades with the Kelly criterion

1. Run pip install -r requirements.txt, add the missing notebook packages (pandas_ta, scipy, sympy) and set FMP_API_KEY in the environment.
2. Open sandbox/Main strategy.ipynb; it reads S&P 500 symbols from Wikipedia and downloads ten price histories through src/data.py.
3. Split each series into a three-year training set and an unseen set.
4. Optimize RsiOscillator with Backtest.optimize and read the parameter heatmap.
5. Compute win probability and win/loss sizes per ticker on both sets, then the Kelly fraction for each kept ticker.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Jupyter Notebook | 97.99 |
| Python | 2.01 |



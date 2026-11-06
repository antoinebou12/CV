# BatchBacktesting: comparable strategy runs

> BatchBacktesting runs Python backtests across instruments and keeps strategy assumptions and outputs visible.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/batchbacktesting/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/batchbacktesting/index.md
- Published: 2026-10-24
- Updated: 2026-11-06
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/AlgoETS/BatchBacktesting
- Inspected revision: 6aae4af0733c248ae4c4dec1b25affa942f8037d


## Use cases

AlgoÉTS notebooks that backtest indicator strategies on S&P 500 stocks and cryptos in parallel, with CSV and charts.

- **Build the ticker universe** (Strategy researcher, Wikipedia S&P 500 list): get_SP500() reads the S&P 500 symbol table from Wikipedia with pandas.read_html, and get_all_crypto() returns a fixed list of crypto pairs such as BTCUSD and ETHUSD.
- **Download daily prices** (Strategy researcher, FMP price API): process_instrument calls the FMP historical-price-full endpoint for stocks or the crypto variant, with FMP_API_KEY read from the environment in src/config.py.
- **Backtest one strategy in batch** (Strategy researcher, FMP price API): run_backtests(tickers, strategy=EMA, num_threads=12, generate_plots=True) runs backtesting.py on every ticker in a thread pool and writes output/raw/<Strategy>/<ticker>-<start>-<end>.csv.
- **Run all strategies on a ticker** (Strategy researcher): run_backtests_strategies(["BMO"], STRATEGIES_STR) submits every strategy defined in src/strategies.py (EMA, RSI, MACD, Bollinger Bands, ADX, TRIX…) for the given instruments.
- **Compare returns to buy & hold** (Strategy researcher): analyse.ipynb loads output/raw/<Strategy>/*.csv, ranks instruments by Return [%] and plots the top five against Buy & Hold Return [%] with matplotlib.
- **Open the HTML trade charts** (Strategy researcher): With generate_plots=True, plot_results saves each backtesting.py chart as output/charts/<Strategy>/<ticker>-<start>-<end>.html; the repository already holds charts for 23 strategies.

### Scenario: Test EMA on the S&P 500

1. Install the dependencies with pip install -r requirements.txt and put an FMP_API_KEY in the environment (see .env.exemple).
2. Run jupyter notebook and open batch.ipynb.
3. Run the cell tickers = get_SP500() then run_backtests(tickers, strategy=EMA, num_threads=12, generate_plots=True).
4. Check output/EMA-<start>-<end>.csv for the combined results and output/charts/EMA/ for one HTML chart per ticker.
5. Open analyse.ipynb and run the EMA section to list the top returns and compare them with buy and hold.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| HTML | 99.98 |
| Jupyter Notebook | 0.02 |
| Python | 0 |

## Getting started (repository commands, not run here)

### README.md · Installation

```bash
git clone https://github.com/username/BatchBacktesting.git
cd BatchBacktesting
pip install -r requirements.txt
```




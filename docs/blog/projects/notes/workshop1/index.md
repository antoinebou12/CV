# Workshop1: Python learning notebooks

> Workshop1 is an AlgoETS notebook series that moves from Python fundamentals and APIs to pandas, charts and an EMA exercise.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/workshop1/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/workshop1/index.md
- Published: 2026-10-24
- Updated: 2026-10-24
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/AlgoETS/Workshop1


## Use cases

AlgoÉTS French workshop: Jupyter notebooks from Python basics to APIs, pandas, charts and a 20-day EMA on Apple stock.

- **Set up a Python environment** (Workshop participant, Jupyter or Colab): 0.1_python_environement covers virtualenv, Anaconda and Jupyter Lab; 0.2_jupyter_cloud shows DeepNote and Google Colab, and the README links a Colab copy of the first notebook.
- **Learn Python basics** (Workshop participant, Jupyter or Colab): 1.1_python_basic and 1.2_python_advanced cover variables, control flow, file I/O on monfichier.txt and a small SQLite database (ma_base.db).
- **Call a web API** (Workshop participant, Jupyter or Colab): 2.1_python_api explains REST verbs, status codes, Bearer tokens, API keys and OAuth, with requests and async httpx examples.
- **Clean data with pandas** (Workshop participant): 3.1_python_panda walks through DataFrames, filtering with loc and iloc, missing values, merges, pandas_ta indicators and a polars comparison.
- **Plot an EMA on Apple stock** (Workshop participant, FMP price API): 5.1_project_ema fetches AAPL daily prices from FMP historical-price-full, computes a 20-day EMA with pandas ewm and plots it against the close with Matplotlib; 4.2 adds SMA, RSI and MACD charts.

### Scenario: Follow the workshop up to the EMA project

1. Clone https://github.com/AlgoETS/Workshop1.git and run pip install -r requirements.txt.
2. Start jupyter notebook, or open 1.0-basic/1.1_python_basic.ipynb in Google Colab from the README link.
3. Work through 1.0-basic, 2.0-api and 3.0-data in order.
4. Open 5.0-project/5.1_project_ema.ipynb and replace YOUR_API_KEY with a Financial Modeling Prep key.
5. Run the cells to load AAPL prices into a DataFrame, add EMA_20 and plot the close price with the 20-day EMA.



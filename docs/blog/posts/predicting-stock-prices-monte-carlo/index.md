# Predicting Stock Prices with Monte Carlo Simulations

> Forward Monte Carlo bands for AAPL from historical log returns — hold-out coverage, percentiles, and how that differs from MCMC.

- HTML page: https://antoineboucher.info/CV/blog/posts/predicting-stock-prices-monte-carlo/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/posts/predicting-stock-prices-monte-carlo/index.md
- Published: 2024-05-14
- Updated: 2026-11-05
- Tags: Python, Finance, Monte Carlo, Backtesting
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)Trading is about **ranges**, not one magic price. I used **forward Monte Carlo** on Apple daily closes: estimate log-return drift and volatility before 2023, simulate many paths, then check whether 2023 hold-out prices fell inside a **5th–95th percentile band**.

## Forward Monte Carlo vs MCMC

| Tool | Question it answers |
|------|---------------------|
| **Forward Monte Carlo (this post)** | “How wide could prices swing under a simple GBM-style model?” |
| **MCMC** (e.g. Landauskas & Valakevičius KDE sampling) | “What distribution fits observed prices before simulating?” |

You can combine them: fit with MCMC, explore scenarios with forward paths. This article implements the forward step in Python; [AlgoETS/MarkokChainMonteCarlo](https://github.com/AlgoETS/MarkokChainMonteCarlo) explores MCMC-oriented experiments.

## Setup

Libraries: `pandas`, `numpy`, `httpx`, `matplotlib`, `scipy`, `rich`, optional `backtesting` / `pandas_ta` for related charts. Historical prices via Financial Modeling Prep API helpers in the original notebook.

## Train / hold-out split

Pull full history for `AAPL`, split at **2023-01-01**:

- **Train** — estimate mean/variance of log returns.
- **Hold-out** — compare simulated bands to realized closes.

![Train vs hold-out price series](https://antoineboucher.info/CV/blog/posts/predicting-stock-prices-monte-carlo/images/img-001.png)

The same split for AAPL, GOOGL and MSFT shows how differently the three names moved after January 2023:

![AAPL, GOOGL and MSFT before and after 2023](https://antoineboucher.info/CV/blog/posts/predicting-stock-prices-monte-carlo/images/img-002.png)

## The simulation core

Estimate log returns on train window → daily drift and volatility → draw Gaussian shocks → propagate price with `exp(drift + vol * Z)`.

```python
def monte_carlo_simulation(data, days, iterations):
    if isinstance(data, pd.Series):
        data = data.to_numpy()
    if not isinstance(data, np.ndarray):
        raise TypeError("Data must be a numpy array or pandas Series")

    log_returns = np.log(data[1:] / data[:-1])
    mean = np.mean(log_returns)
    variance = np.var(log_returns)
    drift = mean - (0.5 * variance)
    daily_volatility = np.std(log_returns)

    future_prices = np.zeros((days, iterations))
    current_price = data[-1]
    for t in range(days):
        shocks = drift + daily_volatility * norm.ppf(np.random.rand(iterations))
        future_prices[t] = current_price * np.exp(shocks)
        current_price = future_prices[t]
    return future_prices
```

`norm.ppf(np.random.rand(iterations))` turns uniform draws into standard normal shocks, so each row of `future_prices` is one trading day across every simulated path. The `- 0.5 * variance` term is the Itô correction: without it, the mean of `exp(shock)` would drift upward faster than the historical returns justify.

![Simulated price paths from the training window](https://antoineboucher.info/CV/blog/posts/predicting-stock-prices-monte-carlo/images/img-003.png)

Data download helpers and plotting loops: [Medium original](https://medium.com/@antoine.boucher012/predicting-stock-prices-with-monte-carlo-simulations-0884ef32c35b).

## Reading the output

- **Fan of gray paths** — scenario diversity.
- **Median and mean paths** — central tendency (not identical under skew).
- **5th–95th band** — risk-style interval for “where might price land.”
- **Hold-out dot** — did reality sit inside the band at the aligned horizon?

![Percentile band and simulated paths](https://antoineboucher.info/CV/blog/posts/predicting-stock-prices-monte-carlo/images/img-005.png)

For AAPL, the mean simulated price after 364 days was **$206.63** against a real close of **$192.53** on 2023-12-29: a gap of $14.10, or 7.32 %.

![Mean simulated price against the real 2023-12-29 close](https://antoineboucher.info/CV/blog/posts/predicting-stock-prices-monte-carlo/images/img-006.png)

A later run for AAPL and MSFT, with the 2024 closes as the check, gives wider fans. The MSFT mean missed by about 14 %, which is a reminder that a band built on past volatility says nothing about a re-rating.

![AAPL forecast fan](https://antoineboucher.info/CV/blog/posts/predicting-stock-prices-monte-carlo/images/img-007.png)

![MSFT forecast fan](https://antoineboucher.info/CV/blog/posts/predicting-stock-prices-monte-carlo/images/img-008.png)

Terminal distribution gives **quantile prices** and simple return percentiles vs last train close — useful for “how wrong is the model?” not “buy signal.”

## When not to use GBM Monte Carlo alone

| Limitation | Reality |
|------------|---------|
| Constant vol | Markets cluster volatility |
| No jumps | Earnings gaps exist |
| Single name | Diversification ignored |
| Not a strategy test | Pair with [backtesting posts](https://antoineboucher.info/CV/blog/posts/experimentation-indicateurs-backtesting/) |

## Takeaway

Monte Carlo answers **model risk width** on a hold-out window; backtesting answers **rule PnL**. Keep the questions separate.

## Related posts

- [MarketWatch Python library](https://antoineboucher.info/CV/blog/posts/marketwatch-python-trading/)
- [Multiple indicators backtesting](https://antoineboucher.info/CV/blog/posts/multiple-indicators-backtesting/)

## Reference

- Landauskas, M. & Valakevičius, E. (2011). [*Modelling of Stock Prices by MCMC*](https://ojs.mruni.eu/ojs/intellectual-economics/article/view/817)
- [Investopedia — Monte Carlo basics](https://www.investopedia.com/articles/investing/112514/monte-carlo-simulation-basics.asp)

---

*Originally published on [Medium](https://medium.com/@antoine.boucher012/predicting-stock-prices-with-monte-carlo-simulations-0884ef32c35b). Notebook code: see repo and Medium for full listings.*

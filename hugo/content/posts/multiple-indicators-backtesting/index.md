---
post_kind: article
title: Multiple Technical Indicators Backtesting on Multiple Tickers using Python
date: 2024-05-30T15:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "Scaled BatchBacktesting across stocks and crypto — reading aggregate leaderboards without mistaking screening for a strategy."
translationKey: multiple-indicators-backtesting
tags:
  - Python
  - Trading
  - Backtesting
  - Crypto
canonicalURL: "https://medium.com/@antoine.boucher012/multiple-technical-indicators-backtesting-on-multiple-tickers-using-python-a5c933d3f1bf"
---

Same **[BatchBacktesting](https://github.com/AlgoETS/BatchBacktesting)** engine as the [earlier indicator experiment]({{< ref "/posts/experimentation-indicateurs-backtesting/index.md" >}}), but emphasized at **portfolio scale**: many tickers, two strategies, equities plus crypto, aggregate winners and losers. **[Version française]({{< ref "/posts/multiple-indicators-backtesting/index.fr.md" >}})**.

<!--more-->

## Why run many tickers at once

Single-ticker backtests flatter you. A grid run answers:

- Does this rule only work on one heroic symbol?
- Are disasters clustered in a sector or era?
- Is crypto dominating the leaderboard because volatility is unbounded in the sim?

## Architecture (same as BatchBacktesting)

| Layer | Role |
|-------|------|
| Data adapters | FMP + Binance fetch |
| Strategy objects | `EMA`, `MACD` parameter sets |
| Runner | Thread pool, CSV output, optional plots |
| `output/` | Per-run artifacts — not committed to GitHub by default |

Pre-calculated results are **not** in the upstream repo (too user-specific). You generate locally, then inspect `output/charts/...`.

## Running at scale

```python
run_backtests(get_SP500(), strategy=EMA, num_threads=12, generate_plots=True)
run_backtests(get_SP500(), strategy=MACD, num_threads=12, generate_plots=True)
run_backtests(get_all_crypto(), strategy=EMA, num_threads=12, generate_plots=True)
run_backtests(get_all_crypto(), strategy=MACD, num_threads=12, generate_plots=True)
```

Tune `num_threads` to your machine and API rate limits.

## Reading leaderboard extremes (EMA example)

**High returns** often mix:

- Long bullish windows on leveraged crypto pairs.
- Mean-reversion false signals in sideways stocks (sometimes lucky).
- Parameters tuned implicitly by the default strategy class.

**Deep negatives** flag:

- Illiquid symbols where the sim still trades.
- Trend rules in collapsing sectors.
- Stablecoins or broken pairs treated like normal tickers.

![Summary chart from batch output](./img-001.png)

Before narrating “MACD beats EMA,” compare **median return**, not only top decile.

## Honest limitations

- Not **financial advice**.
- Fees, borrow, halts, and corporate actions are only as good as the data feed + library defaults.
- Past batch output ≠ future edge.

## Takeaway

Use multi-ticker backtests as **smoke tests** for rules — find where they break, not where to deploy capital.

## Related posts

- [Experimentation with indicators]({{< ref "/posts/experimentation-indicateurs-backtesting/index.md" >}})
- [Predicting stock prices with Monte Carlo]({{< ref "/posts/predicting-stock-prices-monte-carlo/index.md" >}})

---

*Originally published on [Medium](https://medium.com/@antoine.boucher012/multiple-technical-indicators-backtesting-on-multiple-tickers-using-python-a5c933d3f1bf). Full code listings: [BatchBacktesting](https://github.com/AlgoETS/BatchBacktesting).*

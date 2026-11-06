---
title: "BatchBacktesting: comparable strategy runs"
date: 2026-10-24T12:00:00-04:00
description: "BatchBacktesting runs Python backtests across instruments and keeps strategy assumptions and outputs visible."
mermaid: true
lastmod: 2026-11-06T04:00:00-05:00
translationKey: repository-note-batchbacktesting
repository_note: "BatchBacktesting"
---

# BatchBacktesting

BatchBacktesting turns a backtest into a repeatable batch: choose instruments, obtain and clean prices, run a strategy, and save comparable results. It is an [AlgoÉTS](https://github.com/AlgoETS) repository; the facts below come from its source files and README as read for the [companion article]({{< ref "/posts/batchbacktesting-engine/index.md" >}}).

## Overview

**Why it exists.** A batch backtest is a small data pipeline, and the project keeps every step visible in Python instead of behind a dashboard.

**Best fit.** Comparing one strategy across many instruments with the same recorded assumptions, then reading the per-instrument and aggregate CSVs side by side.

## Getting started

The README links a published example rather than a one-command install; the runner is the entry point.

- Runner: [`src/BatchBacktesting.py`](https://github.com/AlgoETS/BatchBacktesting/blob/main/src/BatchBacktesting.py) — `process_instrument` selects a stock or crypto price adapter, cleans the data and constructs a `Backtest`.
- Strategies: [`src/strategies.py`](https://github.com/AlgoETS/BatchBacktesting/blob/main/src/strategies.py).
- Analysis helpers: [`src/analyse.py`](https://github.com/AlgoETS/BatchBacktesting/blob/main/src/analyse.py).
- Published AAPL EMA chart (2018-04-04 to 2023-04-03): [output/charts/EMA](https://algoets.github.io/BatchBacktesting/output/charts/EMA/AAPL-2018-04-04-2023-04-03.html).

## Features and components

| Component | What it does |
| --- | --- |
| Instrument runner | Picks the price adapter, cleans observations, runs one `Backtest`, tags the result with instrument and strategy names |
| Worker pool | `ThreadPoolExecutor`, four workers by default for the single-strategy runner; the multi-strategy helper nests an outer pool around inner pools |
| Strategy defaults | 100,000 starting cash, 0.002 commission (0.2%), exclusive orders |
| EMA strategy | 20-, 80- and 150-period EMAs computed; entries compare the 20 and 80 curves; long side closes the prior position and buys with a 90% stop and a 125% target |
| Outputs | Per-instrument CSV, aggregate CSV per strategy, optional HTML chart |

## How the strategies decide {#algorithm}

**EMA crossover.** The default strategy computes exponential moving averages of the close, `EMAₜ = α · Pₜ + (1 − α) · EMAₜ₋₁` with `α = 2 / (n + 1)`: 0.095 for the 20-period average and 0.025 for the 80-period one, so the short average reacts about four times faster. On each bar:

- when EMA 20 crosses above EMA 80, the strategy closes any position and buys, with a stop at 90% and a target at 125% of the close;
- when EMA 80 crosses above EMA 20, it closes and sells short, with a stop at 110% and a target at 75%.

The 150-period average is computed but never used.

**What the exits imply.** With a stop 10% away and a target 25% away, a long trade risks 10 to make 25. Ignoring fees, it breaks even if more than 10 / (10 + 25) ≈ 28.6% of trades reach the target before the stop. Each round trip also pays the 0.2% commission twice, which raises that threshold slightly. Because the next crossover closes the position first, many trades end on a crossover rather than on the stop or the target.

```mermaid
flowchart TD
  B["New bar"] --> C1{"EMA20 crosses above EMA80?"}
  C1 -->|yes| L["Close position, buy: SL 0.90 × close, TP 1.25 × close"]
  C1 -->|no| C2{"EMA80 crosses above EMA20?"}
  C2 -->|yes| S["Close position, sell short: SL 1.10 × close, TP 0.75 × close"]
  C2 -->|no| H["Hold; the broker checks SL and TP"]
```

**The other strategies.** `src/strategies.py` defines twenty-three indicator strategies (RSI, Bollinger Bands, MACD, linear regression, ADX, OBV, Aroon, DEMA, ALMA, SMA …). Most follow the same pattern, and fourteen of them use the same 90/125% and 110/75% exits. Two of them do not test what their names suggest. In `RSI`, `rsi30` and `rsi70` are RSIs computed over 30 and 70 bars, not the 30 and 70 levels, so the strategy trades crossings between three RSI curves. `BollingerBands` uses only the first column of `pandas_ta.bbands`, the lower band.

**Aggregation.** `process_instrument` tags each `Backtest.run()` result with the instrument and the strategy, the runner concatenates them into one CSV per strategy, and `analyse.py` ranks instruments. `get_max_return` groups by instrument and takes `max()` column by column, so the "best" row mixes the best return with the best value of every other column.

## Architecture

```mermaid
flowchart TD
  I["Instrument list and strategy"] --> P["ThreadPoolExecutor"]
  P --> D["Fetch and clean historical data"]
  D --> B["Backtest per instrument"]
  B --> R["Result with Instrument and Strategy"]
  R --> C["Per-instrument CSV"]
  R --> A["Aggregate strategy CSV"]
  B --> H["Optional HTML chart"]
```

## Constraints and checks

- A failed instrument returns `None`; if every instrument fails, the later concatenation has no frames.
- `groupby("Instrument").max()` in `analyse.py` takes each column's maximum independently, so a summary row can mix metrics from different runs. Select a real row by return before quoting its drawdown.
- The defaults do not cover slippage, short availability, delisted securities or corporate actions.
- Worker counts and dates above are code defaults and example dates, not measured throughput or a fixed range.

## Links

- [Repository](https://github.com/AlgoETS/BatchBacktesting)
- [Published example](https://algoets.github.io/BatchBacktesting/)
- [Workshop1]({{< ref "/projects/notes/workshop1/index.md" >}}), the beginner notebooks that lead into this batch runner

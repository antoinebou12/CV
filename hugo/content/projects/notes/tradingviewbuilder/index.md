---
title: "TradingViewBuilder: Pine Script indicators and strategies"
date: 2026-11-05T12:00:00-05:00
description: "TradingViewBuilder collects Pine Script indicators and strategies (EMA, MACD, RSI, Bollinger Bands, RVI …) to paste into TradingView."
translationKey: repository-note-tradingviewbuilder
repository_note: "TradingViewBuilder"
---

# TradingViewBuilder

<div class="repo-status-row"><span class="repo-badge kind">Scripts</span></div>

<div class="repo-tech-badges"><span class="tag tool">Pine Script</span><span class="tag tool">TradingView</span></div>

TradingViewBuilder is a collection of TradingView indicators and strategies written in Pine Script, one file per technique. It is an [AlgoÉTS](https://github.com/AlgoETS) repository for traders who want readable starting points for common technical rules that they can paste into the Pine Editor, apply to a chart and adjust.

## Overview {#overview}

Files ending in `.indicator` declare a `study()` (or `indicator()`) that only plots values. Files ending in `.strategy` declare a `strategy()` that also places `strategy.entry` orders on crossover rules:

| Technique | Strategy rule | Files |
| :-- | :-- | :-- |
| EMA crossover | Long when EMA 9 crosses above EMA 21, short on the opposite cross | `ema.strategy`, `ema.indcator` |
| SMA crossover | Buy when SMA 10 crosses above SMA 20, close on the opposite cross | `mac.strategy` |
| MACD | Long/short on MACD (12, 26) crossing its 9-period signal line | `macd.strategy`, `macd.indicator` |
| RSI | Long when RSI 14 crosses above 30, short when it crosses below 70 | `rsi.strategy`, `rsi.indicator` |
| Bollinger Bands | Long when the close crosses above the lower band (20, 2σ), short below the upper band | `bollingerbands.strategy` |
| Linear regression | Same band rule around a 20-bar linear regression ± 2 standard deviations | `linearregression.strategy`, `linearregression.indicator` |
| Relative Vigor Index | Long/short when RVI (10) crosses its 4-period signal line | `rvi.strategy`, `rvi.indicator` |
| Standard deviation | Bands at close ± 20-bar standard deviation | `standarddeviation.strategy`, `standarddeviation.indicator` |

`TimeSeriesMomentumEffect.strategy` is a larger draft: it lists 60 futures contracts, measures each one's return over 12 × 21 bars, goes long winners and short losers, and sizes positions with a volatility target and a leverage cap.

## Getting started {#installation}

There is nothing to install. The README's steps are:

1. Log in to TradingView and open the **Pine Editor** tab at the bottom of a chart.
2. Copy the contents of a `.indicator` or `.strategy` file from this repository and paste it into the editor.
3. Click **Add to Chart** (and **Save** to keep the script under a name).
4. Use the gear icon next to the script label to change lengths, sources, levels and colours.

## Repository guide {#reader-guide}

- `*.indicator` (and `ema.indcator`): plotting-only versions of EMA, linear regression, MACD, RSI, RVI and standard deviation.
- `*.strategy`: trading versions with entry rules for EMA, SMA crossover (`mac`), MACD, RSI, Bollinger Bands, linear regression, RVI and standard deviation.
- `TimeSeriesMomentumEffect.strategy`: multi-asset time-series momentum draft.
- `README.md`: list of techniques and the TradingView setup steps.
- `docs/about.md`: placeholder page with a heading only.

## Features {#features}

- eight classic technical techniques, most available as both an indicator and a strategy;
- adjustable inputs (`input()`) for every length, multiplier and threshold;
- chart overlays: bands, moving averages, signal lines and overbought/oversold levels;
- a written-out time-series momentum idea with volatility targeting.

## Limits {#limits}

- Most files target Pine Script v4. `mac.strategy` declares `@version=5` but uses v4 calls, and `ema.indcator` declares `@version=4` but uses v5 calls (`indicator`, `input.int`, `ta.ema`); either version header needs changing before they compile.
- `standarddeviation.strategy` compares `close` with `close ± std`; since the bands always sit on either side of the close, the crossover conditions never fire and the strategy places no trades as written.
- `TimeSeriesMomentumEffect.strategy` uses syntax that Pine does not accept (brace-delimited functions, `length()` on arrays), so it reads as pseudocode rather than a runnable script.
- The README calls RVI the "Relative Volatility Index", but the code computes the Relative Vigor Index; `mac.strategy` is not listed in the README, and `ema.indcator` has a typo in its extension.
- Strategies enter and reverse on opposite signals (only `mac.strategy` closes instead); there are no stops, position sizing or commission settings, and the repository contains no backtest results.

## Sources {#sources}

- [GitHub repository](https://github.com/AlgoETS/TradingViewBuilder)
- [README](https://github.com/AlgoETS/TradingViewBuilder/blob/main/README.md)
- [`macd.strategy`](https://github.com/AlgoETS/TradingViewBuilder/blob/main/macd.strategy)
- [`rsi.strategy`](https://github.com/AlgoETS/TradingViewBuilder/blob/main/rsi.strategy)
- [`bollingerbands.strategy`](https://github.com/AlgoETS/TradingViewBuilder/blob/main/bollingerbands.strategy)
- [`TimeSeriesMomentumEffect.strategy`](https://github.com/AlgoETS/TradingViewBuilder/blob/main/TimeSeriesMomentumEffect.strategy)

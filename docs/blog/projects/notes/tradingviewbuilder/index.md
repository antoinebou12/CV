# TradingViewBuilder: Pine Script indicators and strategies

> TradingViewBuilder collects Pine Script indicators and strategies (EMA, MACD, RSI, Bollinger Bands, RVI …) to paste into TradingView.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/tradingviewbuilder/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/tradingviewbuilder/index.md
- Published: 2026-11-05
- Updated: 2026-11-05
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/AlgoETS/TradingViewBuilder


## Use cases

Pine Script indicators and strategies (EMA, MACD, RSI, Bollinger, RVI …) to paste into TradingView.

- **Plot an indicator** (Trader, TradingView): Paste a .indicator file such as rsi.indicator or macd.indicator into the Pine Editor and add it to the chart to plot the series and its levels.
- **Test a crossover strategy** (Trader, TradingView): ema.strategy, mac.strategy and macd.strategy enter on a fast/slow or MACD/signal crossover and reverse or close on the opposite cross.
- **Trade band reversals** (Trader, TradingView): bollingerbands.strategy and linearregression.strategy go long when the close crosses above the lower band and short when it crosses below the upper band.
- **Trade oscillator signals** (Trader, TradingView): rsi.strategy trades RSI crosses of the 30 and 70 levels, and rvi.strategy trades crosses of the Relative Vigor Index and its signal line.
- **Tune script inputs** (Trader, TradingView): Each script declares input() values (lengths, multipliers, levels) that the README says to change from the gear icon on the chart.
- **Sketch a momentum portfolio** (Trader): TimeSeriesMomentumEffect.strategy outlines a 12-month time-series momentum on 60 futures with volatility targeting and a leverage cap; it is a draft, not valid Pine.

### Scenario: Backtest the RSI strategy on a chart

1. Log in to TradingView, open a chart and click the Pine Editor tab.
2. Copy the contents of rsi.strategy and paste it into the editor.
3. Click Add to Chart: Long entries appear when RSI(14) crosses above 30 and Short entries when it crosses below 70.
4. Open the gear icon to change RSI Length, Overbought Level or Oversold Level and compare the trades.
5. Add rsi.indicator in a separate pane to see the oscillator with the same levels.



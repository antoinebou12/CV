---
post_kind: article
title: "Python library for MarketWatch virtual trading"
date: 2026-04-13T10:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "PyPI package marketwatch — Python client for MarketWatch’s virtual stock game, API surface, limits, and how it pairs with backtesting experiments."
translationKey: marketwatch-python-trading
tags:
  - Python
  - MarketWatch
  - Trading
  - Finance
  - Open Source
images:
  - featured.png
---

I wanted to automate chores in MarketWatch’s **virtual stock game** (paper trading, not a real broker). **[marketwatch](https://pypi.org/project/marketwatch/)** on PyPI is the small client I shipped — watchlists, game state, portfolio, orders, leaderboard. **[Version française]({{< ref "/posts/marketwatch-python-trading/index.fr.md" >}})**.

<!--more-->

## Why build this

Course and side projects already used **BatchBacktesting** on historical data — see **[experimentation with indicators]({{< ref "/posts/experimentation-indicateurs-backtesting/index.md" >}})**. MarketWatch’s game is a different beast: **session cookies**, game rules, and leaderboards that change with the semester. A thin Python wrapper beat curl scripts in a notebook.

I also wanted a **documented surface** for teammates: “here is how you list games” beats sharing a gist that rots when the HTML form changes. The package is intentionally small — no ORM, no strategy engine — just HTTP shaped like the site.

## Design choices

| Choice | Reason |
|--------|--------|
| **Class-based client** | One login, many calls in a script |
| **Explicit methods per endpoint** | Easier to grep when MarketWatch changes a path |
| **Docs on GitHub Pages** | PyPI description alone is too short for auth edge cases |
| **No bundled strategies** | Keeps the library neutral; strategies belong in your repo |

## Links

- **Package:** [pypi.org/project/marketwatch](https://pypi.org/project/marketwatch/)
- **Documentation:** [antoinebou12.github.io/marketwatch](https://antoinebou12.github.io/marketwatch/)
- **Source & issues:** [github.com/antoinebou12/marketwatch](https://github.com/antoinebou12/marketwatch)

## What it can do

| Area | Methods (see docs for signatures) |
|------|-----------------------------------|
| **Watchlists** | Create, list, update symbols |
| **Games** | List games, read settings |
| **Portfolio** | Positions, pending orders |
| **Trading** | Buy / sell inside game rules |
| **Social** | Leaderboard for a game |

Useful for **small bots and screening** inside the game — not HFT, not brokerage.

## Quick start

```bash
pip install marketwatch
```

```python
from marketwatch import MarketWatch

mw = MarketWatch("your_username", "your_password")
mw.get_games()
mw.get_price("AAPL")
```

Login edge cases (2FA absent, session expiry) are documented on the site — read before cron-scheduling anything.

![MarketWatch Python client — package branding](./featured.png)

## Limits and responsibility

- **Unofficial API** — HTML/JSON endpoints can change; pin versions and expect breakage.
- **Terms of use** — automation may conflict with MarketWatch rules; use for learning, not abuse.
- **Not financial advice** — paper gains do not validate a strategy; pair with honest backtests on separate data.

For research-style batch runs on many tickers, see **[multiple indicators backtesting]({{< ref "/posts/multiple-indicators-backtesting/index.md" >}})** and **[Monte Carlo risk bands]({{< ref "/posts/predicting-stock-prices-monte-carlo/index.md" >}})**.

## Related posts

- [Experimentation with technical indicators]({{< ref "/posts/experimentation-indicateurs-backtesting/index.md" >}})
- [Economics of LEGO with data science]({{< ref "/posts/economics-lego-data-science/index.md" >}}) — another “Python for curiosity” project

Questions or bugs: [GitHub issues](https://github.com/antoinebou12/marketwatch).

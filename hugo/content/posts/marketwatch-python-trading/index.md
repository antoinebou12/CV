---
post_kind: article
title: "Python library for MarketWatch virtual trading"
date: 2026-04-13T10:00:00-04:00
description: "PyPI package `marketwatch`—a Python client for MarketWatch’s virtual stock game (watchlists, games, portfolio, orders, leaderboard)."
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

I published **[marketwatch](https://pypi.org/project/marketwatch/)** on PyPI: a small Python client for the [MarketWatch](https://www.marketwatch.com) **virtual stock game** (paper trading), not live brokerage access. If you want to script watchlists, pull game or portfolio data, or experiment with automation against the game, it wraps the flows in a straightforward API.

## Links

- **Package:** [pypi.org/project/marketwatch](https://pypi.org/project/marketwatch/)
- **Documentation:** [antoinebou12.github.io/marketwatch](https://antoinebou12.github.io/marketwatch/)
- **Source & issues:** [github.com/antoinebou12/marketwatch](https://github.com/antoinebou12/marketwatch)

## What it can do

- Create and manage **watchlists**
- Read **game** details and settings
- Inspect **portfolio**, positions, and pending orders
- **Buy** and **sell** (in-game)
- Fetch the **leaderboard** for a game

Useful if you are exploring automated strategies or small bots **inside the game’s rules**—see the docs for method names and return shapes.

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

For login edge cases, every method, and examples for orders and watchlists, use the [documentation](https://antoinebou12.github.io/marketwatch/).

![Featured image for the MarketWatch Python library post](./featured.png)

Automation can conflict with a platform’s terms or rate limits; use the library responsibly and check MarketWatch’s own rules if you rely on it for anything non-trivial.

Questions or bugs are welcome on [GitHub](https://github.com/antoinebou12/marketwatch).

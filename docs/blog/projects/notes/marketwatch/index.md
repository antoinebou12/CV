# marketwatch: A client around a virtual trading game

> marketwatch is an archived Python client for MarketWatch’s virtual trading game. It wraps login, game queries and simulated order operations. These are…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/marketwatch/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/marketwatch/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Repository: https://github.com/antoinebou12/marketwatch
- License: Apache-2.0
- Inspected revision: 9a8bd76c464501f249aff141f1e105e7345155c6

## Summary

marketwatch is an archived Python client for MarketWatch’s virtual trading game. It wraps login, game queries and simulated order operations. These are game interactions, not connections to a brokerage account.

**Why it exists:** Robust Python client library scraping and wrapping the MarketWatch virtual stock market game API.

**Best fit:** Automated trading bot development and portfolio backtesting.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Python | 77.68 |
| Jupyter Notebook | 13.22 |
| Jinja | 7.65 |
| Dockerfile | 1.45 |

## Getting started (repository commands, not run here)

### README.md · Installation

```bash
pip install marketwatch
```

### README.md · Installation

```bash
pip install git+https://github.com/antoinebou12/marketwatch.git
```

### README.md · Installation

```bash
git clone https://github.com/antoinebou12/marketwatch.git
```


## Features and components

- **Session and game scope** — MarketWatchGame subclasses MarketWatch and stores a game identifier. Methods such as buy and sell delegate to the base client with that identifier. Ledger and portfolio operations are scoped by the game.
- **Remote dependency** — The client depends on the website’s authentication and response structure. A Python method still existing does not mean its remote counterpart remains accessible. Authentication failure can block otherwise unchanged game methods.

## Architecture

Components and connections verified in the repository.

- Python caller → MarketWatchGame wrapper
- MarketWatchGame wrapper → Base HTTP client
- Base HTTP client → Virtual game service
- Virtual game service → Base HTTP client

```mermaid
flowchart LR
  n0["Python caller"]
  n1["MarketWatchGame wrapper"]
  n2["Base HTTP client"]
  n3["Virtual game service"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n2
```

**One path through the code:** Follow buy from the game wrapper into the base client. The wrapper adds the game ID; session handling and the actual HTTP request happen below it.

## Constraints and checks

The README reports broken login because of CAPTCHA. This historical client should not be presented as a working automated trading integration.

## Files to read

- [marketwatch/game.py](https://github.com/antoinebou12/marketwatch/blob/main/marketwatch/game.py)
- [marketwatch/__init__.py](https://github.com/antoinebou12/marketwatch/blob/main/marketwatch/__init__.py)
- [README.md](https://github.com/antoinebou12/marketwatch/blob/main/README.md)


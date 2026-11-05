---
title: "Simulateur: a Django stock-market simulation game"
date: 2026-11-05T12:00:00-05:00
description: "Simulateur is a Django platform where admins script market scenarios and teams trade simulated stocks with live WebSocket prices."
translationKey: repository-note-simulateur
repository_note: "Simulateur"
---

# Simulateur

<div class="repo-status-row"><span class="repo-badge kind">Web app</span><span class="repo-badge api">API</span><span class="repo-badge docker">Docker</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">Django</span><span class="tag tool">Django REST framework</span><span class="tag tool">Channels</span><span class="tag tool">Daphne</span><span class="tag tool">Celery</span><span class="tag tool">PostgreSQL</span><span class="tag tool">Redis</span><span class="tag tool">MinIO</span><span class="tag tool">Ollama</span><span class="tag tool">Wagtail</span></div>

Simulateur is a stock-market simulation platform built with Django: an admin prepares a scenario with fictional companies, news and events, and teams of players trade the simulated stocks while prices move in real time. It is an [AlgoÉTS](https://github.com/AlgoETS) repository for groups that want to run a market game together, with an admin interface that controls the settings and the flow of each simulation.

## Overview {#overview}

The Django project lives in `simulateur/`. `simulateur/settings.py` registers two local apps, `simulation` and `backtesting`, and uses SQLite unless `DATABASE_ENGINE=postgresql` is set.

- **Price engine.** `simulation/logic/simulation_manager.py` holds one `SimulationManager` per simulation. While the state is `ongoing`, it sleeps for the configured timer step, skips New York market-closed hours if asked, and writes an OHLC candle per stock from the chosen noise model (`brownian`, `perlin`, `random_walk`, `fbm`, `random` or `monte_carlo` in `logic/noise_patterns/`). Each candle is stored as `StockPriceHistory` and pushed to the WebSocket layer.
- **Lifecycle.** `manage.py start_simulation <ids>` sets the simulations to `ongoing`, polls their state every five seconds and applies changed settings. The states are initialized, created, published, ongoing, stopped and finished.
- **Live updates.** `simulation/channels/consumers.py` serves `ws/simulation/<room>/` and relays stock updates, news, events and triggers to the game dashboard.
- **Trading.** `simulation/api/portfolio.py` handles buy and sell orders against the latest price and the portfolio balance, and exposes holdings, performance and leaderboards.
- **Scenario authoring.** The admin dashboard walks through five steps (settings, companies and stocks, teams, events, review). `simulation/api/ai_llm.py` can draft news, events, triggers, companies or whole scenarios with an Ollama model (`OLLAMA_MODEL`, `llama3` by default).
- **Backtesting app.** `backtesting/` adds chart search, strategy management and a sandbox page, data endpoints named for FMP, CoinGecko and yfinance, and Celery tasks for strategy runs.

`run.py` ties it together: it installs requirements, applies migrations, creates a superadmin, seeds the CSV files in `data/`, then starts Daphne (and optionally simulations and the Wagtail CMS on port 8001) in separate threads. In the Docker image, `run.sh` runs the same migrate, seed and superadmin steps before `run.py --start-simulation 1`.

## Getting started {#installation}

The README's Docker Compose path runs Django, Celery, PostgreSQL, a Redis-compatible Dragonfly server and MinIO. The compose file and its `.env` live in `simulateur/`:

```shell
cd simulateur
cp env-default .env
docker compose --profile all down
docker compose --profile all up -d --build
```

Without Docker, use `run.py` (the README writes `python3 -m run.py`, but the script is run directly):

```shell
cd simulateur
python3 run.py --install
python3 run.py --start-simulation 1
```

`--install` creates an `admin`/`admin` superadmin and seeds the database. Another superadmin can be created with:

```shell
python3 manage.py createsuperadmin --username=admin --password=admin --email=admin@admin.com
```

The Django test suite under `simulation/tests/` runs with `python3 manage.py test`. Swagger and ReDoc pages are served at `/swagger/` and `/redoc/`.

## Repository guide {#reader-guide}

- `simulateur/run.py`: install, migrate, seed and start Daphne, simulations or the CMS.
- `simulateur/simulateur/`: settings, URL root, ASGI entry (`asgi.py`) and Celery app.
- `simulateur/simulation/logic/`: simulation loop, noise models, broker and buy/sell queue.
- `simulateur/simulation/api/`: REST views for companies, stocks, scenarios, simulation managers, news, events, triggers, teams, portfolios and AI generation.
- `simulateur/simulation/channels/`: WebSocket consumer and routing.
- `simulateur/simulation/models/`: scenario, company, stock, team, portfolio, order and settings models.
- `simulateur/simulation/management/commands/`: `start_simulation`, `seed_database` and `createsuperadmin`.
- `simulateur/simulation/templates/`: admin, game, team and user dashboards built from partials.
- `simulateur/simulation/tests/`: tests for the API, models, logic, channels and commands.
- `simulateur/backtesting/`: backtesting views, data APIs, models and Celery tasks.
- `simulateur/cms/`: a separate Wagtail project.
- `simulateur/data/`: CSV seed data (companies, stocks, scenarios, teams, users, events, triggers …).
- `notebooks/`: prototypes for the broker, agents, noise, charts and strategies.
- `docs/diagrams/`: PlantUML use-case and sequence diagrams.

## Features {#features}

- create companies with backstories, stocks, teams and user profiles;
- configure the timer step, fluctuation rate, market-hours closing and noise model per simulation;
- start, stop and finish simulations from the admin dashboard or the command line;
- stream OHLC candles, news, events and triggers to players over WebSockets;
- buy and sell stocks within a portfolio balance and follow holdings and performance;
- rank players and teams on leaderboards and invite players with team join links;
- draft scenario content with a local Ollama model;
- sign in with accounts or Google, GitHub, Microsoft and Notion through django-allauth;
- expose health checks, Prometheus metrics and an OpenAPI description.

## Limits {#limits}

- The README lists Django 4.2.13; `requirements.txt` pins Django 5.0.8. The README badge says Python 3.12 while the Docker image uses Python 3.10.
- Price broadcasts are sent to WebSocket room `1` regardless of the simulation id, so only simulation 1 receives live updates as written.
- The `dynamic` trading mode relies on `logic/broker.py`, which imports the `BuySellQueue` module instead of the class and omits the `simulation_manager` argument; that path looks unfinished. The default mode is `static`.
- `logic/noise_patterns/` also contains GBM, Heston, Ornstein-Uhlenbeck and Vasicek models that the simulation manager does not offer.
- `backtesting/batchbacktesting.py` imports `src.data` and `strategies` modules that are not in the repository.
- The AI endpoints need a reachable Ollama server; `entrypoint.sh` starts one and pulls a model, but the Dockerfile and compose file do not use it.
- Defaults use weak demo credentials (`admin`/`admin`, `minioadmin`, `postgres`), and `scripts/` contains a localhost certificate and key.

## Sources {#sources}

- [GitHub repository](https://github.com/AlgoETS/Simulateur)
- [README](https://github.com/AlgoETS/Simulateur/blob/main/README.md)
- [`simulateur/run.py`](https://github.com/AlgoETS/Simulateur/blob/main/simulateur/run.py)
- [`simulateur/simulation/logic/simulation_manager.py`](https://github.com/AlgoETS/Simulateur/blob/main/simulateur/simulation/logic/simulation_manager.py)
- [`simulateur/simulation/urls.py`](https://github.com/AlgoETS/Simulateur/blob/main/simulateur/simulation/urls.py)
- [`simulateur/simulation/api/portfolio.py`](https://github.com/AlgoETS/Simulateur/blob/main/simulateur/simulation/api/portfolio.py)
- [`simulateur/docker-compose.yml`](https://github.com/AlgoETS/Simulateur/blob/main/simulateur/docker-compose.yml)

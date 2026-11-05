---
title: "LegosTracker: LEGO catalog data and set price history"
date: 2026-11-05T12:00:00-05:00
description: "LegosTracker combines Rebrickable catalog exports, a Playwright scraper for BrickEconomy prices and notebooks that model LEGO set values."
translationKey: repository-note-legostracker
repository_note: "LegosTracker"
---

# LegosTracker

<div class="repo-status-row"><span class="repo-badge kind">Notebooks and data</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">Jupyter</span><span class="tag tool">Playwright</span><span class="tag tool">Pydantic</span><span class="tag tool">pandas</span><span class="tag tool">scikit-learn</span><span class="tag tool">Matplotlib</span><span class="tag tool">BeautifulSoup</span></div>

LegosTracker is an AlgoÉTS data project that looks at LEGO sets as a market: the Rebrickable catalog says which sets, parts and themes exist, and a BrickEconomy scraper adds the prices sets fetch over time. It is meant for collectors and data science readers who want to explore the catalog or test simple price models on one set. The article [Economics of LEGO Sets with Data Science]({{< ref "/posts/economics-lego-data-science/index.md" >}}) tells the story with charts.

## Overview {#overview}

`brickeconomy.py` reads set numbers from `set_list.txt` and drives a visible Chromium window with Playwright. For each set it searches BrickEconomy, opens the matching page and extracts the chart rows embedded in the page script: the value history goes to `<set>_history.csv` and, when present, the four-band price series to `<set>_new.csv`. It then reads the details, pricing, quick buy, predictions, facts and subtheme panels into Pydantic models and appends them to `lego_sets.csv`. `brickeconomy.ipynb` holds the same code with the install commands.

`general.ipynb` loads the Rebrickable tables in `datasets/` (colors, inventories, parts, sets, themes and their links) and plots grouped counts. `analyse.ipynb` cleans the scraped `data/lego_sets.csv` and the `data/001-1_*.csv` files for the 1965 set 001-1, fits linear and gradient boosting regressions on the price history, projects them to 2030, runs a Monte Carlo simulation on log returns and charts yearly gains and the four price bands. `price.ipynb` takes a personal `mycollection.csv`, looks up retail and current values on BrickEconomy with requests and BeautifulSoup, and writes `updated_mycollection.csv`.

## Getting started {#installation}

`brickeconomy.ipynb` installs the scraper dependencies:

```shell
pip install playwright asyncio pydantic aiohttp
playwright install
python brickeconomy.py
```

The script writes its CSV files in the current directory; `analyse.ipynb` reads them from `data/`. The notebooks need pandas, NumPy, Matplotlib, seaborn and scikit-learn (installed by the first cell of `analyse.ipynb`), plus requests and BeautifulSoup for `price.ipynb`:

```shell
pip install pandas matplotlib seaborn scikit-learn numpy
jupyter notebook
```

## Repository guide {#reader-guide}

- `brickeconomy.py` is the Playwright scraper for BrickEconomy set pages.
- `set_list.txt` lists the set numbers to scrape (001-1 to 0016-1 and 002-1).
- `data/` holds scraped output: `lego_sets.csv` and one `_history.csv` per set, plus `001-1_new.csv`.
- `datasets/` holds the Rebrickable exports as CSV and `.csv.gz`; the README documents their columns, and `images/downloads_schema_v3.webp` shows the schema.
- `general.ipynb` explores the Rebrickable catalog.
- `analyse.ipynb` cleans scraped prices and models the history of set 001-1.
- `price.ipynb` updates the values of the sets in `mycollection.csv`.

## Features {#features}

- scrape BrickEconomy value history, price bands and set panels for a list of sets;
- explore Rebrickable colors, inventories, parts, sets and themes;
- compare scraped prices across sets (lowest, highest, average);
- fit linear and gradient boosting regressions on a set's price history and project them;
- simulate future prices with a Monte Carlo model on log returns;
- update the current value of a personal collection.

## Limits {#limits}

- There is no requirements file; dependencies come from `!pip install` cells in the notebooks.
- The scraper depends on BrickEconomy's page structure and CSS selectors, runs a visible browser and stops with an error when a search returns no link.
- Output files are written in the working directory, not in `data/`, so they must be moved before running `analyse.ipynb`.
- The scraped data covers nine sets; the price models work on a single set (001-1) and are illustrations, not forecasts.
- `price.ipynb` reads only the first table of the BrickEconomy search page and defines a `TAX_RATE` constant that it never uses.
- The Rebrickable exports are a dated snapshot; the repository has no script to refresh them.

## Sources {#sources}

- [GitHub repository](https://github.com/AlgoETS/LegosTracker)
- [README](https://github.com/AlgoETS/LegosTracker/blob/main/README.md)
- [`brickeconomy.py`](https://github.com/AlgoETS/LegosTracker/blob/main/brickeconomy.py)
- [`analyse.ipynb`](https://github.com/AlgoETS/LegosTracker/blob/main/analyse.ipynb)
- [`general.ipynb`](https://github.com/AlgoETS/LegosTracker/blob/main/general.ipynb)
- [`price.ipynb`](https://github.com/AlgoETS/LegosTracker/blob/main/price.ipynb)
- [Exploring the data of LEGO history](https://github.com/hevalhazalkurt/exploring_the_data_of_LEGO_history), linked from the README

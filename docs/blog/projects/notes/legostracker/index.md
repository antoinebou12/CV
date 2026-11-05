# LegosTracker: LEGO catalog data and set price history

> LegosTracker combines Rebrickable catalog exports, a Playwright scraper for BrickEconomy prices and notebooks that model LEGO set values.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/legostracker/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/legostracker/index.md
- Published: 2026-11-05
- Updated: 2026-11-05
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/AlgoETS/LegosTracker


## Use cases

Notebooks and a Playwright scraper to study LEGO sets with Rebrickable data and BrickEconomy price history.

- **Scrape set prices** (LEGO collector, BrickEconomy website): brickeconomy.py reads set_list.txt, opens each set on BrickEconomy with Playwright Chromium, writes <set>_history.csv and <set>_new.csv from the page charts and appends details and pricing to lego_sets.csv.
- **Explore the LEGO catalog** (LEGO collector, Rebrickable exports): general.ipynb loads the Rebrickable CSV tables in datasets/ (colors, inventories, parts, sets, themes) and plots counts such as transparent versus opaque colors.
- **Model a set's price history** (LEGO collector): analyse.ipynb cleans data/001-1_history.csv, fits linear and gradient boosting regressions on dates, projects to 2030, runs a Monte Carlo on log returns and plots the price bands in data/001-1_new.csv.
- **Compare scraped set prices** (LEGO collector): analyse.ipynb loads data/lego_sets.csv, strips currency symbols and reports the lowest and highest Quick Buy price and the average Pricing value.
- **Update collection values** (LEGO collector, BrickEconomy website): price.ipynb reads mycollection.csv, looks up each set on BrickEconomy search with requests and BeautifulSoup for retail and current values, and writes updated_mycollection.csv.

### Scenario: Track the price of set 001-1

1. Install playwright, pydantic and aiohttp and run playwright install, as in brickeconomy.ipynb.
2. List set numbers such as 001-1 in set_list.txt, one per line.
3. Run python brickeconomy.py; a visible Chromium window searches BrickEconomy and opens each set page.
4. Move the generated 001-1_history.csv, 001-1_new.csv and lego_sets.csv into data/, where analyse.ipynb reads them.
5. Run analyse.ipynb to plot the history, fit the regressions and simulate future prices.



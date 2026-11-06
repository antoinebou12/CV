# Economics of LEGO Sets with Data Science

> Rebrickable trends, BrickEconomy prices, Playwright scraping, and a humble regression on classic set 001-1 — narrative with charts, code in LegosTracker.

- HTML page: https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/posts/economics-lego-data-science/index.md
- Published: 2024-05-30
- Updated: 2026-11-05
- Tags: LEGO, Data Science, Pandas, Scraping, Playwright, Data Visualization, Scikit-Learn
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)I collect LEGO and write Python, so I merged **Rebrickable** exports with a **BrickEconomy** scraper to see how sets and themes evolved, and whether a simple model could follow the resale price of a classic set like **001-1**. The notebooks and scraper live in **[AlgoETS/LegosTracker](https://github.com/AlgoETS/LegosTracker)**.

## Data sources

| Dataset | What it gives you |
|---------|-------------------|
| **Rebrickable CSVs** | sets, themes, parts, colors, inventories: good for counts and joins |
| **BrickEconomy (scraped)** | value history and sealed-price ranges that Rebrickable does not ship |

Rebrickable publishes `sets.csv`, `themes.csv`, `parts.csv`, `colors.csv` and the inventory tables. The schema below is how they join.

![Rebrickable tables and their keys](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-001.png)

## Sets over the decades

Grouping `sets` by `year` gives two trends:

```python
sets.groupby('year')['name'].nunique().plot(kind='bar')
plt.title("The Numbers of Sets by Year")
plt.show()

parts_by_year = sets[['year', 'num_parts']].groupby('year', as_index=False).mean()
parts_by_year.plot(x='year', y='num_parts', color="purple")
plt.title("Average Number of Parts by Year")
plt.show()
```

1. The **number of sets** per year climbs steeply after the late 1990s and passes 1,000 in recent years.
2. The **average part count** per set rises too, from under 100 for most of the 1970s and 1980s to around 300 at the peak.

![Number of sets released per year](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-002.png)

![Average parts per set by year](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-003.png)

## Themes that dominate the catalog

Count sets per `theme_id`, join `themes`, keep top-level themes (no `parent_id`) and plot the ten largest:

```python
set_themes = sets["theme_id"].value_counts()
set_themes = pd.DataFrame({"id": set_themes.index, "count": set_themes.values})
set_themes = pd.merge(set_themes, themes, on="id")
set_themes_no_parent = set_themes[pd.isnull(set_themes["parent_id"])]
set_themes_top_10 = set_themes_no_parent.sort_values(by=["count"], ascending=False)[:10]
top_10 = set_themes_top_10["count"]
top_10.index = set_themes_top_10["name"]
top_10.plot.bar(color="gold", rot=30)
```

![Top 10 themes by number of sets](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-004.png)

Star Wars leads by a wide margin, followed by Friends, Gear, Ninjago, Bionicle and Technic. Gear and Service Packs are a reminder that the catalog counts more than buildable sets.

## Why scrape BrickEconomy?

Rebrickable answers **what exists**. It does not say **what people pay on the secondary market**. BrickEconomy shows value estimates, growth forecasts and sales trends per set, so I wrote a scraper with **Playwright**, **asyncio**, **pydantic** models for validation, and **aiohttp**.

![What BrickEconomy publishes for a set: value, growth forecast, sales trend](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-005.png)

```bash
pip install playwright pydantic aiohttp pandas scikit-learn matplotlib
playwright install
```

The price history is not in the HTML table. It sits in an inline script that feeds a Google Charts `DataTable`, so `parse_history` reads the `<script>` tags and parses the rows out of it.

![The inline chart script that holds the price history](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-006.png)

The full `LegoAPI` class (navigation, `parse_history`, `parse_set`, CSV writing) is in the repository and the [Medium original](https://medium.com/@antoine.boucher012/economics-of-lego-sets-with-data-science-a4ca07d613fb).

## Price history for set 001-1

Set 001-1, the 1965 Samsonite Gears set, is a good test case: long history and enough resale activity to plot.

![BrickEconomy page for 001-1 Samsonite Gears](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-007.png)

The scraper writes two files per set. `001-1_history.csv` holds dated values with annotations such as the release, and `001-1_new.csv` holds monthly value ranges for sealed copies.

![001-1_history.csv: dated values and annotations](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-009.png)

![001-1_new.csv: monthly value ranges](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-008.png)

Cleaning removes duplicates, strips currency symbols, parses dates and drops zero values:

```python
df_0011.drop_duplicates(inplace=True)
df_0011['Currency Value'] = df_0011['Currency Value'].fillna(0)
df_0011['Currency Value'] = df_0011['Currency Value'].str.replace('[^\d.]', '', regex=True)
df_0011['Currency Value'] = pd.to_numeric(df_0011['Currency Value'], errors='coerce')
df_0011.drop(['Value', 'Status'], axis=1, inplace=True)
df_0011['Date'] = pd.to_datetime(df_0011['Date'], errors='coerce')
df_0011.rename(columns={'Currency Value': 'USD Value', 'Description': 'Set Description'}, inplace=True)
df_0011['USD Value'] = df_0011['USD Value'].fillna(0)
df_0011 = df_0011[df_0011['USD Value'] != 0]
```

One caveat: BrickEconomy displayed Canadian dollars for my session (`C$` in the raw values), and the notebook renames the column to `USD Value` anyway. Read the axis below as Canadian dollars.

![Notebook output: lowest and highest priced sets, average price](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-010.png)

## Linear regression as a humble forecast

The model is a plain linear regression of value against the date, with a projection to 2030:

```python
X = df_0011['Date'].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
y = df_0011['USD Value'].values

model = LinearRegression().fit(X, y)

future_dates = pd.date_range('2008-12-31', '2030-12-31', freq='Y')
future_dates_ordinal = future_dates.map(pd.Timestamp.toordinal).values.reshape(-1, 1)
future_predictions = model.predict(future_dates_ordinal)
```

![Linear regression of set 001-1 with future predictions](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-011.png)

It is not a trading signal. It is a way to ask simple questions: does the trend dominate, do the residuals cluster by era, and how far off are the recent spikes above 600? Plotting the gain between observations makes those spikes obvious.

![Gain over time and value over time for 001-1](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-012.png)

## When not to trust this analysis

| Pitfall | Effect |
|---------|--------|
| Scraper breakage | Missing months look like price crashes |
| Survivorship in the sets table | Discontinued sets skew counts |
| Linear model on hype sets | Residuals explode |
| Treating resale as MSRP | A different economic story |

## Takeaway

LEGO data is messy fun: good for **pandas practice**, **async scraping discipline**, and remembering that secondary prices are sentiment plus plastic, not fundamentals.

## Related posts

- [Vector databases / movie embeddings](https://antoineboucher.info/CV/blog/posts/vector-databases-similar-movies/): another teaching dataset story
- [MarketWatch Python](https://antoineboucher.info/CV/blog/posts/marketwatch-python-trading/): different market, same curiosity

## References

- [Rebrickable downloads](https://rebrickable.com/downloads/)
- [BrickEconomy](https://www.brickeconomy.com)
- [AlgoETS/LegosTracker](https://github.com/AlgoETS/LegosTracker)
- [Exploring LEGO History (GitHub inspiration)](https://github.com/hevalhazalkurt/exploring_the_data_of_LEGO_history)

---

*Originally published on [Medium](https://medium.com/@antoine.boucher012/economics-of-lego-sets-with-data-science-a4ca07d613fb).*

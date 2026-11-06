# Économie des boîtes LEGO avec science des données

> Tendances Rebrickable, prix BrickEconomy, scraping Playwright, régression sur le set 001-1 — récit avec graphiques, code dans LegosTracker.

- Page HTML: https://antoineboucher.info/CV/blog/fr/posts/economics-lego-data-science/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/index.md
- Publié: 2024-05-30
- Mis à jour: 2026-11-05
- Tags: LEGO, Data Science, Pandas, Scraping, Playwright, Data Visualization, Scikit-Learn
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)Je collectionne les LEGO et j’écris du Python : j’ai donc croisé les exports **Rebrickable** avec un scraper **BrickEconomy** pour voir comment les boîtes et les thèmes ont évolué, et si un modèle simple pouvait suivre le prix de revente d’une boîte classique comme la **001-1**. Les notebooks et le scraper sont dans **[AlgoETS/LegosTracker](https://github.com/AlgoETS/LegosTracker)**.

## Sources de données

| Jeu de données | Ce qu’il apporte |
|----------------|------------------|
| **CSV Rebrickable** | boîtes, thèmes, pièces, couleurs, inventaires : idéal pour compter et joindre |
| **BrickEconomy (scrapé)** | historique de valeur et fourchettes de prix des boîtes scellées, absents de Rebrickable |

Rebrickable publie `sets.csv`, `themes.csv`, `parts.csv`, `colors.csv` et les tables d’inventaire. Le schéma ci-dessous montre comment elles se joignent.

![Tables Rebrickable et leurs clés](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-001.png)

## Les boîtes au fil des décennies

Regrouper `sets` par `year` fait ressortir deux tendances :

```python
sets.groupby('year')['name'].nunique().plot(kind='bar')
plt.title("The Numbers of Sets by Year")
plt.show()

parts_by_year = sets[['year', 'num_parts']].groupby('year', as_index=False).mean()
parts_by_year.plot(x='year', y='num_parts', color="purple")
plt.title("Average Number of Parts by Year")
plt.show()
```

1. Le **nombre de boîtes** par année grimpe fortement à partir de la fin des années 1990 et dépasse 1 000 ces dernières années.
2. Le **nombre moyen de pièces** par boîte augmente aussi : moins de 100 pendant presque toutes les années 1970 et 1980, autour de 300 au sommet.

![Nombre de boîtes publiées par année](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-002.png)

![Nombre moyen de pièces par boîte et par année](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-003.png)

## Les thèmes qui dominent le catalogue

On compte les boîtes par `theme_id`, on joint `themes`, on garde les thèmes de premier niveau (sans `parent_id`) et on trace les dix plus gros :

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

![Les 10 thèmes qui comptent le plus de boîtes](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-004.png)

Star Wars arrive loin devant, suivi de Friends, Gear, Ninjago, Bionicle et Technic. Gear et Service Packs rappellent que le catalogue compte bien plus que des boîtes à construire.

## Pourquoi scraper BrickEconomy ?

Rebrickable dit **ce qui existe**, pas **ce que les gens paient sur le marché secondaire**. BrickEconomy affiche, pour chaque boîte, des estimations de valeur, des prévisions de croissance et les tendances de vente. J’ai donc écrit un scraper avec **Playwright**, **asyncio**, des modèles **pydantic** pour la validation et **aiohttp**.

![Ce que BrickEconomy publie pour une boîte : valeur, prévision de croissance, tendance des ventes](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-005.png)

```bash
pip install playwright pydantic aiohttp pandas scikit-learn matplotlib
playwright install
```

L’historique des prix n’est pas dans un tableau HTML. Il se trouve dans un script en ligne qui alimente un `DataTable` Google Charts ; `parse_history` lit donc les balises `<script>` et en extrait les lignes.

![Le script de graphique qui contient l’historique des prix](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-006.png)

La classe `LegoAPI` complète (navigation, `parse_history`, `parse_set`, écriture CSV) est dans le dépôt et dans l’[article original sur Medium](https://medium.com/@antoine.boucher012/economics-of-lego-sets-with-data-science-a4ca07d613fb).

## Historique de prix de la boîte 001-1

La 001-1, la boîte Samsonite Gears de 1965, est un bon cas d’essai : un long historique et assez de reventes pour tracer une courbe.

![Page BrickEconomy de la 001-1 Samsonite Gears](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-007.png)

Le scraper écrit deux fichiers par boîte. `001-1_history.csv` contient des valeurs datées avec des annotations, comme la sortie de la boîte, et `001-1_new.csv` des fourchettes de valeur mensuelles pour les exemplaires scellés.

![001-1_history.csv : valeurs datées et annotations](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-009.png)

![001-1_new.csv : fourchettes de valeur mensuelles](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-008.png)

Le nettoyage supprime les doublons, retire les symboles monétaires, convertit les dates et écarte les valeurs nulles :

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

Une réserve : BrickEconomy affichait des dollars canadiens pendant ma session (`C$` dans les valeurs brutes), et le notebook renomme quand même la colonne `USD Value`. Lisez l’axe ci-dessous en dollars canadiens.

![Sortie du notebook : boîtes la moins chère et la plus chère, prix moyen](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-010.png)

## Une régression linéaire comme prévision modeste

Le modèle est une simple régression linéaire de la valeur en fonction de la date, prolongée jusqu’en 2030 :

```python
X = df_0011['Date'].map(pd.Timestamp.toordinal).values.reshape(-1, 1)
y = df_0011['USD Value'].values

model = LinearRegression().fit(X, y)

future_dates = pd.date_range('2008-12-31', '2030-12-31', freq='Y')
future_dates_ordinal = future_dates.map(pd.Timestamp.toordinal).values.reshape(-1, 1)
future_predictions = model.predict(future_dates_ordinal)
```

![Régression linéaire de la boîte 001-1 et prédictions futures](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-011.png)

Ce n’est pas un signal d’achat. C’est une façon de poser des questions simples : la tendance domine-t-elle, les résidus se regroupent-ils par époque, et à quel point les pics récents au-dessus de 600 s’en écartent-ils ? Tracer le gain entre deux observations rend ces pics évidents.

![Gain et valeur dans le temps pour la 001-1](https://antoineboucher.info/CV/blog/posts/economics-lego-data-science/images/img-012.png)

## Quand ne pas se fier à cette analyse

| Piège | Effet |
|-------|-------|
| Scraper cassé | Des mois manquants ressemblent à des krachs |
| Biais du survivant dans la table des boîtes | Les boîtes retirées faussent les comptes |
| Modèle linéaire sur des boîtes à la mode | Les résidus explosent |
| Confondre revente et prix de détail | Une tout autre histoire économique |

## À retenir

Les données LEGO sont désordonnées et amusantes : de quoi **pratiquer pandas**, apprendre la **discipline du scraping asynchrone**, et se rappeler qu’un prix de revente, c’est du sentiment plus du plastique, pas des fondamentaux.

## Articles liés

- [Bases vectorielles et films similaires](https://antoineboucher.info/CV/blog/fr/posts/vector-databases-similar-movies/) : un autre jeu de données pédagogique
- [MarketWatch en Python](https://antoineboucher.info/CV/blog/fr/posts/marketwatch-python-trading/) : un autre marché, la même curiosité

## Références

- [Téléchargements Rebrickable](https://rebrickable.com/downloads/)
- [BrickEconomy](https://www.brickeconomy.com)
- [AlgoETS/LegosTracker](https://github.com/AlgoETS/LegosTracker)
- [Exploring LEGO History (inspiration GitHub)](https://github.com/hevalhazalkurt/exploring_the_data_of_LEGO_history)

---

*Publié à l’origine sur [Medium](https://medium.com/@antoine.boucher012/economics-of-lego-sets-with-data-science-a4ca07d613fb) (en anglais).*

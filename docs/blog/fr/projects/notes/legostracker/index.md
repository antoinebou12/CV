# LegosTracker : catalogue LEGO et historique des prix des ensembles

> LegosTracker réunit les exports du catalogue Rebrickable, un collecteur Playwright des prix BrickEconomy et des carnets qui modélisent la valeur des sets LEGO.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/legostracker/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/legostracker/index.md
- Publié: 2026-11-05
- Mis à jour: 2026-11-05
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/AlgoETS/LegosTracker
- Révision inspectée: c24d7e7693e838f9fd3888dd566926e7dea1fd7d


## Cas d’utilisation

Carnets et collecteur Playwright pour étudier les ensembles LEGO avec Rebrickable et l’historique de prix BrickEconomy.

- **Collecter les prix des sets** (Collectionneur LEGO, Site BrickEconomy): brickeconomy.py lit set_list.txt, ouvre chaque set sur BrickEconomy avec Playwright Chromium, écrit <set>_history.csv et <set>_new.csv à partir des graphiques et ajoute détails et prix à lego_sets.csv.
- **Explorer le catalogue LEGO** (Collectionneur LEGO, Exports Rebrickable): general.ipynb charge les tables CSV Rebrickable de datasets/ (couleurs, inventaires, pièces, sets, thèmes) et trace des décomptes, par exemple couleurs transparentes ou opaques.
- **Modéliser le prix d’un set** (Collectionneur LEGO): analyse.ipynb nettoie data/001-1_history.csv, ajuste des régressions linéaire et gradient boosting sur les dates, projette jusqu’en 2030, lance un Monte Carlo sur les rendements et trace les bandes de prix de data/001-1_new.csv.
- **Comparer les prix collectés** (Collectionneur LEGO): analyse.ipynb charge data/lego_sets.csv, retire les symboles monétaires et donne le prix Quick Buy le plus bas et le plus haut ainsi que la moyenne de Pricing.
- **Mettre à jour sa collection** (Collectionneur LEGO, Site BrickEconomy): price.ipynb lit mycollection.csv, cherche chaque set sur BrickEconomy avec requests et BeautifulSoup pour le prix de détail et la valeur actuelle, puis écrit updated_mycollection.csv.

### Scénario : Suivre le prix du set 001-1

1. Installer playwright, pydantic et aiohttp puis lancer playwright install, comme dans brickeconomy.ipynb.
2. Inscrire les numéros de sets, par exemple 001-1, dans set_list.txt, un par ligne.
3. Lancer python brickeconomy.py ; une fenêtre Chromium visible cherche sur BrickEconomy et ouvre la page de chaque set.
4. Déplacer 001-1_history.csv, 001-1_new.csv et lego_sets.csv dans data/, où analyse.ipynb les lit.
5. Exécuter analyse.ipynb pour tracer l’historique, ajuster les régressions et simuler les prix futurs.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Jupyter Notebook | 98.94 |
| Python | 1.06 |



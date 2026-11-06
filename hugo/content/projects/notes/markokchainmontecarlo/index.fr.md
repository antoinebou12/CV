---
title: "MarkokChainMonteCarlo : backtests par Monte Carlo et chaîne de Markov"
date: 2026-11-05T12:00:00-05:00
description: "Carnets d’AlgoÉTS qui simulent les prix d’AAPL par Monte Carlo et chaîne de Markov, puis backtestent une stratégie qui s’en sert face à l’achat-conservation."
mermaid: true
lastmod: 2026-11-06T04:00:00-05:00
translationKey: repository-note-markokchainmontecarlo
repository_note: "MarkokChainMonteCarlo"
---

# MarkokChainMonteCarlo

<div class="repo-status-row"><span class="repo-badge kind">Carnets</span><span class="repo-badge algorithm">Monte Carlo</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">Jupyter</span><span class="tag tool">backtesting.py</span><span class="tag tool">pandas</span><span class="tag tool">NumPy</span><span class="tag tool">SciPy</span><span class="tag tool">httpx</span><span class="tag tool">scikit-learn</span></div>

MarkokChainMonteCarlo est un dépôt de recherche d’AlgoÉTS qui backteste des stratégies d’investissement à l’aide de simulations stochastiques de prix. Ses carnets estiment des trajectoires du cours d’Apple (AAPL) avec un modèle Monte Carlo et une chaîne de Markov sur des tranches de prix, puis utilisent ces simulations dans une stratégie backtesting.py comparée à l’achat-conservation. La partie Monte Carlo est expliquée pas à pas dans [Prévoir des cours boursiers avec des simulations Monte Carlo]({{< ref "/posts/predicting-stock-prices-monte-carlo/index.fr.md" >}}).

## Aperçu {#overview}

`mcmc.ipynb` et `backtest.ipynb` commencent de la même façon : une fonction httpx télécharge l’historique quotidien complet d’AAPL chez Financial Modeling Prep, puis les données sont coupées au 2023-01-01 en une partie d’entraînement et une partie de validation. `monte_carlo_simulation` estime la dérive et la volatilité à partir des rendements logarithmiques et fait évoluer le prix avec des chocs aléatoires ; `mcmc.ipynb` ajoute des variantes à volatilité glissante, à chocs extrêmes occasionnels et à dérive stochastique facultative, et trace des projections sur 364 jours avec 1 000 ou 10 000 trajectoires. La chaîne de Markov découpe les clôtures d’entraînement en tranches de 10 $ entre 0 et 200, compte les passages d’une tranche à l’autre avec `pandas.crosstab` et tire une suite d’états avec `markov_chain_simulation`. Le carnet se termine par une régression linéaire sur l’indice des jours.

`backtest.ipynb` définit `MCMCStrategy` : la stratégie simule trajectoires et états de Markov au début du backtest, achète quand le dernier état simulé vaut 0 et sort sur un stop de 5 % ou quand la clôture atteint un prix cible tiré d’une trajectoire simulée. `BuyAndHoldStrategy` sert de référence. Les deux tournent avec 10 000 en encaisse, une commission de 0,2 % et des ordres exclusifs, sur les deux périodes. `proto.ipynb` est le premier prototype sur des prix générés aléatoirement, et `output/MCMCStrategy.html` est un graphique backtesting.py enregistré.

## Fonctionnement des algorithmes {#algorithm}

**Monte-Carlo vers l’avant.** `monte_carlo_simulation` traite le prix comme un mouvement brownien géométrique estimé sur l’historique :

```text
rᵢ = ln(Pᵢ / Pᵢ₋₁)                      rendements logarithmiques quotidiens des clôtures d’entraînement
drift = moyenne(r) − ½ · var(r)
σ = écart-type(r)
Pₜ₊₁ = Pₜ · exp(drift + σ · Z),  Z ~ N(0, 1)   (Z tiré par norm.ppf(uniforme))
```

La boucle répète ce pas `days` fois sur `iterations` trajectoires, chacune partant de la dernière clôture d’entraînement. Par exemple, avec un rendement logarithmique moyen de 0,0010 et σ = 0,02 (variance 0,0004), la dérive vaut 0,0008, et un tirage Z = 1 fait passer 100 à 100 · e^0,0208 ≈ 102,10. Ces valeurs sont illustratives ; le carnet estime les siennes sur AAPL.

Une subtilité : pour un mouvement brownien géométrique, la moyenne des rendements *logarithmiques* vaut déjà μ − σ²/2 ; retrancher encore ½ var compte la correction deux fois. Avec σ = 0,02, cela fait 0,0002 par jour, et sur l’horizon de 364 jours du carnet la trajectoire médiane baisse d’un facteur e^(−364 · 0,0002) ≈ 0,93, soit environ 7 %. `monte_carlo_simulation_with_roulette` ajoute, avec une probabilité de 5 % par jour, un choc supplémentaire de ±3σ à toutes les trajectoires à la fois.

**Chaîne de Markov sur des tranches de prix.** Les clôtures d’entraînement sont découpées en tranches de 10 $ avec `pd.cut` (0–10, 10–20, …, 190–200, et une tranche au-delà de 200). `pd.crosstab(courant, suivant, normalize='index')` compte combien de fois une clôture de la tranche *i* est suivie d’une clôture de la tranche *j* et divise par le total de la ligne : on obtient la probabilité de transition P(i → j). `markov_chain_simulation` parcourt ensuite la chaîne : depuis l’état courant, elle tire le suivant avec `np.random.choice(états, p=ligne)`.

Un exemple jouet montre le décompte. Six clôtures de 148, 152, 155, 149, 151 et 158 tombent dans les tranches (140, 150], (150, 160], (150, 160], (140, 150], (150, 160], (150, 160]. Les cinq passages sont : 140→150 deux fois, 150→150 deux fois, 150→140 une fois. La ligne de (140, 150] va donc à 100 % vers (150, 160], et celle de (150, 160] reste sur place aux 2/3 et descend au 1/3.

**La stratégie.** `MCMCStrategy.init` lance les deux simulations une seule fois sur toute la durée du backtest ; `next` achète quand le dernier état simulé de la chaîne vaut 0 et, une fois en position, sort sur un stop 5 % sous l’entrée ou quand la clôture atteint un objectif tiré du dernier prix simulé d’une trajectoire au hasard.

```mermaid
flowchart TD
  H["Clôtures quotidiennes d’AAPL (FMP)"] --> S["Coupure au 2023-01-01"]
  S --> T["Clôtures d’entraînement"]
  T --> LR["Rendements logarithmiques → dérive, σ"]
  LR --> MC["1 000 trajectoires MBG sur la durée du backtest"]
  T --> B["Tranches de 10 $ → matrice de transition"]
  B --> MK["Suite d’états simulée depuis l’état 0"]
  MC & MK --> ST["MCMCStrategy.init"]
  ST --> N{"next() : sans position et dernier état == 0 ?"}
  N -->|oui| BUY["Achat, exécuté à l’ouverture suivante"]
  BUY --> EX{"clôture ≤ entrée × 0,95 ou clôture ≥ dernier prix d’une trajectoire ?"}
  EX -->|oui| SELL["Vente"]
```

Tel qu’écrit, les états sont des intervalles comme (0, 10], alors que la stratégie démarre la chaîne à l’entier 0 et compare le dernier état à 0. La recherche de l’état de départ et le test d’achat mélangent un entier et des étiquettes d’intervalles : la condition d’entrée ne se comporte pas comme le disent les commentaires.

## Démarrage {#installation}

Le README installe les bibliothèques avec :

```bash
pip install panda lxml bs4 httpx backtesting yfinance pandas_ta scipy rich TA-Lib
```

`requirements.txt` fige un ensemble plus restreint (`backtesting`, `httpx`, `numpy`, `pandas`, `pandas-ta`). Les carnets utilisent aussi Matplotlib et scikit-learn. Mettez votre propre clé Financial Modeling Prep dans la cellule `FMP_API_KEY`, puis ouvrez les carnets :

```bash
jupyter notebook backtest.ipynb
```

## Guide du dépôt {#reader-guide}

- `mcmc.ipynb` couvre la séparation des données, les variantes Monte Carlo, la chaîne de Markov, les graphiques et la régression linéaire.
- `backtest.ipynb` reprend les simulations et exécute `MCMCStrategy` et `BuyAndHoldStrategy`.
- `proto.ipynb` est le prototype sur des prix synthétiques.
- `output/MCMCStrategy.html` est un graphique de backtest enregistré.
- `images/` contient les illustrations du README.
- `Algo Markov Chain Monte Carlo (MCMC)_.pdf` est un document PDF conservé avec le code.

## Fonctionnalités {#features}

- historique quotidien d’AAPL depuis Financial Modeling Prep, coupé au 2023-01-01 ;
- trajectoires de prix Monte Carlo, avec variantes à volatilité glissante et à chocs extrêmes ;
- chaîne de Markov sur des tranches de 10 $ avec matrice de transition empirique ;
- stratégie backtesting.py fondée sur les états simulés et des prix cibles simulés ;
- référence d’achat-conservation sur les mêmes périodes ;
- tendance linéaire ajustée sur l’indice des jours.

## Limites {#limits}

- Malgré le nom, le code ne contient aucun échantillonneur de Monte Carlo par chaînes de Markov (comme Metropolis–Hastings) : les carnets combinent une simulation Monte Carlo directe et une chaîne de Markov distincte.
- `MCMCStrategy` simule une seule fois, au début du backtest, sur toute la série et lit le dernier élément d’une liste d’états fixe : sa condition d’entrée ne change donc pas d’une barre à l’autre. La chaîne part en outre d’un état 0 codé en dur.
- La matrice de transition ne couvre que les clôtures de 0 à 200, avec une seule tranche ouverte au-dessus.
- Une clé d’API FMP est écrite dans les carnets ; remplacez-la par la vôtre.
- La commande d’installation du README contient `panda` au lieu de `pandas`, et `requirements.txt` ne liste pas tous les imports.
- Les carnets ne conservent pas les résultats des backtests, et ces résultats dépendent de tirages aléatoires sans graine fixe (sauf dans `proto.ipynb`).

## Sources {#sources}

- [Dépôt GitHub](https://github.com/AlgoETS/MarkokChainMonteCarlo)
- [README](https://github.com/AlgoETS/MarkokChainMonteCarlo/blob/main/README.md)
- [`mcmc.ipynb`](https://github.com/AlgoETS/MarkokChainMonteCarlo/blob/main/mcmc.ipynb)
- [`backtest.ipynb`](https://github.com/AlgoETS/MarkokChainMonteCarlo/blob/main/backtest.ipynb)
- [`proto.ipynb`](https://github.com/AlgoETS/MarkokChainMonteCarlo/blob/main/proto.ipynb)

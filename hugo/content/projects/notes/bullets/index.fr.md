---
title: "BullETS : une bibliothèque Python pour backtester des stratégies"
date: 2026-11-05T12:00:00-05:00
description: "BullETS est une bibliothèque Python d’AlgoÉTS pour écrire des stratégies boursières et les backtester sur les données de Financial Modeling Prep."
translationKey: repository-note-bullets
repository_note: "BullETS"
---

# BullETS

<div class="repo-status-row"><span class="repo-badge kind">Bibliothèque</span><span class="repo-badge workflow">CI</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">aiohttp</span><span class="tag tool">python-dotenv</span><span class="tag tool">unittest</span><span class="tag tool">GitHub Actions</span><span class="tag tool">PyPI</span></div>

BullETS est un paquet Python pour développer des stratégies de trading algorithmique : on hérite d’une classe de stratégie, on branche une source de données et un exécuteur rejoue le marché. Ce projet d’AlgoÉTS, publié sur PyPI sous ce nom, s’adresse aux développeurs Python qui veulent tester une idée sur des cours historiques sans écrire eux-mêmes la relecture du marché, la gestion des ordres et l’accès aux données.

## Aperçu {#overview}

Une stratégie hérite de `Strategy` (`src/bullets/strategy.py`) et redéfinit trois méthodes : `on_start`, `on_resolution` et `on_finish`. `Runner` (`src/bullets/runner.py`) dresse la liste des moments entre la date de début et la date de fin, à la journée, à l’heure ou à la minute, en sautant les fins de semaine, les jours fériés des marchés américains (`src/bullets/utils/holiday_date_util.py`) et les heures hors de la plage 9 h 30 – 16 h. À chaque moment, il met à jour l’horodatage commun, appelle la stratégie, puis laisse le portefeuille vérifier les ordres en attente.

`Portfolio` (`src/bullets/portfolio/portfolio.py`) tient l’encaisse, les positions et le journal des transactions. Un ordre au marché est exécuté à un prix simulé : en résolution quotidienne, le prix se rapproche du haut de la journée selon le pourcentage de glissement (25 % par défaut), et des frais fixes (1 par défaut) s’ajoutent. Chaque `Transaction` note son statut (réussie, fonds insuffisants ou symbole introuvable) et s’inscrit au journal.

Les cours et données fondamentales viennent de `FmpDataSource` (`src/bullets/data_source/data_source_fmp.py`), qui interroge l’API Financial Modeling Prep avec aiohttp, met en cache les cours par symbole et lit aussi les états des résultats, bilans, flux de trésorerie et listes de symboles. `Indicators` (`src/bullets/data_indicators/indicators.py`) calcule moyennes mobiles et oscillateurs à partir de la même source.

## Démarrage {#installation}

Créez un compte Financial Modeling Prep pour obtenir une clé d’API, puis installez le paquet dans un environnement virtuel :

```shell
python3 -m venv bot-env
source bot-env/bin/activate
pip install BullETS
```

La stratégie minimale du README achète cinq actions AAPL à chaque résolution :

```python
from bullets.strategy import Strategy, Resolution
from bullets.runner import Runner
from bullets.data_source.data_source_fmp import FmpDataSource
from datetime import datetime

class MyStrategy(Strategy):
    def on_resolution(self):
        self.portfolio.market_order("AAPL", 5)

resolution = Resolution.DAILY
data_source = FmpDataSource("Insert your key here", resolution)
strategy = MyStrategy(resolution=resolution,
                      start_time=datetime(2019, 3, 5),
                      end_time=datetime(2019, 4, 22),
                      starting_balance=5000,
                      data_source=data_source)
Runner(strategy).start()
```

Pour contribuer à la bibliothèque, clonez-la, installez-la en mode modifiable et copiez `.env.sample` vers `.env` avec votre `FMP_TOKEN` :

```shell
git clone https://github.com/AlgoETS/BullETS
cd BullETS
pip install -e .
python -m unittest discover src/test
```

## Guide du dépôt {#reader-guide}

- `src/bullets/strategy.py` définit la classe de base `Strategy` et la validation des paramètres.
- `src/bullets/runner.py` rejoue les moments de marché et affiche le bilan de fin de backtest.
- `src/bullets/portfolio/` contient `Portfolio`, `Holding` et `Transaction`.
- `src/bullets/data_source/` contient l’interface des sources de données, l’implémentation FMP et les enregistrements de cours et d’états financiers.
- `src/bullets/data_indicators/indicators.py` implémente les indicateurs techniques.
- `src/bullets/utils/` calcule les jours fériés américains et les décalages en jours de marché.
- `src/bullets/logger.py` fournit une journalisation colorée à niveaux réglables.
- `src/test/` regroupe les tests unittest des heures de marché, des jours fériés, du portefeuille et d’une exécution complète.
- `.github/workflows/` lance l’analyse et les tests sur les demandes de fusion et les fusions, et publie sur PyPI à chaque version.

## Fonctionnalités {#features}

- méthodes de stratégie au début, à chaque résolution et à la fin ;
- résolutions quotidienne, horaire et à la minute, avec heures et jours fériés des marchés américains ;
- ordres au marché, stop et à cours limité, avec glissement et frais de transaction ;
- bilan de fin d’exécution : solde final, encaisse, frais, profit en pourcentage et appels FMP restants ;
- historique des cours, états des résultats, bilans, flux de trésorerie et listes de symboles depuis FMP, en cache par symbole ;
- SMA, WMA, EMA, MACD, RSI, écart type et bandes de Bollinger ;
- flake8, unittest et Codecov en intégration continue ; publication automatisée sur PyPI.

## Limites {#limits}

- Le README présente la récupération des données, la gestion de portefeuille et le backtesting comme des « fonctionnalités à venir », et `setup.py` indique la version 0.1.1 ; le dernier commit du dépôt date de mars 2022.
- Le glissement ne s’applique qu’en résolution quotidienne ; sinon, la stratégie affiche un avertissement.
- `buy_limit_order` et `sell_limit_order` ajoutent leurs ordres aux listes d’ordres stop, et les ordres stop ou limités exécutés ne sont pas retirés de leur liste : ils peuvent se déclencher de nouveau aux résolutions suivantes.
- La boucle de l’exécuteur ne s’arrête que si elle tombe exactement sur `end_time` ; la date de fin doit donc être atteignable en pas entiers de résolution.
- La plupart des tests interrogent l’API FMP en direct avec `FMP_TOKEN` : ils exigent une clé et un accès réseau.
- Financial Modeling Prep est la seule source de données implémentée.

## Sources {#sources}

- [Dépôt GitHub](https://github.com/AlgoETS/BullETS)
- [README](https://github.com/AlgoETS/BullETS/blob/develop/README.md)
- [`src/bullets/runner.py`](https://github.com/AlgoETS/BullETS/blob/develop/src/bullets/runner.py)
- [`src/bullets/strategy.py`](https://github.com/AlgoETS/BullETS/blob/develop/src/bullets/strategy.py)
- [`src/bullets/portfolio/portfolio.py`](https://github.com/AlgoETS/BullETS/blob/develop/src/bullets/portfolio/portfolio.py)
- [`src/bullets/data_source/data_source_fmp.py`](https://github.com/AlgoETS/BullETS/blob/develop/src/bullets/data_source/data_source_fmp.py)
- [`src/bullets/data_indicators/indicators.py`](https://github.com/AlgoETS/BullETS/blob/develop/src/bullets/data_indicators/indicators.py)

---
title: "BatchBacktesting : comparer des simulations de stratégie"
date: 2026-10-24T12:00:00-04:00
description: "BatchBacktesting exécute des backtests Python sur plusieurs instruments en conservant les hypothèses et les résultats visibles."
translationKey: repository-note-batchbacktesting
repository_note: "BatchBacktesting"
---

# BatchBacktesting

BatchBacktesting transforme un backtest en traitement reproductible : choisir les instruments, obtenir et nettoyer les prix, exécuter une stratégie, puis conserver des résultats comparables. C'est un dépôt [AlgoÉTS](https://github.com/AlgoETS) ; les faits ci-dessous viennent de ses fichiers source et de son README, lus pour l'[article associé]({{< ref "/posts/batchbacktesting-engine/index.fr.md" >}}).

## Aperçu

**Pourquoi il existe.** Un backtest par lots est un petit pipeline de données, et le projet garde chaque étape visible en Python plutôt que derrière un tableau de bord.

**Cas d'usage.** Comparer une stratégie sur plusieurs instruments avec les mêmes hypothèses enregistrées, puis lire côte à côte les CSV par instrument et agrégés.

## Démarrage

Le README pointe vers un exemple publié plutôt qu'une installation en une commande ; le point d'entrée est le runner.

- Runner : [`src/BatchBacktesting.py`](https://github.com/AlgoETS/BatchBacktesting/blob/main/src/BatchBacktesting.py) — `process_instrument` choisit l'adaptateur de prix (actions ou crypto), nettoie les données et construit un `Backtest`.
- Stratégies : [`src/strategies.py`](https://github.com/AlgoETS/BatchBacktesting/blob/main/src/strategies.py).
- Outils d'analyse : [`src/analyse.py`](https://github.com/AlgoETS/BatchBacktesting/blob/main/src/analyse.py).
- Graphique AAPL EMA publié (2018-04-04 au 2023-04-03) : [output/charts/EMA](https://algoets.github.io/BatchBacktesting/output/charts/EMA/AAPL-2018-04-04-2023-04-03.html).

## Fonctions et composants

| Composant | Rôle |
| --- | --- |
| Runner par instrument | Choisit l'adaptateur de prix, nettoie les observations, exécute un `Backtest`, étiquette le résultat avec l'instrument et la stratégie |
| Pool de workers | `ThreadPoolExecutor`, quatre workers par défaut pour une stratégie ; l'aide multi-stratégies imbrique un pool externe autour des pools internes |
| Paramètres par défaut | 100 000 de capital initial, commission de 0,002 (0,2 %), ordres exclusifs |
| Stratégie EMA | EMA de 20, 80 et 150 périodes calculées ; les entrées comparent les courbes 20 et 80 ; côté long, fermeture de la position précédente puis achat avec stop à 90 % et cible à 125 % |
| Sorties | CSV par instrument, CSV agrégé par stratégie, graphique HTML optionnel |

## Architecture

```mermaid
flowchart TD
  I["Liste d'instruments et stratégie"] --> P["ThreadPoolExecutor"]
  P --> D["Télécharger et nettoyer l'historique"]
  D --> B["Backtest par instrument"]
  B --> R["Résultat avec instrument et stratégie"]
  R --> C["CSV par instrument"]
  R --> A["CSV agrégé par stratégie"]
  B --> H["Graphique HTML optionnel"]
```

## Limites et points à vérifier

- Un instrument en échec renvoie `None` ; si tous échouent, la concaténation finale n'a aucun tableau.
- `groupby("Instrument").max()` dans `analyse.py` prend le maximum de chaque colonne séparément : une ligne de synthèse peut mélanger des métriques de runs différents. Choisissez une vraie ligne par rendement avant de citer son drawdown.
- Les paramètres par défaut n'incluent ni le slippage, ni la disponibilité des ventes à découvert, ni les titres radiés, ni les opérations sur titres.
- Les nombres de workers et les dates ci-dessus sont des valeurs par défaut du code et des dates d'exemple, pas un débit mesuré ni une plage fixe.

## Liens

- [Dépôt](https://github.com/AlgoETS/BatchBacktesting)
- [Exemple publié](https://algoets.github.io/BatchBacktesting/)
- [Workshop1]({{< ref "/projects/notes/workshop1/index.fr.md" >}}), les notebooks d'initiation qui mènent à ce runner par lots

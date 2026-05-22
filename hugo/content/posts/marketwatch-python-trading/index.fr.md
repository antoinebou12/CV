---
post_kind: article
title: "Bibliothèque Python pour le trading virtuel MarketWatch"
date: 2026-04-13T10:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "Paquet PyPI marketwatch — client Python pour le jeu boursier virtuel MarketWatch, surface API, limites, lien avec backtesting."
translationKey: marketwatch-python-trading
tags:
  - Python
  - MarketWatch
  - Trading
  - Finance
  - Open Source
images:
  - featured.png
---

Automatiser quelques tâches dans le **jeu boursier virtuel** MarketWatch (paper trading, pas un courtier réel). **[marketwatch](https://pypi.org/project/marketwatch/)** sur PyPI — listes de suivi, état de partie, portefeuille, ordres, classement. **[English version]({{< ref "/posts/marketwatch-python-trading/index.md" >}})**.

<!--more-->

## Pourquoi

Les projets utilisaient déjà **BatchBacktesting** sur données historiques — voir **[expérimentation indicateurs]({{< ref "/posts/experimentation-indicateurs-backtesting/index.fr.md" >}})**. Le jeu MarketWatch = cookies de session, règles de partie, classements qui changent. Un wrapper Python bat les scripts curl dans un notebook.

## Liens

- [pypi.org/project/marketwatch](https://pypi.org/project/marketwatch/)
- [antoinebou12.github.io/marketwatch](https://antoinebou12.github.io/marketwatch/)
- [github.com/antoinebou12/marketwatch](https://github.com/antoinebou12/marketwatch)

## Fonctions

| Domaine | Usage |
|---------|--------|
| **Listes** | Créer, lister, mettre à jour |
| **Parties** | Lister, lire paramètres |
| **Portefeuille** | Positions, ordres en attente |
| **Trading** | Achat / vente dans les règles du jeu |
| **Classement** | Leaderboard |

Petits bots et criblage — pas du HFT.

## Démarrage

```bash
pip install marketwatch
```

```python
from marketwatch import MarketWatch

mw = MarketWatch("your_username", "your_password")
mw.get_games()
mw.get_price("AAPL")
```

Cas limites de connexion documentés sur le site.

![Client Python MarketWatch](./featured.png)

## Limites

- **API non officielle** — peut casser ; épingler les versions.
- **Conditions d’utilisation** — respecter les règles MarketWatch.
- **Pas un conseil financier** — gains papier ≠ stratégie validée.

Voir aussi **[backtesting multi-indicateurs]({{< ref "/posts/multiple-indicators-backtesting/index.fr.md" >}})** et **[Monte Carlo]({{< ref "/posts/predicting-stock-prices-monte-carlo/index.fr.md" >}})**.

## Articles liés

- [Expérimentation indicateurs techniques]({{< ref "/posts/experimentation-indicateurs-backtesting/index.fr.md" >}})
- [Économie LEGO et data science]({{< ref "/posts/economics-lego-data-science/index.fr.md" >}})

Tickets : [GitHub](https://github.com/antoinebou12/marketwatch).

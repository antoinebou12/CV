---
post_kind: article
title: "Bibliothèque Python pour le trading virtuel MarketWatch"
date: 2026-04-13T10:00:00-04:00
description: "Paquet PyPI `marketwatch` — client Python pour le jeu boursier virtuel MarketWatch (listes de suivi, parties, portefeuille, ordres, classement)."
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

J’ai publié **[marketwatch](https://pypi.org/project/marketwatch/)** sur PyPI : un petit client Python pour le **jeu boursier virtuel** [MarketWatch](https://www.marketwatch.com) (paper trading), pas l’accès à un courtier réel. Pour scripter des listes de suivi, récupérer les données d’une partie ou du portefeuille, ou expérimenter une automatisation dans le cadre du jeu, le paquet encapsule les flux dans une API simple.

## Liens

- **Paquet :** [pypi.org/project/marketwatch](https://pypi.org/project/marketwatch/)
- **Documentation :** [antoinebou12.github.io/marketwatch](https://antoinebou12.github.io/marketwatch/)
- **Source et tickets :** [github.com/antoinebou12/marketwatch](https://github.com/antoinebou12/marketwatch)

## Ce que ça permet

- Créer et gérer des **listes de suivi**
- Lire les détails et paramètres d’une **partie**
- Inspecter **portefeuille**, positions et ordres en attente
- **Acheter** et **vendre** (dans le jeu)
- Récupérer le **classement** d’une partie

Utile pour explorer des stratégies automatisées ou de petits bots **dans les règles du jeu** — voir la doc pour les noms de méthodes et les structures retournées.

## Démarrage rapide

```bash
pip install marketwatch
```

```python
from marketwatch import MarketWatch

mw = MarketWatch("your_username", "your_password")
mw.get_games()
mw.get_price("AAPL")
```

Pour les cas limites de connexion, chaque méthode et des exemples d’ordres et de listes, voir la [documentation](https://antoinebou12.github.io/marketwatch/).

![Image à la une pour l’article sur la bibliothèque Python MarketWatch](./featured.png)

L’automatisation peut entrer en conflit avec les conditions d’utilisation ou les limites de débit de la plateforme ; utilisez le paquet de façon responsable et vérifiez les règles MarketWatch pour tout usage non trivial.

Questions ou bugs bienvenus sur [GitHub](https://github.com/antoinebou12/marketwatch).

# Bibliothèque Python pour le trading virtuel MarketWatch

> Paquet PyPI marketwatch — client Python pour le jeu boursier virtuel MarketWatch, surface API, limites, lien avec backtesting.

- Page HTML: https://antoineboucher.info/CV/blog/fr/posts/marketwatch-python-trading/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/posts/marketwatch-python-trading/index.md
- Publié: 2026-04-13
- Mis à jour: 2026-05-22
- Tags: Python, MarketWatch, Trading, Finance, Open Source
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)Automatiser quelques tâches dans le **jeu boursier virtuel** MarketWatch (paper trading, pas un courtier réel). **[marketwatch](https://pypi.org/project/marketwatch/)** sur PyPI — listes de suivi, état de partie, portefeuille, ordres, classement.

## Pourquoi

Les projets utilisaient déjà **BatchBacktesting** sur données historiques — voir **[expérimentation indicateurs](https://antoineboucher.info/CV/blog/fr/posts/experimentation-indicateurs-backtesting/)**. Le jeu MarketWatch = cookies de session, règles de partie, classements qui changent. Un wrapper Python bat les scripts curl dans un notebook.

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

## Limites

- **API non officielle** — peut casser ; épingler les versions.
- **Conditions d’utilisation** — respecter les règles MarketWatch.
- **Pas un conseil financier** — gains papier ≠ stratégie validée.

Voir aussi **[backtesting multi-indicateurs](https://antoineboucher.info/CV/blog/fr/posts/multiple-indicators-backtesting/)** et **[Monte Carlo](https://antoineboucher.info/CV/blog/fr/posts/predicting-stock-prices-monte-carlo/)**.

## Articles liés

- [Expérimentation indicateurs techniques](https://antoineboucher.info/CV/blog/fr/posts/experimentation-indicateurs-backtesting/)
- [Économie LEGO et data science](https://antoineboucher.info/CV/blog/fr/posts/economics-lego-data-science/)

Tickets : [GitHub](https://github.com/antoinebou12/marketwatch).

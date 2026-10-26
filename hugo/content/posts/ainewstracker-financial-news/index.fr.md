---
title: "Suivre l’actualité financière avec AINewsTracker"
date: 2026-10-24T12:00:00-04:00
description: "Une lecture fondée sur le dépôt du flux de collecte, d’analyse par IA et de backtesting d’AINewsTracker."
translationKey: ainewstracker-financial-news
tags: [Python, IA, Finance]
post_kind: article
mermaid: true
lastmod: 2026-10-26T12:00:00-04:00
---

AINewsTracker transforme les actualités financières en données consultables, analysables et comparables aux données de marché.

<!--more-->

Le projet est un service FastAPI avec des routes distinctes pour les actualités, les articles, les entreprises, les utilisateurs, l’amorçage des données et les stratégies de négociation. Les routes reçoivent les requêtes HTTP; les services et les dépôts prennent en charge l’analyse et le stockage.

## Du flux à l’article

Le parcours principal commence dans `app/routers/news.py`. Une route transmet le travail à `app/core/services/news.py`, qui récupère le contenu des flux et construit les articles. L’analyse de texte se trouve dans `app/core/services/metrics.py`; le dépôt d’articles enregistre ensuite le résultat dans MongoDB.

```mermaid
flowchart LR
  User["Client API"] --> API["FastAPI<br/>app/main.py"]
  API --> Routes["Routes d’actualités<br/>app/routers/news.py"]
  Routes --> Fetcher["Service d’actualités<br/>app/core/services/news.py"]
  Sources["Sources financières"] --> Fetcher
  Fetcher --> Metrics["Mesures de texte<br/>app/core/services/metrics.py"]
  Fetcher --> Repo["Dépôt d’articles<br/>app/core/repo/article.py"]
  Repo --> Mongo[("MongoDB")]
```

Les routes définissent l’interface HTTP, les modèles décrivent les données, les services traitent les actualités et les dépôts isolent l’accès à la base. `app/main.py` configure aussi le cache Redis.

## Garder la source avec l’analyse

L’[aperçu des données](https://algoets.github.io/AINewsTracker/overview/) relie quatre objets : une source produit des articles, les commentaires appartiennent à un article et les entreprises identifient les sociétés mentionnées. La source porte notamment la langue et le pays. L’article conserve son URL, sa date et son texte avec les champs d’analyse.

Cette séparation facilite la vérification. On peut remonter d’un sentiment à l’article et à son éditeur. Le symbole boursier permet de rapprocher les mentions d’une entreprise sans traiter chaque variante de son nom comme une société différente.

## Les résultats de l’analyse de texte

La documentation illustre un sentiment et son score, des symboles boursiers détectés, un résumé et des sujets. Ces champs répondent à des questions différentes : de quelle entreprise parle-t-on, que dit l’article et comment son texte est-il classé ? Les exemples expliquent le modèle, tandis que les classes Pydantic définissent les champs réels.

Je comparerais ces résultats au texte original avant de les utiliser dans une stratégie. Un résumé peut omettre une condition. La mention d’une entreprise ne suffit pas à établir un événement exploitable en bourse. L’URL et la date doivent donc rester accessibles pendant la vérification.

## Analyse et backtesting

La documentation décrit l’analyse de sentiment, la classification par sujet, l’attribution de tickers et le résumé d’articles. La route de stratégie transmet les demandes de backtest à `app/core/trading/strategy.py`.

Ces étiquettes restent des données d’entrée pour une expérience. Elles ne prouvent pas qu’une actualité a causé un mouvement de marché, et un backtest historique ne garantit pas les résultats futurs.

Pour examiner une expérience, je distingue les étapes suivantes :

| Étape | Éléments à vérifier |
| --- | --- |
| Collecte | Éditeur, URL, date de publication et texte récupéré |
| Analyse du texte | Entreprises détectées, étiquettes et résumé comparés à l’article |
| Entrée de stratégie | Observations disponibles au moment testé |
| Résultat du backtest | Période, hypothèses et résultat annoncé par la stratégie |

Cette grille décrit la façon dont j’évaluerais une expérience construite sur le service. Elle ne présente aucune mesure de précision prédictive ou de rendement.

## Surface de l’API

La documentation publiée couvre l’ingestion depuis RSS, GNews et des flux nommés; le stockage des articles et la lecture des scores; les entreprises et la recherche par ticker; ainsi que les stratégies pour une ou plusieurs entreprises. FastAPI expose sa documentation interactive sous `/api/v1/docs` sur le port local documenté `8000`.

## Exécution locale

```shell
cp .env.example .env
pip install poetry
poetry shell
poetry install
poetry run pytest
poetry run uvicorn app.main:app --reload
```

Docker Compose fournit un autre point d’entrée :

```shell
docker-compose up --build
```

## Lire l’architecture

Le GitDiagram complet montre l’enregistrement des routes, les modèles, les dépôts, les scripts d’amorçage, MongoDB, Redis et la branche de stratégie. Chaque nœud renvoie à son fichier source.

- [GitDiagram interactif](https://gitdiagram.com/algoets/ainewstracker)
- [Référence du projet AINewsTracker]({{< ref "/projects/notes/ainewstracker/index.fr.md" >}})
- [Dépôt source](https://github.com/AlgoETS/AINewsTracker)
- [Documentation publiée](https://algoets.github.io/AINewsTracker/)
- [Modèle de données et analyse de texte](https://algoets.github.io/AINewsTracker/overview/)

Le dépôt reste la référence pour la configuration, les routes actuelles et les prérequis d’installation.

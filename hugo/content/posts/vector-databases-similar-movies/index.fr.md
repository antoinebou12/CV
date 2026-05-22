---
post_kind: article
title: "Similarité entre films et recherche vectorielle"
date: 2026-04-13T12:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "Récit pédagogique : kNN pgvector en SQL, vecteurs denses et creux Qdrant sur MovieLens, puis RAG LangChain + Ollama."
translationKey: vector-databases-similar-movies
images:
  - featured.png
tags:
  - PostgreSQL
  - pgvector
  - Qdrant
  - Python
  - Embeddings
  - RAG
  - Machine Learning
canonicalURL: "https://medium.com/@antoine.boucher012/using-vector-databases-to-find-similar-movies-algorithm-part-1-f14a244bb23d"
aliases:
  - /posts/dense-sparse-vectors-qdrant-movielens/
  - /posts/rag-movies-pgvector-langchain-ollama/
---

Fil conducteur « films similaires » : **embeddings dans PostgreSQL**, même idée dans **Qdrant** avec deux sens du vecteur, puis **récupération + LLM local** sur les mêmes lignes. Récit ici ; notebooks dans [AlgoETS/SimilityVectorEmbedding](https://github.com/AlgoETS/SimilityVectorEmbedding). **[English version]({{< ref "/posts/vector-databases-similar-movies/index.md" >}})**.

<!--more-->

## Trois questions différentes

1. **Langage des synopsis** — « films dans cet esprit ».
2. **Chevauchement de notes** — « utilisateurs au profil proche ».
3. **Explication** — « pourquoi ces titres ? » à partir d’une question.

Les parties 1–3 y répondent. Mélanger sans nommer le type de vecteur = démos trompeuses.

## Partie 1 — PostgreSQL et pgvector

Catalogue depuis [`movies.json`](https://github.com/AlgoETS/SimilityVectorEmbedding/blob/main/movies.json) : concaténer champs texte, encoder (MiniLM, GTE…), colonnes `vector` à côté du relationnel.

Opérateurs `<=>` (cosinus), `<->` (L2) → kNN en `ORDER BY … LIMIT`.

```sql
SELECT title,
       1 - (embedding_minilm <=> (
         SELECT embedding_minilm FROM movies WHERE title = $1
       )) AS similarity
FROM movies
WHERE title IS DISTINCT FROM $1
ORDER BY similarity DESC
LIMIT 10;
```

Plusieurs colonnes `embedding_*` pour comparer les encodeurs. Graphiques : [Medium partie 1](https://medium.com/@antoine.boucher012/using-vector-databases-to-find-similar-movies-algorithm-part-1-f14a244bb23d), notebooks `postgres/`.

## Partie 2 — Qdrant et MovieLens

| Collection | Type | Question |
|------------|------|----------|
| Films | Dense | « Comme cette formulation » |
| Profils | Dense | Représentation utilisateur (pipeline seed) |
| Notes | **Creux** id film → note | « Goûts qui se recoupent » |

Dense : texte → MiniLM → recherche films. Creux : vecteur de notes → voisins → agrégation — filtrage collaboratif sans réseau de neurones dans le notebook.

Projet FastAPI `movie_recommendation` dans le dépôt cours. Entrée : `qdrant/0.simple.ipynb`.

## Partie 3 — RAG LangChain + Ollama

```mermaid
flowchart LR
  Q[Question] --> E[Embedding]
  E --> SQL[kNN SQL]
  SQL --> Rows[Films]
  Rows --> LLM[Ollama]
  LLM --> A[Réponse ancrée]
```

Notebook `postgres/3.LLMS.ipynb` — échecs utiles : type `vector` inconnu pour LangChain, SQL invalide généré, timeouts Ollama.

## Quand éviter cette pile

| Cas | Mieux |
|-----|--------|
| Utilisateur sans notes | Métadonnées denses seulement |
| CF à très grande échelle | Stack CF dédiée |
| Latence ms stricte | Vector DB managée + tuning |

## Bilan

**Embed → stocker → voisins** trois fois, trois sens. Partie 3 = humilité sur la génération SQL.

## Articles liés

- [Snowflake Data-for-Breakfast]({{< ref "/posts/snowflake-data-for-breakfast/index.fr.md" >}})
- [Expérimentation indicateurs]({{< ref "/posts/experimentation-indicateurs-backtesting/index.fr.md" >}})

## Références

- [AlgoETS/SimilityVectorEmbedding](https://github.com/AlgoETS/SimilityVectorEmbedding)
- [pgvector](https://github.com/pgvector/pgvector) · [Qdrant](https://qdrant.tech/documentation/)

---

*Publié d’abord sur [Medium](https://medium.com/@antoine.boucher012/using-vector-databases-to-find-similar-movies-algorithm-part-1-f14a244bb23d) ; page fusionnée parties 1–3.*

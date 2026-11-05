---
title: "SimilityVectorEmbedding: movie similarity with vector search"
date: 2026-11-05T12:00:00-05:00
description: "Jupyter notebooks that embed a movie catalog and compare pgvector, Qdrant, BM25, Neo4j and a local LLM for finding similar films."
translationKey: repository-note-similityvectorembedding
repository_note: "SimilityVectorEmbedding"
---

# SimilityVectorEmbedding

<div class="repo-status-row"><span class="repo-badge kind">Notebooks</span><span class="repo-badge docker">Docker</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">Jupyter</span><span class="tag tool">PostgreSQL</span><span class="tag tool">pgvector</span><span class="tag tool">Qdrant</span><span class="tag tool">Neo4j</span><span class="tag tool">Sentence Transformers</span><span class="tag tool">LangChain</span><span class="tag tool">Ollama</span><span class="tag tool">Gradio</span></div>

SimilityVectorEmbedding is a set of Jupyter notebooks that turn a movie catalog into embeddings and look for similar films with several storage and ranking approaches. It is an [AlgoÉTS](https://github.com/AlgoETS) repository for readers who want to see vector search applied to real movie records. The article [Exploring movie similarities with vector search algorithms]({{< ref "/posts/vector-databases-similar-movies/index.md" >}}) tells the same work as a story, with the original demo animations.

## Overview {#overview}

Each folder pairs a notebook with the database it needs. All of them read a `movies.json` file whose records use French keys (`titre`, `annee`, `genre`, `realisateur`, `role`, `synopsis` …) under `films.film`.

- `postgres/0.simple.ipynb` is the shortest full path: it builds one text per film (title, year, genres, actors, director, summary, country, language, writers), encodes it with `sentence-transformers/all-MiniLM-L6-v2` using mean pooling, normalizes the vectors and inserts them into a `movies` table with a `VECTOR(384)` column. Titles typed by the user are matched with `pg_trgm` before cosine similarity ranks the rest of the catalog. It also averages several titles, weights titles by rating, plots the scores and ends with a Gradio interface.
- `postgres/1.create_table.ipynb` encodes the same catalog with five configurations (BART, GTE, MiniLM-L12, RoBERTa and e5-large) and stores one vector column per model.
- `postgres/3.LLMS.ipynb` embeds a natural-language question, runs a pgvector `<=>` cosine query and sends the table schema to a LangChain chain backed by Ollama (`llama2:13b-chat`).
- `qdrant/0.simple.ipynb` upserts 384-dimension vectors in batches of 100 into a cosine collection, searches it, and projects the vectors with t-SNE and k-means.
- `bm25/0.bm25.ipynb` ranks films by keywords with `rank_bm25`, without embeddings.
- `neo4j/1.create_db.ipynb` loads movies and people as a graph and scores neighbours by shared genres, directors, writers and actors.

## Getting started {#installation}

The notebooks install their own packages with `!pip install` cells. Start the database for the notebook you want to run, then open Jupyter:

```shell
git clone https://github.com/AlgoETS/SimilityVectorEmbedding.git
cd SimilityVectorEmbedding/postgres
docker-compose up -d
jupyter notebook
```

`postgres/docker-compose.yml` builds PostgreSQL with pgvector compiled from source and `pg_trgm`, on port 5432. The `qdrant/` and `neo4j/` folders each have their own `docker-compose.yml` (Qdrant on 6333/6334, Neo4j on 7474/7687 with APOC and Graph Data Science). `neo4j/install_ollama.sh` installs Ollama on Linux for the LLM notebook.

## Repository guide {#reader-guide}

- `postgres/0.simple.ipynb`: MiniLM embeddings, title matching, single/multiple/rated searches, bar chart and Gradio UI.
- `postgres/1.create_table.ipynb`: five embedding models stored side by side in PostgreSQL.
- `postgres/3.LLMS.ipynb`: question embedding, pgvector query and LangChain + Ollama prompt.
- `postgres/Dockerfile`, `postgres/docker-compose.yml`, `postgres/init-db.sh`: database image and extension setup.
- `qdrant/0.simple.ipynb`, `qdrant/docker-compose.yml`: the Qdrant version of the search, with clustering plots.
- `bm25/0.bm25.ipynb`: keyword ranking baseline.
- `neo4j/1.create_db.ipynb`, `neo4j/docker-compose.yml`, `neo4j/personnes.json`: graph model of films and people.
- `*/movies.json`: the movie catalog, copied into each folder.

## Features {#features}

- build an embedding text from several movie fields, with English stopwords removed from title and summary;
- compare five Hugging Face / Sentence Transformers models on the same catalog;
- store vectors in PostgreSQL with pgvector and match approximate titles with `pg_trgm`;
- search by one title, the mean of several titles, or a rating-weighted mix of titles;
- run the same idea on Qdrant, then on BM25 keywords and a Neo4j graph for comparison;
- ask questions through a local LLM grounded on the `movies` table;
- view results as bar charts, t-SNE/k-means plots, graph views and a Gradio page.

## Limits {#limits}

- The README asks for `pip install -r requirements.txt` and a `Similarity_Vector_Embedding.ipynb` notebook; neither file is in the repository. Dependencies come from the `!pip install` cells.
- The README schema shows a single `VECTOR(768)` column; the notebooks create per-model columns (384 or 1024 dimensions).
- `postgres/init-db.sh` creates an extension named `pgvector`, while the notebooks create `vector`, the name pgvector registers.
- Notebooks drop and recreate the `movies` table and the Qdrant collection, and use hard-coded local credentials (`postgres/postgres`, `neo4j/password`).
- The LLM notebook needs a running Ollama server with `llama2:13b-chat`; the Gradio cell uses `launch(share=True)`, which opens a public share link.
- There are no tests. Saved notebook outputs show past runs, not benchmarks.

## Sources {#sources}

- [GitHub repository](https://github.com/AlgoETS/SimilityVectorEmbedding)
- [README](https://github.com/AlgoETS/SimilityVectorEmbedding/blob/main/README.md)
- [`postgres/0.simple.ipynb`](https://github.com/AlgoETS/SimilityVectorEmbedding/blob/main/postgres/0.simple.ipynb)
- [`postgres/1.create_table.ipynb`](https://github.com/AlgoETS/SimilityVectorEmbedding/blob/main/postgres/1.create_table.ipynb)
- [`postgres/3.LLMS.ipynb`](https://github.com/AlgoETS/SimilityVectorEmbedding/blob/main/postgres/3.LLMS.ipynb)
- [`qdrant/0.simple.ipynb`](https://github.com/AlgoETS/SimilityVectorEmbedding/blob/main/qdrant/0.simple.ipynb)
- [`neo4j/1.create_db.ipynb`](https://github.com/AlgoETS/SimilityVectorEmbedding/blob/main/neo4j/1.create_db.ipynb)

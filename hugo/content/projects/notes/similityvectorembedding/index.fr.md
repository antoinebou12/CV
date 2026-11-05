---
title: "SimilityVectorEmbedding : trouver des films proches par recherche vectorielle"
date: 2026-11-05T12:00:00-05:00
description: "Carnets Jupyter qui vectorisent un catalogue de films et comparent pgvector, Qdrant, BM25, Neo4j et un LLM local pour trouver des films proches."
translationKey: repository-note-similityvectorembedding
repository_note: "SimilityVectorEmbedding"
---

# SimilityVectorEmbedding

<div class="repo-status-row"><span class="repo-badge kind">Carnets</span><span class="repo-badge docker">Docker</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">Jupyter</span><span class="tag tool">PostgreSQL</span><span class="tag tool">pgvector</span><span class="tag tool">Qdrant</span><span class="tag tool">Neo4j</span><span class="tag tool">Sentence Transformers</span><span class="tag tool">LangChain</span><span class="tag tool">Ollama</span><span class="tag tool">Gradio</span></div>

SimilityVectorEmbedding regroupe des carnets Jupyter qui transforment un catalogue de films en vecteurs, puis cherchent des films semblables avec plusieurs méthodes de stockage et de classement. C’est un dépôt [AlgoÉTS](https://github.com/AlgoETS) pour qui veut voir la recherche vectorielle appliquée à de vraies fiches de films. L’article [Similarité entre films et recherche vectorielle]({{< ref "/posts/vector-databases-similar-movies/index.fr.md" >}}) raconte le même travail, avec les animations de démonstration d’origine.

## Aperçu {#overview}

Chaque dossier associe un carnet à la base de données dont il a besoin. Tous lisent un fichier `movies.json` dont les fiches utilisent des clés en français (`titre`, `annee`, `genre`, `realisateur`, `role`, `synopsis` …) sous `films.film`.

- `postgres/0.simple.ipynb` est le parcours complet le plus court : il compose un texte par film (titre, année, genres, acteurs, réalisateur, résumé, pays, langue, scénaristes), l’encode avec `sentence-transformers/all-MiniLM-L6-v2` par mean pooling, normalise les vecteurs et les insère dans une table `movies` avec une colonne `VECTOR(384)`. Le titre saisi est retrouvé avec `pg_trgm`, puis la similarité cosinus classe le reste du catalogue. Le carnet calcule aussi la moyenne de plusieurs titres, pondère des titres selon une note, trace les scores et se termine par une interface Gradio.
- `postgres/1.create_table.ipynb` encode le même catalogue avec cinq configurations (BART, GTE, MiniLM-L12, RoBERTa et e5-large) et range une colonne de vecteurs par modèle.
- `postgres/3.LLMS.ipynb` vectorise une question en langage naturel, lance une requête cosinus pgvector `<=>` et transmet le schéma de la table à une chaîne LangChain reliée à Ollama (`llama2:13b-chat`).
- `qdrant/0.simple.ipynb` insère des vecteurs de 384 dimensions par lots de 100 dans une collection cosinus, l’interroge et projette les vecteurs avec t-SNE et k-means.
- `bm25/0.bm25.ipynb` classe les films par mots-clés avec `rank_bm25`, sans vecteurs.
- `neo4j/1.create_db.ipynb` charge films et personnes sous forme de graphe et note les voisins selon les genres, réalisateurs, scénaristes et acteurs partagés.

## Démarrage {#installation}

Les carnets installent leurs paquets avec des cellules `!pip install`. Démarrez la base du carnet voulu, puis ouvrez Jupyter :

```shell
git clone https://github.com/AlgoETS/SimilityVectorEmbedding.git
cd SimilityVectorEmbedding/postgres
docker-compose up -d
jupyter notebook
```

`postgres/docker-compose.yml` construit PostgreSQL avec pgvector compilé depuis les sources et `pg_trgm`, sur le port 5432. Les dossiers `qdrant/` et `neo4j/` ont chacun leur `docker-compose.yml` (Qdrant sur 6333/6334, Neo4j sur 7474/7687 avec APOC et Graph Data Science). `neo4j/install_ollama.sh` installe Ollama sous Linux pour le carnet LLM.

## Guide du dépôt {#reader-guide}

- `postgres/0.simple.ipynb` : vecteurs MiniLM, correspondance de titres, recherches simple, multiple ou pondérée, graphique en barres et interface Gradio.
- `postgres/1.create_table.ipynb` : cinq modèles de vectorisation rangés côte à côte dans PostgreSQL.
- `postgres/3.LLMS.ipynb` : vectorisation de la question, requête pgvector et invite LangChain + Ollama.
- `postgres/Dockerfile`, `postgres/docker-compose.yml`, `postgres/init-db.sh` : image de la base et activation des extensions.
- `qdrant/0.simple.ipynb`, `qdrant/docker-compose.yml` : la version Qdrant de la recherche, avec graphiques de regroupement.
- `bm25/0.bm25.ipynb` : point de comparaison par mots-clés.
- `neo4j/1.create_db.ipynb`, `neo4j/docker-compose.yml`, `neo4j/personnes.json` : modèle en graphe des films et des personnes.
- `*/movies.json` : le catalogue de films, copié dans chaque dossier.

## Fonctionnalités {#features}

- composer le texte à vectoriser à partir de plusieurs champs, en retirant les mots vides anglais du titre et du résumé ;
- comparer cinq modèles Hugging Face / Sentence Transformers sur le même catalogue ;
- stocker les vecteurs dans PostgreSQL avec pgvector et retrouver des titres approximatifs avec `pg_trgm` ;
- chercher à partir d’un titre, de la moyenne de plusieurs titres ou d’un mélange pondéré par des notes ;
- reprendre la même idée avec Qdrant, puis avec BM25 et un graphe Neo4j pour comparer ;
- poser des questions à un LLM local appuyé sur la table `movies` ;
- lire les résultats en graphiques à barres, projections t-SNE/k-means, vues de graphe et page Gradio.

## Limites {#limits}

- Le README demande `pip install -r requirements.txt` et un carnet `Similarity_Vector_Embedding.ipynb` ; aucun des deux fichiers n’est dans le dépôt. Les dépendances viennent des cellules `!pip install`.
- Le schéma du README montre une seule colonne `VECTOR(768)` ; les carnets créent une colonne par modèle (384 ou 1024 dimensions).
- `postgres/init-db.sh` crée une extension nommée `pgvector`, alors que les carnets créent `vector`, le nom enregistré par pgvector.
- Les carnets suppriment puis recréent la table `movies` et la collection Qdrant, et utilisent des identifiants locaux codés en dur (`postgres/postgres`, `neo4j/password`).
- Le carnet LLM exige un serveur Ollama avec `llama2:13b-chat` ; la cellule Gradio appelle `launch(share=True)`, qui ouvre un lien de partage public.
- Il n’y a pas de tests. Les sorties enregistrées dans les carnets montrent des exécutions passées, pas des mesures de performance.

## Sources {#sources}

- [Dépôt GitHub](https://github.com/AlgoETS/SimilityVectorEmbedding)
- [README](https://github.com/AlgoETS/SimilityVectorEmbedding/blob/main/README.md)
- [`postgres/0.simple.ipynb`](https://github.com/AlgoETS/SimilityVectorEmbedding/blob/main/postgres/0.simple.ipynb)
- [`postgres/1.create_table.ipynb`](https://github.com/AlgoETS/SimilityVectorEmbedding/blob/main/postgres/1.create_table.ipynb)
- [`postgres/3.LLMS.ipynb`](https://github.com/AlgoETS/SimilityVectorEmbedding/blob/main/postgres/3.LLMS.ipynb)
- [`qdrant/0.simple.ipynb`](https://github.com/AlgoETS/SimilityVectorEmbedding/blob/main/qdrant/0.simple.ipynb)
- [`neo4j/1.create_db.ipynb`](https://github.com/AlgoETS/SimilityVectorEmbedding/blob/main/neo4j/1.create_db.ipynb)

# SimilityVectorEmbedding : trouver des films proches par recherche vectorielle

> Carnets Jupyter qui vectorisent un catalogue de films et comparent pgvector, Qdrant, BM25, Neo4j et un LLM local pour trouver des films proches.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/similityvectorembedding/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/similityvectorembedding/index.md
- Publié: 2026-11-05
- Mis à jour: 2026-11-05
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/AlgoETS/SimilityVectorEmbedding
- Révision inspectée: f3db0326f06dcadc56e0809fa054135f0ecacfc5


## Cas d’utilisation

Carnets Jupyter qui vectorisent un catalogue de films et trouvent des films proches avec pgvector, Qdrant, BM25, Neo4j et Ollama.

- **Vectoriser le catalogue** (Apprenant, Base en conteneur): postgres/1.create_table.ipynb compose un texte par film à partir de movies.json et l’encode avec BART, GTE, MiniLM-L12, RoBERTa et e5-large, avec une colonne de vecteurs par modèle.
- **Trouver des films proches** (Apprenant, Base en conteneur): postgres/0.simple.ipynb retrouve le titre saisi avec pg_trgm, puis classe le catalogue par similarité cosinus pour un titre, plusieurs titres ou des titres notés.
- **Chercher dans Gradio** (Apprenant, Base en conteneur): Les dernières cellules de postgres/0.simple.ipynb lancent une interface Gradio (modes Single, Multiple et Ratings) qui affiche affiches, années et scores.
- **Chercher avec Qdrant** (Apprenant, Base en conteneur): qdrant/0.simple.ipynb insère des vecteurs MiniLM de 384 dimensions dans une collection cosinus, l’interroge et projette les vecteurs avec t-SNE et k-means.
- **Interroger un LLM local** (Apprenant, Base en conteneur, LLM local (Ollama)): postgres/3.LLMS.ipynb vectorise une question, lance une requête cosinus pgvector et transmet le schéma à une chaîne LangChain reliée à Ollama llama2:13b-chat.
- **Comparer BM25 et graphe Neo4j** (Apprenant, Base en conteneur): bm25/0.bm25.ipynb classe les films par mots-clés avec rank_bm25, et neo4j/1.create_db.ipynb les note selon les genres, réalisateurs, scénaristes et acteurs partagés.

### Scénario : Trouver des films proches de The Matrix

1. Démarrer PostgreSQL avec pgvector et pg_trgm : cd postgres, puis docker-compose up -d.
2. Ouvrir postgres/0.simple.ipynb avec jupyter notebook et exécuter les cellules d’installation et d’import.
3. Exécuter main() pour charger movies.json, vectoriser chaque film avec all-MiniLM-L6-v2 et l’insérer dans la table movies.
4. Appeler find_similar_movies(conn, cur, "The Matrix") pour obtenir les titres les plus proches au-dessus d’un seuil cosinus de 0,5.
5. Tracer le résultat avec plot_similar_movies ou refaire la recherche dans l’interface Gradio.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Jupyter Notebook | 99.9 |
| Shell | 0.09 |
| Dockerfile | 0.01 |



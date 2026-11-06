# SimilityVectorEmbedding: movie similarity with vector search

> Jupyter notebooks that embed a movie catalog and compare pgvector, Qdrant, BM25, Neo4j and a local LLM for finding similar films.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/similityvectorembedding/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/similityvectorembedding/index.md
- Published: 2026-11-05
- Updated: 2026-11-05
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/AlgoETS/SimilityVectorEmbedding
- Inspected revision: f3db0326f06dcadc56e0809fa054135f0ecacfc5


## Use cases

Jupyter notebooks that embed a movie catalog and find similar films with pgvector, Qdrant, BM25, Neo4j and Ollama.

- **Embed the movie catalog** (Learner, Database container): postgres/1.create_table.ipynb builds one text per film from movies.json and encodes it with BART, GTE, MiniLM-L12, RoBERTa and e5-large, storing one vector column per model.
- **Find films like a title** (Learner, Database container): postgres/0.simple.ipynb resolves the typed title with pg_trgm, then ranks the catalog by cosine similarity for one title, several titles or rated titles.
- **Search from a Gradio page** (Learner, Database container): The last cells of postgres/0.simple.ipynb launch a Gradio interface with Single, Multiple and Ratings modes that shows posters, years and similarity scores.
- **Search with Qdrant** (Learner, Database container): qdrant/0.simple.ipynb upserts 384-dimension MiniLM vectors into a cosine collection, searches it and projects the vectors with t-SNE and k-means.
- **Ask a local LLM** (Learner, Database container, Local LLM (Ollama)): postgres/3.LLMS.ipynb embeds a question, runs a pgvector cosine query and passes the schema to a LangChain chain backed by Ollama llama2:13b-chat.
- **Compare BM25 and graph search** (Learner, Database container): bm25/0.bm25.ipynb ranks films by keywords with rank_bm25, and neo4j/1.create_db.ipynb scores films by shared genres, directors, writers and actors.

### Scenario: Find films like The Matrix

1. Start PostgreSQL with pgvector and pg_trgm: cd postgres, then docker-compose up -d.
2. Open postgres/0.simple.ipynb with jupyter notebook and run the pip install and import cells.
3. Run main() to load movies.json, embed each film with all-MiniLM-L6-v2 and insert it into the movies table.
4. Call find_similar_movies(conn, cur, "The Matrix") to get the closest titles above a 0.5 cosine threshold.
5. Plot the result with plot_similar_movies or try the same search in the Gradio interface.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Jupyter Notebook | 99.9 |
| Shell | 0.09 |
| Dockerfile | 0.01 |



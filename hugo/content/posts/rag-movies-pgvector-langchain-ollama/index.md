---
post_kind: article
title: "Grounding movie Q&A with embeddings, LangChain, and Ollama"
date: 2026-04-13T12:00:00-04:00
tags:
    - RAG
    - LangChain
    - pgvector
    - Ollama
    - PostgreSQL
    - Embeddings
    - Python
---

This post is a follow-up to [Exploring movie similarities with vector search (pgvector + Qdrant)]({{< ref "/posts/vector-databases-similar-movies/index.md" >}}), where we stored movie embeddings in PostgreSQL with pgvector, compared distance metrics, and extended the same ideas to Qdrant and MovieLens. Here the same dataset becomes the **retrieval layer** for a small **retrieve-then-generate** pipeline: embed the user question, pull the nearest rows in SQL, then let a local LLM explain the results with LangChain and Ollama.

The reference implementation lives in the teaching repo **SimilityVectorEmbedding**, notebook `postgres/3.LLMS.ipynb` ([AlgoETS/SimilityVectorEmbedding](https://github.com/AlgoETS/SimilityVectorEmbedding)).

## Why not only ChatGPT?

A plain prompt like “movies similar to *The Incredibles*” draws on the open web, not on *your* catalog. The notebook contrasts that behavior with recommendations constrained to rows that actually exist in your `movies` table—same theme as RAG: **ground the model in evidence you control**.

## Pipeline at a glance

```mermaid
flowchart LR
  Q[User question] --> E[HuggingFaceEmbeddings]
  E --> SQL[SQL with pgvector kNN]
  SQL --> Rows[Top movie rows]
  Rows --> LLM[Ollama LLM via LangChain]
  LLM --> A[Natural language answer]
```

## Retrieval: question to SQL + vectors

1. **Embedding the question** — `HuggingFaceEmbeddings` with `sentence-transformers/all-MiniLM-L12-v2` (`embed_query`).
2. **Similarity in SQL** — The notebook builds a query that orders by cosine-style distance on `embedding_MiniLM`, e.g. using the pgvector `<=>` operator and `1 - (embedding_MiniLM <=> ARRAY[...]::vector) AS cosine_similarity`, with `ORDER BY cosine_similarity DESC` and `LIMIT 5`.

That step is the bridge to the pgvector section in the main post: same vectors and `<=>` idea, but the **query vector** comes from free text instead of an existing movie row.

## Generation: schema-aware prompting + Ollama

The notebook wires **LangChain**: a `ChatPromptTemplate` describes the `movies` table (including embedding columns), asks for PostgreSQL-friendly behavior, and instructs the model to return question, SQL, formatted results, and a short natural-language answer. The runnable chain uses **`Ollama(model="llama2:13b-chat")`** and `StrOutputParser()`.

`ConversationBufferMemory` is created in the notebook; the demonstrated flow is still essentially **one-shot** invocations per question.

## What goes wrong in practice (and why it matters)

The saved notebook output is useful precisely because it is messy:

- **SQLAlchemy / LangChain** warns that it does not recognize the `vector` type on embedding columns when reflecting the schema.
- The LLM sometimes emits **SQL that does not match pgvector semantics** (for example treating embeddings like scalars with `@>` or `ANY(...)` in ways that are not valid for your schema).
- **Ollama** can **time out** under load (`llama2:13b-chat` is heavy); one of the parallel test questions fails with a runner timeout.

Those issues are normal teaching points: RAG is not only “embed and search”—you need validation, fallbacks, smaller models, or hybrid retrieval when the generator drifts from executable SQL.

## Running it yourself

You need PostgreSQL with pgvector, movie rows populated as in the pgvector section of [that post]({{< ref "/posts/vector-databases-similar-movies/index.md" >}}), **Ollama** with the chosen model pulled, and the Python stack from the notebook (`langchain`, `langchain-community`, `langchain-huggingface`, `psycopg2`, etc.). Adjust connection strings and model names to match your environment.

## Related material

- [Exploring movie similarities with vector search (pgvector + Qdrant)]({{< ref "/posts/vector-databases-similar-movies/index.md" >}})
- [SimilityVectorEmbedding on GitHub](https://github.com/AlgoETS/SimilityVectorEmbedding) — `postgres/3.LLMS.ipynb`

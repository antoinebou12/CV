---
title: WordUnveil
linkTitle: WordUnveil
date: 2021-09-06T22:42:23+08:00
description: "Jeu multilingue façon Wordle avec RedwoodJS, GraphQL et Prisma."
draft: false
---

# WordUnveil

![License](https://img.shields.io/badge/license-MIT-green)
![Redwood](https://img.shields.io/badge/-RedwoodJS-B7410E?logo=redwoodjs)
![GraphQL](https://img.shields.io/badge/-GraphQL-E10098?logo=graphql)
![Prisma](https://img.shields.io/badge/-Prisma-2D3748?logo=prisma)
![MySQL](https://img.shields.io/badge/-MySQL-4479A1?logo=mysql)

Variante multilingue du jeu Wordle pour découvrir du vocabulaire tout en jouant. Stack : RedwoodJS, GraphQL, Prisma et MySQL.

## Démarrage

**En développement**

```bash
cd WordUnveil
yarn install
cp .env.default .env
yarn rw prisma migrate dev
yarn rw exec seed
yarn rw dev
```

**Docker Compose**

```bash
docker-compose up -d
```

**PostgreSQL seul**

```bash
docker run --name=db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -p '5432:5432' -d postgres
```

## Déploiement

```bash
yarn rw deploy baremetal production --first-run
```

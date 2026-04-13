---
title: WordUnveil
linkTitle: WordUnveil # The title of left navigation, optional.
date: 2021-09-06T22:42:23+08:00
description: "Multilingual Wordle-style game built with RedwoodJS, GraphQL, and Prisma."
draft: false
---


# WordsUnveil
![License](https://img.shields.io/badge/license-MIT-green)
![Redwood](https://img.shields.io/badge/-RedwoodJS-B7410E?logo=redwoodjs)
![GraphQL](https://img.shields.io/badge/-GraphQL-E10098?logo=graphql)
![Prisma](https://img.shields.io/badge/-Prisma-2D3748?logo=prisma)
![MySQL](https://img.shields.io/badge/-MySQL-4479A1?logo=mysql)

WordsEnigma is a multilingual twist on the popular game Wordle, providing a fun and educational way to learn new languages. Built with advanced technologies for efficiency and a seamless gaming experience.

## Getting Started

**Development Setup**
WordsUnveil is a multilingual twist on the popular game Wordle, providing a fun and educational way to learn new languages. Built with advanced technologies for efficiency and a seamless gaming experience.

## Getting Started

**Development Setup**

```bash
# Navigate to the WordsUnveil directory
cd WordsUnveil

# Install dependencies
yarn install

# Copy default environment variables
cp .env.default .env

# Run database migrations
yarn rw prisma migrate dev

# (Optional) Seed the database
yarn rw exec seed

# Start the development server
yarn rw dev
```

**Docker-Compose Setup**

```bash
# Start services with Docker
docker-compose up -d
```

**PostgreSQL Database Setup**

```bash
# Create PostgreSQL container named `db`
docker run --name=db -e POSTGRES_USER=admin -e POSTGRES_PASSWORD=admin -p '5432:5432' -d postgres
```

## Deployment

Deploy the application to a bare metal server in production mode.

```bash
# Initial deployment
yarn rw deploy baremetal production --first-run
```
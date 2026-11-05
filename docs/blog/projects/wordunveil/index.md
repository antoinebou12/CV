# WordUnveil

> Multilingual Wordle-style game built with RedwoodJS, GraphQL, and Prisma.

- HTML page: https://antoineboucher.info/CV/blog/projects/wordunveil/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/wordunveil/index.md
- Published: 2021-09-06
- Updated: 2021-09-06
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)# WordsUnveil
![License](https://img.shields.io/badge/license-MIT-green)
![Redwood](https://img.shields.io/badge/-RedwoodJS-B7410E?logo=redwoodjs)
![GraphQL](https://img.shields.io/badge/-GraphQL-E10098?logo=graphql)
![Prisma](https://img.shields.io/badge/-Prisma-2D3748?logo=prisma)
![MySQL](https://img.shields.io/badge/-MySQL-4479A1?logo=mysql)

WordUnveil is a multilingual Wordle-style game. Stack: RedwoodJS, GraphQL, Prisma, and MySQL.

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

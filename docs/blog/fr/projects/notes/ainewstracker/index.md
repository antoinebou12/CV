# AINewsTracker : analyser l’actualité financière et la backtester

> AINewsTracker combine collecte d’actualités financières, analyse par IA et backtesting dans une application web Python.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/ainewstracker/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/ainewstracker/index.md
- Publié: 2026-10-24
- Mis à jour: 2026-10-24
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/AlgoETS/AINewsTracker
- Révision inspectée: 74a8366f5c19e352277a74381559e310e9cf959c


## Cas d’utilisation

Service FastAPI d'AlgoÉTS qui collecte des nouvelles financières, les note avec FinBERT et les range dans MongoDB.

- **Récupérer des nouvelles** (Analyste quantitatif, Sources de nouvelles): Les routes /news interrogent le flux RSS 8-K de Financial Modeling Prep, GNews ou un flux nommé avec feedparser, téléchargent le texte de chaque article et l'enregistrent ; au-delà de 10, le travail passe en tâche de fond.
- **Noter le sentiment** (Analyste quantitatif): TextMetrics charge ProsusAI/finbert pour le sentiment, Jean-Baptiste/roberta-ticker pour repérer les tickers et distilbart-cnn-12-6 pour les résumés ; GET /articles/{article_id}/score renvoie la note enregistrée.
- **Chercher par entreprise** (Analyste quantitatif): /company enregistre les tickers, et /articles/articles_by_company_id/{company_id} ou POST /articles/articles_by_company_ids renvoient les articles liés à une ou plusieurs entreprises.
- **Charger sociétés et nouvelles** (Analyste quantitatif, Sources de nouvelles): POST /seed/seed_companies et /seed/seed_news lancent CompanySeeder et NewsSeeder en tâche de fond ; NewsSeeder lit les nouvelles boursières de Financial Modeling Prep avec FMP_API_KEY et enregistre les articles dans MongoDB.
- **Fournir les articles notés** (Service de backtest): GET /v1/articles, protégé par un jeton de service Bearer (AINEWSTRACKER_SERVICE_TOKEN), renvoie les articles filtrés par symboles et période, avec étiquette de sentiment, probabilités et nom du modèle, paginés par curseur.

### Scénario : Collecter et interroger les nouvelles d'Apple en local

1. Copier .env.example en .env, renseigner FMP_API_KEY, puis lancer docker-compose up --build pour démarrer l'API avec MongoDB et Redis.
2. Ouvrir http://localhost:8000/api/v1/docs et appeler POST /seed/seed_companies.
3. Appeler POST /seed/seed_news ; NewsSeeder lit les nouvelles boursières de Financial Modeling Prep en tâche de fond et enregistre les articles notés.
4. Lire les articles avec GET /articles/ et vérifier l'un d'eux avec GET /articles/{article_id}/score.
5. Depuis un service de backtest, appeler GET /v1/articles?symbols=AAPL avec le jeton de service Bearer.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Python | 88.92 |
| Shell | 8.19 |
| Dockerfile | 2.9 |



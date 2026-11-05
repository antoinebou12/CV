# AINewsTracker: Financial news analysis and backtesting

> AINewsTracker combines financial-news ingestion, AI analysis and market backtesting in a Python web application.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/ainewstracker/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/ainewstracker/index.md
- Published: 2026-10-24
- Updated: 2026-10-24
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/AlgoETS/AINewsTracker


## Use cases

FastAPI service from AlgoÉTS that collects financial news, scores it with FinBERT and stores it in MongoDB.

- **Fetch news from a source** (Quant analyst, News feeds and APIs): The /news routes pull the Financial Modeling Prep 8-K RSS feed, GNews or a named feed with feedparser, download each article's text and save it; limits above 10 run as background tasks.
- **Score article sentiment** (Quant analyst): TextMetrics loads ProsusAI/finbert for sentiment, Jean-Baptiste/roberta-ticker for ticker extraction and distilbart-cnn-12-6 for summaries; GET /articles/{article_id}/score returns the stored score.
- **Query news by company** (Quant analyst): /company stores tickers, and /articles/articles_by_company_id/{company_id} or POST /articles/articles_by_company_ids return the articles linked to one or more companies.
- **Seed companies and news** (Quant analyst, News feeds and APIs): POST /seed/seed_companies and /seed/seed_news start CompanySeeder and NewsSeeder in the background; NewsSeeder reads Financial Modeling Prep stock news with FMP_API_KEY and saves the articles to MongoDB.
- **Serve scored articles** (Backtesting service): GET /v1/articles, protected by a Bearer service token (AINEWSTRACKER_SERVICE_TOKEN), returns articles filtered by symbols and time window with sentiment label, probabilities and model name, paged by cursor.

### Scenario: Collect and query Apple news locally

1. Copy .env.example to .env, set FMP_API_KEY, then run docker-compose up --build to start the API with MongoDB and Redis.
2. Open http://localhost:8000/api/v1/docs and call POST /seed/seed_companies.
3. Call POST /seed/seed_news; NewsSeeder reads Financial Modeling Prep stock news in the background and stores the scored articles.
4. Read the stored articles with GET /articles/ and check one with GET /articles/{article_id}/score.
5. From a backtesting service, call GET /v1/articles?symbols=AAPL with the Bearer service token.



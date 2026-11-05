# Simulateur: a Django stock-market simulation game

> Simulateur is a Django platform where admins script market scenarios and teams trade simulated stocks with live WebSocket prices.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/simulateur/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/simulateur/index.md
- Published: 2026-11-05
- Updated: 2026-11-05
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/AlgoETS/Simulateur


## Use cases

Django stock-market game where admins run scripted scenarios and teams trade simulated stocks live.

- **Build a scenario** (Simulation admin): The admin dashboard walks through five form steps (settings, companies and stocks, teams, events, review) backed by the scenario and simulation-manager APIs.
- **Run a market simulation** (Simulation admin): manage.py start_simulation sets a simulation to ongoing; SimulationManager then writes OHLC candles from the chosen noise model (Brownian, Perlin, random walk, fBm, Monte Carlo) at each time step.
- **Generate content with AI** (Simulation admin, Ollama LLM): simulation/api/ai_llm.py exposes create-news-ai, create-event-ai, create-trigger-ai, create-company-stock-ai and create-scenario-ai, which prompt an Ollama model (OLLAMA_MODEL, llama3 by default).
- **Join a team** (Player): A team member generates a join link from the team dashboard (team/generate-join-link/) and other players join with it; the same page shows members and leaderboards.
- **Buy and sell stocks** (Player): From /dashboard/, the order form calls POST /api/stock/buy/ or /api/stock/sell/, which check the balance against the latest price, record an order and update holdings.
- **Follow live prices** (Player): The game dashboard opens ws/simulation/<id>/ and Django Channels pushes stock updates, news, events and triggers from SimulationConsumer.

### Scenario: Run the seeded demo simulation

1. In simulateur/, copy env-default to .env and run python3 run.py --install to install packages, migrate, create admin/admin and seed the CSV data.
2. Start the ASGI server and simulation 1 with python3 run.py --start-simulation 1 (Daphne on port 8000).
3. Sign in as admin and open /dashboard/admin to review the scenario, settings and noise function.
4. Open /dashboard/game: candles arrive over the ws/simulation/ WebSocket at each timer step.
5. From /dashboard/, choose the simulation and a stock and press Buy, which calls POST /api/stock/buy/; then check holdings and leaderboards.



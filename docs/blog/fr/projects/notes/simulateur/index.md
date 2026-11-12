# Simulateur : un jeu de simulation boursière en Django

> Simulateur est une plateforme Django où des admins scénarisent un marché et où des équipes échangent des actions simulées en direct.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/simulateur/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/simulateur/index.md
- Publié: 2026-11-05
- Mis à jour: 2026-11-05
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/AlgoETS/Simulateur
- Révision inspectée: 77f9e70c9982784327ac522c6dc6fcd050ad2ffc


## Cas d’utilisation

Jeu boursier Django : les admins lancent des scénarios scriptés et les équipes échangent des actions simulées en direct.

- **Créer un scénario** (Admin de simulation): Le tableau de bord admin suit cinq étapes de formulaire (réglages, entreprises et actions, équipes, événements, révision) appuyées sur les API de scénario et de gestionnaire de simulation.
- **Lancer une simulation** (Admin de simulation): manage.py start_simulation passe une simulation à l’état en cours ; SimulationManager écrit ensuite des chandelles OHLC à partir du modèle de bruit choisi (brownien, Perlin, marche aléatoire, fBm, Monte-Carlo) à chaque pas.
- **Générer du contenu par IA** (Admin de simulation, LLM Ollama): simulation/api/ai_llm.py expose create-news-ai, create-event-ai, create-trigger-ai, create-company-stock-ai et create-scenario-ai, qui interrogent un modèle Ollama (OLLAMA_MODEL, llama3 par défaut).
- **Rejoindre une équipe** (Joueur): Un membre génère un lien d’invitation depuis le tableau d’équipe (team/generate-join-link/) et les autres joueurs s’en servent pour entrer ; la même page affiche membres et classements.
- **Acheter et vendre des actions** (Joueur): Depuis /dashboard/, le formulaire d’ordre appelle POST /api/stock/buy/ ou /api/stock/sell/, qui vérifient le solde au dernier prix, enregistrent l’ordre et mettent à jour les positions.
- **Suivre les cours en direct** (Joueur): Le tableau de jeu ouvre ws/simulation/<id>/ et Django Channels pousse les mises à jour de cours, actualités, événements et déclencheurs depuis SimulationConsumer.

### Scénario : Lancer la simulation de démonstration

1. Dans simulateur/, copier env-default vers .env et exécuter python3 run.py --install pour installer, migrer, créer admin/admin et charger les CSV.
2. Démarrer le serveur ASGI et la simulation 1 avec python3 run.py --start-simulation 1 (Daphne sur le port 8000).
3. Se connecter en admin et ouvrir /dashboard/admin pour revoir le scénario, les réglages et la fonction de bruit.
4. Ouvrir /dashboard/game : les chandelles arrivent par le WebSocket ws/simulation/ à chaque pas de temps.
5. Depuis /dashboard/, choisir la simulation et une action puis cliquer sur Buy, qui appelle POST /api/stock/buy/ ; consulter ensuite positions et classements.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Jupyter Notebook | 56.91 |
| Python | 30.97 |
| HTML | 11.59 |
| Dockerfile | 0.2 |
| CSS | 0.17 |
| Shell | 0.16 |

## Démarrage (commandes du dépôt, non exécutées ici)

### README.md · Run the Complete System

```bash
docker compose --profile all down
docker compose --profile all up -d --build
```




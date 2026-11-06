# Workshop1 : des notebooks pour apprendre Python

> Workshop1 est une série de notebooks d’AlgoETS qui va des bases de Python et des API à pandas, aux graphiques et à un exercice d’EMA.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/workshop1/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/workshop1/index.md
- Publié: 2026-10-24
- Mis à jour: 2026-10-24
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/AlgoETS/Workshop1
- Révision inspectée: 7858d0e73ce4bee9bff9d6cf455118b8a6cef5f1


## Cas d’utilisation

Atelier AlgoÉTS en français : carnets Jupyter, des bases de Python aux API, à pandas, aux graphiques et à une EMA sur Apple.

- **Préparer son environnement** (Participant, Jupyter ou Colab): 0.1_python_environement présente virtualenv, Anaconda et Jupyter Lab ; 0.2_jupyter_cloud montre DeepNote et Google Colab, et le README pointe vers une copie Colab du premier carnet.
- **Apprendre les bases de Python** (Participant, Jupyter ou Colab): 1.1_python_basic et 1.2_python_advanced couvrent variables, structures de contrôle, lecture de fichier (monfichier.txt) et une petite base SQLite (ma_base.db).
- **Appeler une API web** (Participant, Jupyter ou Colab): 2.1_python_api explique les verbes REST, les codes d'état, les jetons Bearer, les clés d'API et OAuth, avec des exemples requests et httpx asynchrone.
- **Nettoyer des données (pandas)** (Participant): 3.1_python_panda présente les DataFrame, le filtrage avec loc et iloc, les valeurs manquantes, les fusions, les indicateurs pandas_ta et une comparaison avec polars.
- **Tracer une EMA sur Apple** (Participant, API de cours FMP): 5.1_project_ema récupère les cours journaliers d'AAPL via historical-price-full de FMP, calcule une EMA 20 jours avec ewm de pandas et la trace avec la clôture dans Matplotlib ; 4.2 ajoute SMM, RSI et MACD.

### Scénario : Suivre l'atelier jusqu'au projet EMA

1. Cloner https://github.com/AlgoETS/Workshop1.git et lancer pip install -r requirements.txt.
2. Démarrer jupyter notebook, ou ouvrir 1.0-basic/1.1_python_basic.ipynb dans Google Colab depuis le lien du README.
3. Parcourir 1.0-basic, 2.0-api et 3.0-data dans l'ordre.
4. Ouvrir 5.0-project/5.1_project_ema.ipynb et remplacer YOUR_API_KEY par une clé Financial Modeling Prep.
5. Exécuter les cellules pour charger les cours d'AAPL dans un DataFrame, ajouter EMA_20 et tracer la clôture avec l'EMA 20 jours.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Jupyter Notebook | 100 |



---
title: "Salary : explorer les guides salariaux et les données de salaires au Canada"
date: 2026-11-05T12:00:00-05:00
description: "Salary extrait des guides salariaux canadiens en PDF et les salaires du Guichet-Emplois avec Python, puis compare la paie par poste, province et région."
translationKey: repository-note-salary
repository_note: "Salary"
---

# Salary

<div class="repo-status-row"><span class="repo-badge kind">Analyse de données</span><span class="repo-badge api">API</span><span class="repo-badge docker">Docker</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">pandas</span><span class="tag tool">Polars</span><span class="tag tool">PyPDF2</span><span class="tag tool">Jupyter</span><span class="tag tool">FastAPI</span><span class="tag tool">BeautifulSoup</span><span class="tag tool">pre-commit</span></div>

Salary est un projet de données d’AlgoÉTS sur la rémunération au Canada. Il transforme des guides salariaux de firmes de recrutement (PDF) et des tableaux de salaires fédéraux (CSV) en tableaux de données, puis compare les postes entre provinces, régions et niveaux d’expérience. Il sert à voir, par exemple, comment un architecte infonuagique est payé d’une région à l’autre, et intéressera aussi ceux qui veulent extraire des tableaux de rapports PDF.

## Aperçu {#overview}

L’extraction des PDF repose sur un script par édition de guide. `src/pdf_salary_scraper_2023_1.py` et `src/pdf_salary_scraper_2024_1.py` lisent un guide de `data/pdf/` avec PyPDF2, suivent la province et la région courantes à partir de listes de noms fixes, séparent chaque ligne en un titre de poste et trois fourchettes (junior, intermédiaire et senior) et enregistrent le résultat en pickle dans `data/pickle/`. `src/pdf.py` est un essai antérieur avec PyMuPDF qui étiquette le texte selon la taille de police pour repérer les titres.

`src/wages_in_time.py` charge les fichiers du Guichet-Emplois `data/csv/wage_2012.csv` à `wage_2022.csv` avec Polars, harmonise les noms de colonnes d’une année à l’autre, met la table combinée en cache dans `data/pickle/wages.pkl` et affiche les postes les mieux payés par année ainsi que les postes d’ingénierie les mieux payés par province. `src/stackoverflow_scraper.py` récupère le tableau des salaires du sondage Stack Overflow 2022.

L’analyse se fait dans `sandbox/salary_exploration_2023.ipynb` et `sandbox/salary_exploration_2024.ipynb`, avec des versions des mêmes fonctions dans `src/analyse.py` : séparer les fourchettes, calculer les moyennes par niveau, classer les postes, filtrer l’ingénierie et le Québec, comparer un poste entre régions et provinces et trouver les postes aux plus grands écarts régionaux. `api/app.py` expose les pickles 2023 et 2024 en JSON avec FastAPI, et `web/` contient deux pages HTML statiques.

## Démarrage {#installation}

Le README donne ces étapes :

```bash
pip install -r requirements.txt
python src/pdf.py
jupyter notebook
```

Lancez les scripts d’extraction depuis la racine du dépôt, car ils utilisent des chemins comme `data/pdf/2023_salary_guide.pdf` :

```bash
python src/pdf_salary_scraper_2023_1.py
python src/wages_in_time.py
```

`api/setup.md` décrit le déploiement de l’API avec Docker et Vercel ; en local, on peut la démarrer avec uvicorn depuis le répertoire `api/` :

```bash
cd api
uvicorn app:app --reload
```

## Guide du dépôt {#reader-guide}

- `src/pdf_salary_scraper_2023_1.py` et `src/pdf_salary_scraper_2024_1.py` extraient les guides 2023 et 2024 (le README indique Randstad comme source) ; les scripts `_2` et `generic_wip` en sont des variantes sous forme de fonctions.
- `src/wages_in_time.py` combine les tableaux de salaires 2012 à 2022 du Guichet-Emplois.
- `src/stackoverflow_scraper.py` récupère le tableau des salaires du sondage Stack Overflow.
- `src/analyse.py` et `src/utils.py` regroupent les fonctions d’analyse et de pickle ; `src/__init__.py` liste provinces et régions.
- `sandbox/` contient les carnets d’exploration 2023 et 2024 et une comparaison 2023-2024.
- `data/pdf/`, `data/csv/`, `data/pickle/` et `data/geo/` contiennent les guides de plusieurs firmes de recrutement, les tableaux de salaires, les pickles extraits et des fichiers de formes des provinces ; `data/csv/README.md` décrit les colonnes des salaires.
- `api/` contient l’application FastAPI, le Dockerfile, le fichier Compose et les notes de déploiement.
- `web/index.html` présente des résultats 2023 en texte statique ; `web/job_search.html` est une maquette de formulaire de recherche.

## Fonctionnalités {#features}

- extraire poste, province, région et fourchettes junior, intermédiaire et senior des guides salariaux en PDF ;
- réunir onze années de tableaux de salaires du Guichet-Emplois dans un seul tableau Polars ;
- classer les postes selon le salaire maximal, au total, par année, par province et pour l’ingénierie ;
- comparer un poste entre régions et provinces et trouver les plus grands écarts régionaux ;
- récupérer les salaires du sondage Stack Overflow ;
- servir les guides 2023 et 2024 extraits en JSON avec FastAPI.

## Limites {#limits}

- Le README annonce un modèle de prédiction des salaires selon la région, l’expérience et la scolarité ; le dépôt contient du code d’extraction et d’exploration, mais aucun modèle.
- Les commandes du README nomment `src/pdf_salary_scraper.py` et un `stackoverflow_scraper.py` à la racine, qui n’existent pas sous ces noms.
- `requirements.txt` omet PyMuPDF, Polars et BeautifulSoup, que les scripts importent ; `src/wages_in_time.py` utilise une ancienne API de Polars.
- La province et la région viennent du premier nom d’une liste fixe trouvé n’importe où sur la page, la fourchette junior joint le bas de la première paire au haut de la deuxième, et les lignes à quatre fourchettes sont ignorées. Le README et `web/index.html` donnent une réceptionniste bilingue à 713 000 $ comme salaire le plus élevé de 2023, signe d’erreurs d’extraction.
- `src/wages_in_time.py` annualise les salaires horaires avec 40 × 45 heures dans une fonction et 45 × 45 dans une autre, et signale les fichiers 2017 et 2018 comme mal formatés.
- Les fichiers de déploiement se contredisent : `vercel.json` construit un `app.py` à la racine alors que l’application est `api/app.py`, le Dockerfile lance `unicorn` sur le port 8000 alors que Compose publie le port 5000, et l’API lit les pickles par des chemins relatifs `../data`.
- `src/test.py` importe des fonctions qui n’existent pas, et `setup.py` pointe encore vers un répertoire de paquet `code` avec une description héritée d’un gabarit.

## Sources {#sources}

- [Dépôt GitHub](https://github.com/AlgoETS/Salary)
- [README](https://github.com/AlgoETS/Salary/blob/main/README.md)
- [`src/pdf_salary_scraper_2024_1.py`](https://github.com/AlgoETS/Salary/blob/main/src/pdf_salary_scraper_2024_1.py)
- [`src/wages_in_time.py`](https://github.com/AlgoETS/Salary/blob/main/src/wages_in_time.py)
- [`sandbox/salary_exploration_2023.ipynb`](https://github.com/AlgoETS/Salary/blob/main/sandbox/salary_exploration_2023.ipynb)
- [`api/app.py`](https://github.com/AlgoETS/Salary/blob/main/api/app.py)
- [`data/csv/README.md`](https://github.com/AlgoETS/Salary/blob/main/data/csv/README.md)

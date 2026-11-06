# Salary : explorer les guides salariaux et les données de salaires au Canada

> Salary extrait des guides salariaux canadiens en PDF et les salaires du Guichet-Emplois avec Python, puis compare la paie par poste, province et région.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/salary/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/salary/index.md
- Publié: 2026-11-05
- Mis à jour: 2026-11-06
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/AlgoETS/Salary
- Révision inspectée: 40b10f4d6a2a6670400b960c2476d9b7e494eaa1


## Cas d’utilisation

Scripts et carnets Python qui extraient des guides salariaux et tableaux de salaires canadiens pour comparer métiers et régions.

- **Extraire les guides PDF** (Analyste des salaires): src/pdf_salary_scraper_2023_1.py et src/pdf_salary_scraper_2024_1.py lisent un guide de data/pdf avec PyPDF2, suivent province et région, extraient les fourchettes junior, intermédiaire et senior par poste et enregistrent un pickle dans data/pickle.
- **Charger les salaires 2012-2022** (Analyste des salaires): src/wages_in_time.py lit data/csv/wage_2012.csv à wage_2022.csv avec Polars, harmonise les colonnes, met en cache data/pickle/wages.pkl et affiche les postes les mieux payés par année et les postes d’ingénierie par province.
- **Comparer métiers et régions** (Analyste des salaires): sandbox/salary_exploration_2023.ipynb et salary_exploration_2024.ipynb classent les postes par salaire maximal, filtrent l’ingénierie et le Québec, comparent un poste entre régions et provinces et trouvent les plus grands écarts.
- **Collecter Stack Overflow** (Analyste des salaires, Sondage Stack Overflow): src/stackoverflow_scraper.py récupère la page des salaires du sondage Stack Overflow 2022 avec httpx, lit le tableau avec BeautifulSoup et l’enregistre dans data/pickle/stackoverflow_salary_data.pkl.
- **Interroger l’API des salaires** (Client de l’API): api/app.py est une application FastAPI dont les routes /load_pickle/2023 et /salary/2024 renvoient les guides en JSON ; la documentation interactive est à /docs.

### Scénario : Comparer le salaire d’architecte infonuagique au Québec

1. Lancer pip install -r requirements.txt à la racine du dépôt.
2. Placer 2023_salary_guide.pdf dans data/pdf et lancer python src/pdf_salary_scraper_2023_1.py.
3. Vérifier que data/pickle/salary_guide_2023.pkl a été créé.
4. Démarrer jupyter notebook et ouvrir sandbox/salary_exploration_2023.ipynb, qui sépare chaque fourchette et calcule les moyennes par niveau.
5. Appeler compare_job_province('cloud architect', 'québec') pour classer les régions du Québec selon le salaire intermédiaire moyen.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| HTML | 50.9 |
| Jupyter Notebook | 48.1 |
| Python | 0.99 |
| Dockerfile | 0.02 |



# Salary: exploring Canadian salary guides and wage data

> Salary extracts Canadian salary guide PDFs and Job Bank wage tables with Python, then compares pay by job, province and region in notebooks.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/salary/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/salary/index.md
- Published: 2026-11-05
- Updated: 2026-11-05
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/AlgoETS/Salary


## Use cases

Python scripts and notebooks that extract Canadian salary guides and wage tables to compare jobs by region.

- **Extract salary guide PDFs** (Salary analyst): src/pdf_salary_scraper_2023_1.py and src/pdf_salary_scraper_2024_1.py read a guide in data/pdf with PyPDF2, track province and region, parse entry, mid and senior ranges per job and save a pickle in data/pickle.
- **Load 2012–2022 wage tables** (Salary analyst): src/wages_in_time.py reads data/csv/wage_2012.csv to wage_2022.csv with Polars, harmonizes column names, caches data/pickle/wages.pkl and prints the top-paid jobs per year and engineering jobs per province.
- **Compare jobs by region** (Salary analyst): sandbox/salary_exploration_2023.ipynb and salary_exploration_2024.ipynb rank jobs by maximum salary, filter engineering and Québec jobs, compare one job across regions and provinces, and find the widest gaps.
- **Scrape Stack Overflow pay** (Salary analyst, Stack Overflow survey): src/stackoverflow_scraper.py fetches the 2022 Stack Overflow survey salary page with httpx, parses the table with BeautifulSoup and pickles it to data/pickle/stackoverflow_salary_data.pkl.
- **Query salary data over HTTP** (API client): api/app.py is a FastAPI app whose /load_pickle/2023 and /salary/2024 routes return the pickled guides as JSON; interactive documentation is at /docs.

### Scenario: Compare cloud architect pay across Québec regions

1. Run pip install -r requirements.txt from the repository root.
2. Place 2023_salary_guide.pdf in data/pdf and run python src/pdf_salary_scraper_2023_1.py.
3. Check that data/pickle/salary_guide_2023.pkl was written.
4. Start jupyter notebook and open sandbox/salary_exploration_2023.ipynb, which splits each range and computes entry, mid and senior means.
5. Call compare_job_province('cloud architect', 'québec') to rank Québec regions by mean mid-level salary.



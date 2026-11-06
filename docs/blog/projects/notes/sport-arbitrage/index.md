# Sport-Arbitrage: a sports-betting arbitrage calculator

> Sport-Arbitrage is a one-page calculator that checks odds from two betting sites for an arbitrage and computes stakes and guaranteed profit.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/sport-arbitrage/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/sport-arbitrage/index.md
- Published: 2026-11-05
- Updated: 2026-11-06
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/AlgoETS/Sport-Arbitrage
- Inspected revision: dbee18848ac988cd6f99764c3148d5e3349035b2


## Use cases

Browser calculator that checks two bookmakers' odds for a sports-betting arbitrage and splits the stake.

- **Pick 2 or 3 outcomes** (Bettor): The Number of Odds selector in index.html calls toggleOddsFields() in script.js, which shows the two Draw fields only for three outcomes.
- **Enter odds from two sites** (Bettor): The form takes Win and Lost odds for Site 1 and Site 2, optional Draw odds, and the total investment.
- **Detect an arbitrage** (Bettor): calculateArbitrage() tests fixed cross-site pairings; hasArbitrageOpportunity() reports one when the sum of inverse odds is below 1.
- **Split the stake** (Bettor): For each opportunity, script.js prints the arbitrage percentage, optimal stakes, returns per outcome and guaranteed profit.
- **Check the math in Python** (Bettor): arbitrage.ipynb implements the same functions in Python with hard-coded sample odds for the two-outcome case.

### Scenario: Test the notebook's sample odds

1. Open index.html in a browser and keep Number of Odds at 2.
2. Enter Win Site 1 = 1.3, Lost Site 1 = 3.93, Win Site 2 = 1.42 and Lost Site 2 = 2.9.
3. Enter a Total Investment of 100 and click Calculate.
4. Read the result: only the lost-site1 and win-site2 pair qualifies, with stakes of about 26.54 and 73.46.
5. Compare with the guaranteed profit line (about 4.31) and rerun arbitrage.ipynb to check the same numbers.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| JavaScript | 38.34 |
| Jupyter Notebook | 33.46 |
| HTML | 25.5 |
| CSS | 2.7 |



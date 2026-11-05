---
title: "Sport-Arbitrage: a sports-betting arbitrage calculator"
date: 2026-11-05T12:00:00-05:00
description: "Sport-Arbitrage is a one-page calculator that checks odds from two betting sites for an arbitrage and computes stakes and guaranteed profit."
translationKey: repository-note-sport-arbitrage
repository_note: "Sport-Arbitrage"
---

# Sport-Arbitrage

<div class="repo-status-row"><span class="repo-badge kind">Static page</span></div>

<div class="repo-tech-badges"><span class="tag tool">HTML</span><span class="tag tool">JavaScript</span><span class="tag tool">Tailwind CSS</span><span class="tag tool">Python</span><span class="tag tool">Jupyter</span></div>

Sport-Arbitrage is a small web calculator for sports-betting arbitrage: you enter the odds two betting sites give for the same match, and it tells you whether betting on opposite outcomes at both sites locks in a profit, and how to split the stake. It is an [AlgoÉTS](https://github.com/AlgoETS) repository with a browser page and a Python notebook that run the same formulas.

## Overview {#overview}

`index.html` is a single form styled with Tailwind CSS 2.2.19 from a CDN. All the logic is in `script.js`:

- `hasArbitrageOpportunity(odds)` adds the inverses of the odds and reports an opportunity when the sum is below 1.
- `calculateArbitragePercentage` returns `(1 − Σ 1/odds) × 100`.
- `calculateOptimalStakes` splits the total investment in proportion to each inverse odd, so every outcome returns the same amount.
- `calculateTotalReturn` and `calculateGuaranteedProfit` give the return per outcome and the smallest return minus the investment.
- `calculateArbitrage()` reads the form, tests two cross-site pairings (win at site 1 with loss at site 2, and loss at site 1 with win at site 2) and adds a draw to each pairing in three-outcome mode, then writes one result card per opportunity.

`arbitrage.ipynb` contains the same functions in Python, with sample odds hard-coded in the first cell.

## Getting started {#installation}

Nothing needs to be built. Clone the repository and open the page in a browser (the Tailwind stylesheet loads from jsDelivr, so the page needs network access to look right):

```shell
git clone https://github.com/AlgoETS/Sport-Arbitrage.git
cd Sport-Arbitrage
```

Then open `index.html`, choose 2 or 3 odds, fill in the odds and the total investment, and click **Calculate**. To run the Python version:

```shell
jupyter notebook arbitrage.ipynb
```

## Repository guide {#reader-guide}

- `index.html`: the calculator form, instructions and result area.
- `script.js`: field toggling, arbitrage test, stake split, returns and profit display.
- `arbitrage.ipynb`: Python version of the formulas for the two-outcome case.
- `style.css`: basic layout styles (not referenced by `index.html`).

## Features {#features}

- switch between two-outcome (win/loss) and three-outcome (win/loss/draw) markets;
- test cross-site pairings for an arbitrage with the inverse-odds sum;
- show the arbitrage percentage, optimal stakes, return per outcome and guaranteed profit;
- run entirely in the browser, with no server or account;
- check the same math in a Jupyter notebook.

## Limits {#limits}

- Only two fixed pairings are tested. In three-outcome mode, the draw from site 1 always joins win at site 1 and loss at site 2, and the draw from site 2 joins loss at site 1 and win at site 2; other mixes are never tried.
- The formulas assume decimal odds, and the form does not validate input: empty fields produce `NaN`.
- Stakes are not rounded and ignore fees, betting limits and odds changes, so the "guaranteed profit" holds only if every bet is accepted at the entered odds.
- `style.css` is not linked from the page, and the notebook covers only the two-outcome case.
- There are no tests.

## Sources {#sources}

- [GitHub repository](https://github.com/AlgoETS/Sport-Arbitrage)
- [README](https://github.com/AlgoETS/Sport-Arbitrage/blob/main/README.md)
- [`index.html`](https://github.com/AlgoETS/Sport-Arbitrage/blob/main/index.html)
- [`script.js`](https://github.com/AlgoETS/Sport-Arbitrage/blob/main/script.js)
- [`arbitrage.ipynb`](https://github.com/AlgoETS/Sport-Arbitrage/blob/main/arbitrage.ipynb)

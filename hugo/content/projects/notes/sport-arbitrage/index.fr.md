---
title: "Sport-Arbitrage : calculatrice d’arbitrage pour paris sportifs"
date: 2026-11-05T12:00:00-05:00
description: "Sport-Arbitrage est une calculatrice d’une page qui compare les cotes de deux sites de paris, repère un arbitrage et calcule mises et profit."
translationKey: repository-note-sport-arbitrage
repository_note: "Sport-Arbitrage"
---

# Sport-Arbitrage

<div class="repo-status-row"><span class="repo-badge kind">Page statique</span></div>

<div class="repo-tech-badges"><span class="tag tool">HTML</span><span class="tag tool">JavaScript</span><span class="tag tool">Tailwind CSS</span><span class="tag tool">Python</span><span class="tag tool">Jupyter</span></div>

Sport-Arbitrage est une petite calculatrice web pour l’arbitrage en paris sportifs : on saisit les cotes que deux sites offrent pour un même match, et elle indique si parier sur des issues opposées aux deux endroits assure un gain, puis comment répartir la mise. C’est un dépôt [AlgoÉTS](https://github.com/AlgoETS) qui contient une page web et un carnet Python reposant sur les mêmes formules.

## Aperçu {#overview}

`index.html` est un formulaire unique mis en forme avec Tailwind CSS 2.2.19 chargé depuis un CDN. Toute la logique se trouve dans `script.js` :

- `hasArbitrageOpportunity(odds)` additionne les inverses des cotes et signale une occasion quand la somme est inférieure à 1.
- `calculateArbitragePercentage` renvoie `(1 − Σ 1/cote) × 100`.
- `calculateOptimalStakes` répartit la mise totale proportionnellement à l’inverse de chaque cote, pour que chaque issue rapporte le même montant.
- `calculateTotalReturn` et `calculateGuaranteedProfit` donnent le gain par issue, puis le plus petit gain moins la mise.
- `calculateArbitrage()` lit le formulaire, teste deux paires entre les sites (victoire au site 1 avec défaite au site 2, et défaite au site 1 avec victoire au site 2), ajoute un match nul à chaque paire en mode trois issues, puis affiche une carte par occasion.

`arbitrage.ipynb` reprend les mêmes fonctions en Python, avec des cotes d’exemple codées en dur dans la première cellule.

## Démarrage {#installation}

Rien à compiler. Clonez le dépôt et ouvrez la page dans un navigateur (la feuille Tailwind vient de jsDelivr : sans réseau, la mise en forme manque) :

```shell
git clone https://github.com/AlgoETS/Sport-Arbitrage.git
cd Sport-Arbitrage
```

Ouvrez ensuite `index.html`, choisissez 2 ou 3 cotes, remplissez les cotes et la mise totale, puis cliquez sur **Calculate**. Pour la version Python :

```shell
jupyter notebook arbitrage.ipynb
```

## Guide du dépôt {#reader-guide}

- `index.html` : formulaire de la calculatrice, consignes et zone de résultats.
- `script.js` : affichage des champs, test d’arbitrage, répartition de la mise, gains et profit.
- `arbitrage.ipynb` : version Python des formules pour le cas à deux issues.
- `style.css` : styles de mise en page de base (non référencés par `index.html`).

## Fonctionnalités {#features}

- passer d’un marché à deux issues (victoire/défaite) à un marché à trois issues (victoire/défaite/nul) ;
- tester des paires entre les deux sites avec la somme des inverses des cotes ;
- afficher le pourcentage d’arbitrage, les mises optimales, le gain par issue et le profit garanti ;
- tout calculer dans le navigateur, sans serveur ni compte ;
- vérifier les mêmes calculs dans un carnet Jupyter.

## Limites {#limits}

- Seules deux paires fixes sont testées. En mode trois issues, le nul du site 1 accompagne toujours la victoire au site 1 et la défaite au site 2, et le nul du site 2 la défaite au site 1 et la victoire au site 2 ; les autres combinaisons ne sont jamais essayées.
- Les formules supposent des cotes décimales, et le formulaire ne valide pas les saisies : un champ vide donne `NaN`.
- Les mises ne sont pas arrondies et ignorent frais, plafonds de mise et variations de cotes : le « profit garanti » ne tient que si chaque pari est accepté aux cotes saisies.
- `style.css` n’est pas relié à la page, et le carnet ne couvre que le cas à deux issues.
- Il n’y a pas de tests.

## Sources {#sources}

- [Dépôt GitHub](https://github.com/AlgoETS/Sport-Arbitrage)
- [README](https://github.com/AlgoETS/Sport-Arbitrage/blob/main/README.md)
- [`index.html`](https://github.com/AlgoETS/Sport-Arbitrage/blob/main/index.html)
- [`script.js`](https://github.com/AlgoETS/Sport-Arbitrage/blob/main/script.js)
- [`arbitrage.ipynb`](https://github.com/AlgoETS/Sport-Arbitrage/blob/main/arbitrage.ipynb)

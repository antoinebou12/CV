# Sport-Arbitrage : calculatrice d’arbitrage pour paris sportifs

> Sport-Arbitrage est une calculatrice d’une page qui compare les cotes de deux sites de paris, repère un arbitrage et calcule mises et profit.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/sport-arbitrage/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/sport-arbitrage/index.md
- Publié: 2026-11-05
- Mis à jour: 2026-11-06
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/AlgoETS/Sport-Arbitrage
- Révision inspectée: dbee18848ac988cd6f99764c3148d5e3349035b2


## Cas d’utilisation

Calculatrice web qui vérifie les cotes de deux sites de paris pour repérer un arbitrage et répartir la mise.

- **Choisir 2 ou 3 issues** (Parieur): Le sélecteur Number of Odds d’index.html appelle toggleOddsFields() dans script.js, qui n’affiche les deux champs Draw que pour trois issues.
- **Saisir les cotes de deux sites** (Parieur): Le formulaire reçoit les cotes Win et Lost des sites 1 et 2, les cotes Draw facultatives et la mise totale.
- **Repérer un arbitrage** (Parieur): calculateArbitrage() teste des paires fixes entre les deux sites ; hasArbitrageOpportunity() signale un arbitrage quand la somme des inverses des cotes est inférieure à 1.
- **Répartir la mise** (Parieur): Pour chaque occasion, script.js affiche le pourcentage d’arbitrage, les mises optimales, le gain par issue et le profit garanti.
- **Vérifier le calcul en Python** (Parieur): arbitrage.ipynb reprend les mêmes fonctions en Python avec des cotes d’exemple codées en dur pour le cas à deux issues.

### Scénario : Tester les cotes d’exemple du carnet

1. Ouvrir index.html dans un navigateur et laisser Number of Odds à 2.
2. Saisir Win Site 1 = 1.3, Lost Site 1 = 3.93, Win Site 2 = 1.42 et Lost Site 2 = 2.9.
3. Entrer une mise totale (Total Investment) de 100 et cliquer sur Calculate.
4. Lire le résultat : seule la paire lost-site1 et win-site2 se qualifie, avec des mises d’environ 26,54 et 73,46.
5. Comparer avec la ligne de profit garanti (environ 4,31) et relancer arbitrage.ipynb pour vérifier les mêmes chiffres.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| JavaScript | 38.34 |
| Jupyter Notebook | 33.46 |
| HTML | 25.5 |
| CSS | 2.7 |



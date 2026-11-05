# nova-backtest : Des bougies historiques à la simulation

> nova-backtest est un fork archivé d’un framework de backtesting. Sa classe centrale choisit un client d’échange, charge une période historique et gère…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/nova-backtest/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/nova-backtest/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Dépôt: https://github.com/antoinebou12/nova-backtest
- Licence: MIT
- Révision inspectée: dda19e6e09bdd59dd483a964f2e47085d2a1bdef

## Résumé

nova-backtest est un fork archivé d’un framework de backtesting. Sa classe centrale choisit un client d’échange, charge une période historique et gère un capital simulé avec des contraintes de position.

**Pourquoi il existe:** Moteur de backtest financier communiquant avec les API d'exchanges crypto pour stratégies quantitatives.

**Cas d’usage:** Validation de stratégies algorithmiques sur données historiques.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Python | 99.74 |
| Dockerfile | 0.26 |

## Fonctions et composants

- **Entrées et clients** — BackTest reçoit l’échange, la stratégie, l’intervalle, les paires et les dates. La classe construit un client avec la factory clients et charge les hypothèses de frais depuis FEES.
- **État de simulation** — Le constructeur conserve le capital initial et courant, le levier, le nombre de positions et leur durée. Le dimensionnement géométrique est une option explicite. Les résultats dépendent de ces hypothèses autant que des signaux.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Historique de l’échange → Client et données
- Client et données → Signaux de stratégie
- Signaux de stratégie → Simulation positions et capital
- Simulation positions et capital → Sorties du backtest

```mermaid
flowchart LR
  n0["Historique de l’échange"]
  n1["Client et données"]
  n2["Signaux de stratégie"]
  n3["Simulation positions et capital"]
  n4["Sorties du backtest"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
```

**Un parcours dans le code:** Lisez le constructeur BackTest avant d’interpréter un graphique. Les frais, le levier et les tailles changent le capital simulé; modifier une hypothèse crée une autre expérience même avec les mêmes données.

## Limites et points à vérifier

Une simulation historique n’est ni une exécution réelle ni une preuve de rendement futur. Ce fork est archivé et les API d’échange doivent être retestées.

## Fichiers à lire

- [novalabs-backtest/utils/backtest.py](https://github.com/antoinebou12/nova-backtest/blob/Master/novalabs-backtest/utils/backtest.py)
- [novalabs-backtest/utils/constant.py](https://github.com/antoinebou12/nova-backtest/blob/Master/novalabs-backtest/utils/constant.py)
- [README.md](https://github.com/antoinebou12/nova-backtest/blob/Master/README.md)


---
title: "TradingViewBuilder : indicateurs et stratégies en Pine Script"
date: 2026-11-05T12:00:00-05:00
description: "TradingViewBuilder rassemble des indicateurs et stratégies Pine Script (EMA, MACD, RSI, Bollinger, RVI …) à coller dans TradingView."
translationKey: repository-note-tradingviewbuilder
repository_note: "TradingViewBuilder"
---

# TradingViewBuilder

<div class="repo-status-row"><span class="repo-badge kind">Scripts</span></div>

<div class="repo-tech-badges"><span class="tag tool">Pine Script</span><span class="tag tool">TradingView</span></div>

TradingViewBuilder est une collection d’indicateurs et de stratégies TradingView écrits en Pine Script, un fichier par technique. C’est un dépôt [AlgoÉTS](https://github.com/AlgoETS) pour les traders qui cherchent des points de départ lisibles pour des règles techniques courantes, à coller dans le Pine Editor, appliquer à un graphique et ajuster.

## Aperçu {#overview}

Les fichiers `.indicator` déclarent un `study()` (ou `indicator()`) qui se contente de tracer des valeurs. Les fichiers `.strategy` déclarent un `strategy()` qui place aussi des ordres `strategy.entry` selon des règles de croisement :

| Technique | Règle de la stratégie | Fichiers |
| :-- | :-- | :-- |
| Croisement EMA | Achat quand l’EMA 9 passe au-dessus de l’EMA 21, vente à découvert au croisement inverse | `ema.strategy`, `ema.indcator` |
| Croisement SMA | Achat quand la SMA 10 passe au-dessus de la SMA 20, fermeture au croisement inverse | `mac.strategy` |
| MACD | Achat ou vente quand le MACD (12, 26) croise sa ligne de signal sur 9 périodes | `macd.strategy`, `macd.indicator` |
| RSI | Achat quand le RSI 14 repasse au-dessus de 30, vente quand il passe sous 70 | `rsi.strategy`, `rsi.indicator` |
| Bandes de Bollinger | Achat quand la clôture repasse au-dessus de la bande basse (20, 2σ), vente sous la bande haute | `bollingerbands.strategy` |
| Régression linéaire | Même règle autour d’une régression linéaire sur 20 barres ± 2 écarts-types | `linearregression.strategy`, `linearregression.indicator` |
| Relative Vigor Index | Achat ou vente quand le RVI (10) croise sa ligne de signal sur 4 périodes | `rvi.strategy`, `rvi.indicator` |
| Écart-type | Bandes à la clôture ± l’écart-type sur 20 barres | `standarddeviation.strategy`, `standarddeviation.indicator` |

`TimeSeriesMomentumEffect.strategy` est un brouillon plus ambitieux : il liste 60 contrats à terme, mesure le rendement de chacun sur 12 × 21 barres, achète les gagnants, vend à découvert les perdants et dimensionne les positions avec une cible de volatilité et un plafond de levier.

## Démarrage {#installation}

Rien à installer. Les étapes du README :

1. Se connecter à TradingView et ouvrir l’onglet **Pine Editor** sous un graphique.
2. Copier le contenu d’un fichier `.indicator` ou `.strategy` du dépôt et le coller dans l’éditeur.
3. Cliquer sur **Add to Chart** (et sur **Save** pour conserver le script sous un nom).
4. Utiliser l’icône d’engrenage à côté du nom du script pour modifier périodes, sources, niveaux et couleurs.

## Guide du dépôt {#reader-guide}

- `*.indicator` (et `ema.indcator`) : versions d’affichage seul de l’EMA, de la régression linéaire, du MACD, du RSI, du RVI et de l’écart-type.
- `*.strategy` : versions de trading avec règles d’entrée pour l’EMA, le croisement de SMA (`mac`), le MACD, le RSI, les bandes de Bollinger, la régression linéaire, le RVI et l’écart-type.
- `TimeSeriesMomentumEffect.strategy` : brouillon de momentum multiactif en séries temporelles.
- `README.md` : liste des techniques et étapes de configuration dans TradingView.
- `docs/about.md` : page d’attente qui ne contient qu’un titre.

## Fonctionnalités {#features}

- huit techniques classiques, la plupart offertes en indicateur et en stratégie ;
- paramètres modifiables (`input()`) pour chaque période, multiplicateur et seuil ;
- tracés sur le graphique : bandes, moyennes mobiles, lignes de signal et niveaux de surachat et de survente ;
- une idée de momentum en séries temporelles rédigée avec ciblage de volatilité.

## Limites {#limits}

- La plupart des fichiers visent Pine Script v4. `mac.strategy` déclare `@version=5` mais utilise des appels v4, et `ema.indcator` déclare `@version=4` mais utilise des appels v5 (`indicator`, `input.int`, `ta.ema`) ; il faut corriger l’en-tête de version avant de les compiler.
- `standarddeviation.strategy` compare `close` à `close ± std` ; comme les bandes encadrent toujours la clôture, les conditions de croisement ne se déclenchent jamais et la stratégie ne place aucun ordre telle qu’écrite.
- `TimeSeriesMomentumEffect.strategy` emploie une syntaxe que Pine refuse (fonctions entre accolades, `length()` sur des tableaux) : c’est plutôt du pseudocode qu’un script exécutable.
- Le README parle de « Relative Volatility Index » pour le RVI, alors que le code calcule le Relative Vigor Index ; `mac.strategy` ne figure pas dans le README, et l’extension de `ema.indcator` contient une coquille.
- Les stratégies entrent en position puis s’inversent au signal opposé (seul `mac.strategy` ferme plutôt) ; il n’y a ni stop, ni dimensionnement, ni réglage de commission, et le dépôt ne contient aucun résultat de backtest.

## Sources {#sources}

- [Dépôt GitHub](https://github.com/AlgoETS/TradingViewBuilder)
- [README](https://github.com/AlgoETS/TradingViewBuilder/blob/main/README.md)
- [`macd.strategy`](https://github.com/AlgoETS/TradingViewBuilder/blob/main/macd.strategy)
- [`rsi.strategy`](https://github.com/AlgoETS/TradingViewBuilder/blob/main/rsi.strategy)
- [`bollingerbands.strategy`](https://github.com/AlgoETS/TradingViewBuilder/blob/main/bollingerbands.strategy)
- [`TimeSeriesMomentumEffect.strategy`](https://github.com/AlgoETS/TradingViewBuilder/blob/main/TimeSeriesMomentumEffect.strategy)

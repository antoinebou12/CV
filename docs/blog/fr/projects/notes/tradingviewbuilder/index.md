# TradingViewBuilder : indicateurs et stratégies en Pine Script

> TradingViewBuilder rassemble des indicateurs et stratégies Pine Script (EMA, MACD, RSI, Bollinger, RVI …) à coller dans TradingView.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/tradingviewbuilder/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/tradingviewbuilder/index.md
- Publié: 2026-11-05
- Mis à jour: 2026-11-05
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/AlgoETS/TradingViewBuilder


## Cas d’utilisation

Indicateurs et stratégies Pine Script (EMA, MACD, RSI, Bollinger, RVI …) à coller dans TradingView.

- **Afficher un indicateur** (Trader, TradingView): Coller un fichier .indicator comme rsi.indicator ou macd.indicator dans le Pine Editor et l’ajouter au graphique pour tracer la série et ses niveaux.
- **Tester un croisement** (Trader, TradingView): ema.strategy, mac.strategy et macd.strategy entrent sur un croisement rapide/lente ou MACD/signal et inversent ou ferment au croisement opposé.
- **Jouer les retours de bande** (Trader, TradingView): bollingerbands.strategy et linearregression.strategy achètent quand la clôture repasse au-dessus de la bande basse et vendent à découvert sous la bande haute.
- **Suivre un oscillateur** (Trader, TradingView): rsi.strategy réagit aux croisements du RSI avec 30 et 70, et rvi.strategy aux croisements du Relative Vigor Index avec sa ligne de signal.
- **Ajuster les paramètres** (Trader, TradingView): Chaque script déclare des input() (périodes, multiplicateurs, niveaux) que le README propose de modifier avec l’icône d’engrenage du graphique.
- **Esquisser un portefeuille** (Trader): TimeSeriesMomentumEffect.strategy esquisse un momentum sur 12 mois pour 60 contrats à terme, avec cible de volatilité et plafond de levier ; c’est un brouillon, pas du Pine valide.

### Scénario : Tester la stratégie RSI sur un graphique

1. Se connecter à TradingView, ouvrir un graphique et cliquer sur l’onglet Pine Editor.
2. Copier le contenu de rsi.strategy et le coller dans l’éditeur.
3. Cliquer sur Add to Chart : les entrées Long apparaissent quand le RSI(14) passe au-dessus de 30, les entrées Short quand il passe sous 70.
4. Ouvrir l’icône d’engrenage pour modifier RSI Length, Overbought Level ou Oversold Level et comparer les opérations.
5. Ajouter rsi.indicator dans un panneau séparé pour voir l’oscillateur avec les mêmes niveaux.



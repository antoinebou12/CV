# Ce que dit un guide salarial canadien quand on lit bien ses tableaux

> Relecture du texte du guide salarial 2023 conservé dans AlgoETS/Salary : 19 387 lignes, des tableaux financiers lus comme des niveaux d’expérience, et les salaires par famille d’emplois, province et ville.

- Page HTML: https://antoineboucher.info/CV/blog/fr/posts/salary-guide-2023-results/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/posts/salary-guide-2023-results/index.md
- Publié: 2026-11-05
- Mis à jour: 2026-11-05
- Tags: Python, AlgoETS, Data Analysis, Salaries
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)Le [projet Salary](https://antoineboucher.info/CV/blog/fr/projects/notes/salary/) partait d’une question simple : combien paie un même emploi d’une région canadienne à l’autre ? Il extrait des guides salariaux de firmes de recrutement à partir de PDF, les range dans des tableaux de données et les compare dans des carnets. Les carnets contiennent déjà des graphiques. Plusieurs sont faux, et les raisons valent plus que les graphiques eux-mêmes.

Cet article relit le guide 2023 à partir du texte que le dépôt a déjà extrait, corrige ce qui a mal tourné et présente ce que dit vraiment le guide.

## D’où viennent les chiffres

Le guide 2023 (le README cite Randstad) donne, pour chacune de 56 régions nommées, des tableaux d’emplois avec trois fourchettes de salaire. L’étape d’extraction du dépôt a laissé un texte complet dans `sandbox/output/output.txt`, une cellule par jeton, chacune marquée du niveau de titre d’où elle vient :

```text
<h1>calgary metropolitan region | <h3>business support & operations | <h5>entry | mid | senior |
<p>administrative assistant | 43.6 - 56.4 | 49.9 - 61.3 | 55.2 - 66.7 | ...
```

Ce marquage suffit pour reconstruire les tableaux : `<h1>` est la région, `<h3>` la famille d’emplois, `<h5>` les en-têtes de colonnes, `<p>` un emploi suivi de ses fourchettes, et un pied de page `<h2>` nomme la province au bas de chaque page. Les montants sont en milliers de dollars par an. Chaque chiffre ci-dessous est la médiane des milieux de fourchette : « 75.0 - 90.0 » compte pour 82,5.

## Trois erreurs d’extraction

**Tous les tableaux ne sont pas débutant / intermédiaire / senior.** Sur 19 387 lignes avec des fourchettes, 17 915 relèvent des trois niveaux d’expérience habituels. Les sections finance et RH sont différentes : 760 lignes ont quatre colonnes pour 1, 3, 5 et 10 ans d’expérience, et 677 lignes ont trois colonnes pour le chiffre d’affaires de l’entreprise, 10 M$, 100 M$ et 1 000 M$. Le script supposait trois niveaux d’expérience partout. Un chef de la direction financière d’une entreprise de 1 000 M$, à 594,1 k$ en haut de fourchette, est donc devenu un salaire « senior », et cette ligne domine le graphique des salaires maximums du carnet.

**Doublons et coquilles.** 3 607 lignes répètent un emploi, une région et une province déjà vus ; l’analyse garde la première occurrence. Trois lignes ont des fourchettes impossibles. La plus visible est une réceptionniste bilingue du comté de Simcoe dont la fourchette senior se lit « 63.1 - 713.0 », probablement 71,3 dans l’original. Dans les carnets, cette ligne est le salaire le plus élevé du Canada.

**Unités mélangées.** La famille soutien industriel (préparateurs de commandes, manœuvres, chauffeurs, concierges) est exprimée à l’heure : 97 % de ses milieux intermédiaires sont sous 30. Mêlés à des salaires annuels en milliers, ces taux tirent toutes les moyennes vers le bas et rendent absurdes les classements d’« écart régional ».

Le carnet de comparaison ajoute deux bogues de code. Les listes de minimums et de maximums 2024 prennent leur valeur senior dans le tableau 2023 (`df_sorted_2023`) : la valeur aberrante de 713 k$ apparaît donc les deux années. Et dans les données 2024, le maximum débutant a exactement la même moyenne (94,67) et le même écart-type que le maximum intermédiaire, ce qui indique une fourchette débutant construite avec les mauvais nombres. Le guide 2024 est en plus en français, celui de 2023 en anglais : impossible de relier les deux années par le titre d’emploi.

Une fois retirés les trois lignes cassées et les doublons, il reste 14 305 lignes emploi-région : 13 063 lignes annuelles couvrant 371 emplois dans 57 régions (York existe à la fois en Ontario et au Nouveau-Brunswick), et 1 242 lignes horaires.

## Ce que dit le guide

**Les niveaux avancent par pas fixes.** Le milieu médian vaut 66,2 k$ au niveau débutant, 75,9 k$ au niveau intermédiaire et 86,8 k$ au niveau senior. Pour l’emploi médian, le salaire senior vaut 1,30 fois le salaire débutant, et 80 % des lignes se situent entre 1,22 et 1,36. Mieux vaut connaître cette régularité avant d’interpréter la progression d’un emploi en particulier. Le soutien industriel, payé à l’heure, suit le même schéma : 19,8 $, puis 22,3 $, puis 24,9 $ de l’heure.

**La technologie paie le plus, nettement.**

![Diagramme en barres horizontales du salaire intermédiaire médian par famille d’emplois](https://antoineboucher.info/CV/blog/posts/salary-guide-2023-results/images/pay-by-job-family-fr.svg "Salaire intermédiaire médian par famille d’emplois, guide 2023.")

Les emplois technos ont un milieu intermédiaire médian de 97,2 k$, environ 15 k$ au-dessus de l’ingénierie (81,8 k$) et du marketing (81,7 k$). L’expérience client et le soutien administratif ferment la marche, tous deux à 54,8 k$.

**Le classement des provinces reflète surtout les emplois listés.**

![Diagramme en barres horizontales du salaire intermédiaire médian par province](https://antoineboucher.info/CV/blog/posts/salary-guide-2023-results/images/pay-by-province-fr.svg "Salaire intermédiaire médian par province, guide 2023.")

L’Alberta arrive en tête à 85,2 k$ et l’Île-du-Prince-Édouard en dernier à 70,3 k$, le Québec étant à 71,4 k$. Mais chaque région liste ses propres emplois, et le Québec compte à lui seul 16 régions, la plupart hors de Montréal. Une médiane provinciale compare des paniers, pas des salaires.

**Pour un même emploi, les grandes villes se tiennent.**

![Diagramme en barres groupées du salaire intermédiaire de sept emplois technos dans quatre métropoles](https://antoineboucher.info/CV/blog/posts/salary-guide-2023-results/images/tech-pay-by-city-fr.svg "Milieux intermédiaires de sept emplois technos dans quatre métropoles, guide 2023.")

Fixer l’emploi règle le problème du panier. Pour les développeurs et les architectes, Montréal, le Grand Toronto, le Grand Vancouver et Calgary sont à moins d’environ 10 % les uns des autres. Un développeur full stack intermédiaire est à 112,4 k$ à Montréal et à 120,2 k$ dans le Grand Toronto ; un architecte infonuagique à 127,7 k$ et 136,2 k$. Le poste DevOps (développement) est le mieux payé à Montréal, à 110,0 k$. C’est dans le soutien que les villes divergent : un analyste de centre d’assistance intermédiaire est à 61,6 k$ à Montréal contre 78,7 k$ dans le Grand Toronto, un écart de 22 %.

**Les directeurs mènent partout.** Parmi les emplois listés dans au moins 25 régions, les milieux médians les plus élevés sont directeur des opérations (190,4 k$), directeur du commerce électronique (159,7 k$), directeur de construction (153,6 k$), directeur de fabrication (153,3 k$) et directeur de l’approvisionnement (152,3 k$). Côté technologies, viennent en tête directeur des TI (151,8 k$), responsable technique (143,1 k$) et architecte d’applications (132,2 k$).

## Limites de cette lecture

- Ce sont les fourchettes d’une firme de recrutement, pas des salaires observés. Elles disent ce que la firme annonce, pas ce que les gens gagnent.
- Les médianes de milieux ignorent la largeur de chaque fourchette.
- Les provinces sont prises telles qu’imprimées en pied de page ; une région, Fort St. John, se trouve sur des pages marquées Alberta.
- Un emploi présent seulement au Québec, « head of workshop and assembly », a un milieu médian de 249 k$ sur ses 11 régions et est probablement mal extrait ; le classement « au moins 25 régions » l’écarte.
- Le guide 2024 n’est pas utilisé ici : ses fourchettes débutant ne sont pas fiables dans les données enregistrées et ses titres sont en français.

## Ce qu’il faudrait corriger dans le dépôt

Les correctifs sont petits. Garder l’en-tête `<h5>` avec chaque ligne et ne le traduire en débutant / intermédiaire / senior que lorsque l’en-tête le dit. Retirer les doublons exacts sur l’emploi, la région et la province. Signaler les fourchettes dont le haut est sous le bas ou à plus de trois fois celui-ci. Enregistrer une unité par famille d’emplois. Les graphiques du carnet de comparaison deviennent alors utiles, et une comparaison 2023-2024 demande une correspondance de titres entre les guides anglais et français.

La fiche du projet présente le code, l’installation et la liste complète des limites : [Salary : explorer les guides salariaux et les données de salaires au Canada](https://antoineboucher.info/CV/blog/fr/projects/notes/salary/).

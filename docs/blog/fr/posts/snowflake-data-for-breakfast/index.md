# Conférence Snowflake Data-for-Breakfast — notes

> Notes élargies — santé à l’échelle, fiscalité, clean rooms, keynote Infostrux, quand un entrepôt bat les feuilles.

- Page HTML: https://antoineboucher.info/CV/blog/fr/posts/snowflake-data-for-breakfast/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/posts/snowflake-data-for-breakfast/index.md
- Publié: 2022-09-06
- Mis à jour: 2026-05-22
- Tags: Conference, Snowflake, Data Analytics
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)**Snowflake Data-for-Breakfast** : matinée sur l’entrepôt cloud, le partage, la gouvernance et des histoires clients qui rendent l’architecture concrète. J’y suis allé pour l’exploitation réelle, pas les goodies. Keynote **Infostrux**.

## Pourquoi

Assez de SQL pour être dangereux, pas assez d’histoires de prod. Format petit-déjeuner = faible engagement, vocabulaire utile (**clean room**, **share**, politiques de lignes) avant midi.

## Matériel d’ouverture

![Supports — gouvernance et positionnement](./images/governed.jpeg)

Snowflake cadré comme **partage gouverné** d’abord, vitesse brute ensuite — pertinent quand la peur est « on ne peut pas exposer cette table ».

![Menu événement](./images/menu.jpeg)

### Santé mondiale

Client santé sur **trois continents** — partage partenaire sans sacrifier SLA.

| Leçon | Détail |
|-------|--------|
| **Réplication + gouvernance** | Conformité liée au partage live |
| **Budgets latence** | Pas seulement du batch nocturne |
| **Contrats de partage** | Juridique + objets techniques |

![Partage de données](./images/sharethrough.jpeg)

![Architecture multi-régions](./images/architecture.jpeg)

### Fiscalité à grande échelle

Gros volumes, questions ad hoc sans script fixe à l’avance.

![À propos](./images/aboutus.jpeg)

![Histoire client](./images/customer.jpeg)

Couche unique de consolidation = dépannage plus rapide, **lignée** expliquable aux auditeurs ; moins de CSV par courriel.

### Clean rooms

Due diligence : comparer des données qui se chevauchent sans tout fusionner.

![Sécurité et gouvernance](./images/security.jpeg)

Collaboration préservant la vie privée — pas qu’une case conformité.

## Tableau comparatif

| Pattern | Bon usage | Vigilance |
|---------|-----------|-----------|
| **Entrepôt central** | Dimensions partagées | Coût sans discipline requêtes |
| **Data sharing** | Partenaires live | Contrats + politiques |
| **Clean room** | Analyses sensibles | Temps de setup |
| **Montée compute** | Pics exploratoires | Entrepôts laissés allumés |

## Bilan

Vocabulaire plus clair même sans Snowflake au quotidien. Même saison que **[Run:ai sur AWS](https://antoineboucher.info/CV/blog/fr/posts/runai-aws-inference-webinar/)**.

## Articles liés

- [Bases vectorielles et films similaires](https://antoineboucher.info/CV/blog/fr/posts/vector-databases-similar-movies/)
- [Économie des LEGO et data science](https://antoineboucher.info/CV/blog/fr/posts/economics-lego-data-science/)

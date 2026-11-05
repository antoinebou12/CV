# Créer un portfolio avec Hugo (semaine 1)

> Semaine 1 portfolio Hugo — compromis HBTheme, embeds data, Substack, shortcode iframe, ce que je ferais autrement aujourd’hui.

- Page HTML: https://antoineboucher.info/CV/blog/fr/posts/portfolio-hugo-week-1/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/posts/portfolio-hugo-week-1/index.md
- Publié: 2024-01-06
- Mis à jour: 2026-05-22
- Tags: Hugo, Portfolio, Static Site, Substack
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)Semaine 1 de migration vers **Hugo** (janvier 2024) : thème, déploiement rapide, prouver que le dépôt peut porter plus qu’un PDF de CV. **HBTheme**, embed data, **Substack** à côté, shortcode **iframe**.

## Pourquoi Hugo sans CMS

| Choix | Raison |
|-------|--------|
| **Génération statique** | Hébergement peu coûteux, builds rapides |
| **Markdown** | Articles et projets versionnés dans git |
| **Modules** | Thème + partials sans tout copier |

Le **dépôt = source de vérité** : Markdown → HTML → GitHub Pages ou équivalent.

## HBTheme semaine 1

Commentaires, assets npm, modules Hugo — pas tout recoder.

Compromis :

- **Structure opinionated** — démarrage vite, friction plus tard pour des types de contenu custom
- **Pipeline assets** — étapes npm en CI mais SCSS/JS propres
- **Doc du thème** — plus utile que la doc Hugo en semaine 1

## Données dans la page

Test : intégrer l’étude des **vols de voitures à Montréal** (Substack d’un ami) — preuve que Hugo peut porter longform et graphiques, pas seulement des billets courts.

[Étude des vols de voitures à Montréal](https://mohamedilias.substack.com/p/etude-des-vols-de-voitures-a-montreal)

Leçon : **iframe ou lien** pour du contenu invité ; graphiques natifs plus tard avec page bundles.

## Substack en parallèle

Essais longs et audience newsletter. Hugo = shell pro ; Substack = format email/commentaires sans serveur mail maison.

## Shortcode iframe

```text

```

Exemple **FlashGames** :

À utiliser avec parcimonie (accessibilité, mobile, cookies tiers).

## Depuis la semaine 1

Site actuel : bilingue, notes de conférence, posts MCP. Journal complet : **[Refonte du site avec Hugo (partie 2)](https://antoineboucher.info/CV/blog/fr/posts/portfolio-hugo-website-refonte/)**. Aussi **[CV JSON Resume](https://antoineboucher.info/CV/blog/fr/posts/professional-resume-json-resume/)**.

## Articles liés

- [Refonte du site avec Hugo (partie 2)](https://antoineboucher.info/CV/blog/fr/posts/portfolio-hugo-website-refonte/) — Paper, modèle bilingue, boucle MCP
- [Parcours en génie logiciel](https://antoineboucher.info/CV/blog/fr/posts/software-engineering-journey/)
- [Prompts diagrammes ChatGPT et AIPRM](https://antoineboucher.info/CV/blog/fr/posts/chatgpt-airprm-sequence-diagrams/)

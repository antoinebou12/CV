---
image_alt: "Aperçu du site après premier déploiement"
post_kind: article
title: "Créer un portfolio avec Hugo (semaine 1)"
date: 2024-01-06T10:00:00-04:00
lastmod: 2026-11-05T12:00:00-05:00
description: "Semaine 1 d’un portfolio Hugo — ce que contenait l’ancien dépôt, une première page de liens Hugo, compromis HBTheme, intégration de données, Substack, shortcode iframe et ce que je ferais autrement aujourd’hui."
translationKey: portfolio-hugo-week-1
tags:
  - Hugo
  - Portfolio
  - Static Site
  - Substack
images:
  - images/featured.png
---

Semaine 1 de la migration de mon site vers **Hugo** (janvier 2024) : choisir un thème, livrer vite et prouver que le dépôt pouvait porter plus qu’un CV en PDF. Ce billet est le journal : d’où je partais, **HBTheme**, l’intégration d’une étude de données, **Substack** en parallèle et un shortcode **iframe** réutilisable.

<!--more-->

## Pourquoi Hugo et pas un CMS

| Choix | Raison |
|-------|--------|
| **Génération statique** | Hébergement peu coûteux, builds rapides, aucune base de données à corriger |
| **Source en Markdown** | Articles et projets versionnés dans git, avec des diffs relisibles |
| **Modules** | Récupérer thème et partials sans tout copier dans le dépôt |

En tant qu’ingénieur, je voulais le **dépôt comme source de vérité** : Markdown en entrée, HTML en sortie, déploiement sur GitHub Pages ou équivalent. Une interface d’administration à la WordPress, je l’aurais ignorée dès la deuxième semaine.

## D’où je partais

Avant la semaine 1, le dépôt de mon ancien site était un ensemble de pièces séparées, chacune avec sa propre chaîne d’outils :

| Pièce | Construction | Mise en ligne |
|-------|--------------|---------------|
| **CV web** | `resume.json` (JSON Resume) exporté avec `resume-cli` et le thème *elegant*, plus une variante sombre avec *kendall* | Le seul workflow GitHub Actions : à chaque push, `npm ci`, `npm run build`, copie de `index.html` dans `dist/`, publication avec `JamesIves/github-pages-deploy-action`. Un Dockerfile pouvait aussi le servir depuis `nginx:alpine` |
| **CV PDF** | LaTeX sur la classe Russell | PDF versionné à côté de la source, sans build en CI |
| **Articles de recherche** | Deux PDF dans un dossier | Fichiers statiques |
| **Page de liens** | Hugo, à partir du thème Lynx avec Tailwind CSS | Un Dockerfile qui lançait `hugo server`, sans build en CI |
| **Blogue** | Un sous-module git vers un thème Hugo tiers (blist) | Le contenu du blogue n’était plus dans le dépôt |

Le dernier commit, une semaine avant ce billet, supprimait l’ancien dossier du site. La semaine 1 est partie de ce terrain dégagé : quatre chaînes d’outils (npm, LaTeX, Hugo, Docker), et une seule déployait automatiquement.

## La première pièce Hugo : une page de liens

La page de liens a été mon premier vrai site Hugo, et elle explique beaucoup des choix faits ensuite.

**Mise en place du thème.** J’avais copié le thème Lynx dans le site au lieu de l’utiliser comme thème : `theme.toml`, `layouts/` et `assets/` étaient à la racine. L’échafaudage du thème a suivi : un `netlify.toml` et une configuration Lighthouse CI pointaient tous les deux vers un dossier `exampleSite` qui n’existait pas dans ma copie. C’est la raison principale de la ligne **Modules** du tableau plus haut : je voulais que le thème suivant soit importé, pas collé.

**Configuration.** Tout ce qui s’affichait venait de `config.toml` : `enableEmoji = true`, `disableKinds = ["taxonomy", "term"]` (pas de pages d’étiquettes pour un site d’une page) et un bloc `[module.hugoVersion]` avec `extended = false` et `min = "0.86.1"`. Les liens sont une liste de tables à une seule clé, et la clé sert deux fois :

```toml
[author]
  name = "Antoine Boucher"
  image = "profile.jpg"   # dans static/
  links = [
    { github = "https://github.com/<user>" },
    { linkedin = "https://linkedin.com/in/<user>" },
    { email = "mailto:<user>@example.com" },
  ]
```

Le gabarit d’accueil parcourt cette liste. La clé (`github`) choisit l’icône `assets/icons/github.svg` et le libellé `link.github` dans les fichiers i18n. Une valeur peut aussi être une table avec `href`, `icon`, `text`, `target` ou `title` pour remplacer les valeurs par défaut. L’avatar est redimensionné en 288×288 quand Hugo le trouve comme ressource.

**Du CSS sans Hugo extended.** Tailwind tourne depuis un script npm et écrit `assets/css/compiled/main.css`, qui est versionné. Hugo n’a qu’à regrouper des fichiers, donc le binaire standard (non extended) suffit. Le partial `head` enchaîne les étapes :

```go-html-template
{{ $bundleCSS := $assets.Get "css" | resources.Concat "css/main.bundle.css" | resources.Minify | resources.Fingerprint "sha512" }}
```

L’empreinte fournit aussi un attribut `integrity` sur la balise `<link>`. Un `assets/css/custom.css` facultatif est ajouté au paquet quand il existe.

**Structure du contenu et i18n.** Ni articles ni sections : une page d’accueil, un gabarit `single.html` avec un lien de retour et deux fichiers de traduction (`en.yaml`, `fr.yaml`) pour les libellés des liens, le lien « Home » et le pied de page (« Powered by » / « Propulsé par »). C’était mon premier fichier Hugo bilingue, bien avant les articles bilingues.

**Shortcodes.** Deux petits. `{{</* icon "github" */>}}` insère un SVG de `assets/icons/` dans le texte. `{{</* lead */>}}…{{</* /lead */>}}` met un paragraphe d’introduction en texte plus grand et atténué. Le shortcode d’icône se rabat sur la clé i18n `shortcode.icon_none` quand le SVG manque, mais aucun des deux fichiers de traduction ne définit cette clé : une faute de frappe dans un nom d’icône donnait un `<em>` vide. Détail, mais ça m’a appris à vérifier les clés i18n avant de faire confiance au repli d’un thème.

**Déploiement.** Le Dockerfile utilisait `klakegg/hugo:0.101.0` et lançait `server`, c’est-à-dire le serveur de développement de Hugo, pas un build statique. Le fichier Compose montait le projet dans `/app` alors que l’image avait copié le site dans un autre répertoire de travail : les modifications faites sur la machine n’atteignaient jamais le conteneur. Du HTML statique produit par `hugo --minify`, construit en CI comme le CV web, aurait été plus simple et plus rapide.

## HBTheme en semaine 1

**HBTheme** apportait les commentaires, des assets compatibles npm et les modules Hugo, ce qui m’évitait de reconstruire les gabarits de zéro.

Les compromis sont apparus tout de suite :

- **Structure imposée** : démarrage rapide, frictions plus tard quand on veut des types de contenu sur mesure
- **Chaîne d’assets** : les étapes npm ajoutent du temps de CI, mais gardent SCSS et JS propres
- **Profondeur de la doc** : en semaine 1, la doc du thème compte plus que celle de Hugo

Je choisirais encore un thème « tout compris » pour un site personnel ; je prévoirais du temps pour **retirer des modules** une fois que le site dépasse les réglages par défaut.

## Des données dans la page (pas seulement des billets)

Premier essai : intégrer une analyse des **vols de voitures à Montréal** (projet Substack d’un ami) dans des pages Hugo, pour prouver que la pile pouvait porter graphiques et textes longs, pas seulement des billets courts comme celui-ci.

[Étude des vols de voitures à Montréal](https://mohamedilias.substack.com/p/etude-des-vols-de-voitures-a-montreal)

Leçon : **iframe ou lien sortant**, ça suffit pour du contenu invité qu’on ne veut pas dupliquer ; les graphiques natifs dans Hugo viendraient plus tard avec les page bundles et les fichiers statiques.

## Substack en parallèle

**Substack** pour les essais longs et un public de type infolettre. Hugo pour la vitrine du portfolio et l’index des projets ; Substack quand un texte a besoin de commentaires ou d’envoi par courriel sans que je gère un serveur de courriel.

Ce partage tient toujours : Hugo, c’est la maison professionnelle de référence ; Substack, un canal facultatif pour les textes longs.

## Shortcode iframe

Les articles peuvent intégrer des pages HTTPS avec le shortcode `iframe` du site (`src` obligatoire ; `title`, `height`, `loading`, etc. facultatifs) :

```text
{{</* iframe src="https://example.com/" title="Exemple" height="480" */>}}
```

Exemple : l’ancienne démo **FlashGames**, toujours hébergée sur GitHub Pages :

{{< iframe src="https://antoinebou12.github.io/FlashGames/" title="FlashGames" height="420" referrerpolicy="no-referrer-when-downgrade" >}}

À utiliser avec parcimonie : accessibilité, hauteur sur mobile et règles sur les cookies tiers cassent plus souvent qu’un build Hugo.

**La raison en une ligne :** les vieilles démos (jeux de l’époque Flash) vivent encore sur GitHub Pages ; Hugo les enveloppe avec une URL stable et ma typographie, sans maintenir deux front-ends complets.

## Ce que je ferais autrement

En regardant ce dépôt avec ce que le site est devenu :

- **Importer les thèmes comme modules.** Un thème copié apporte son échafaudage de démo et transforme chaque correctif en amont en fusion manuelle.
- **Construire du HTML statique en CI pour chaque pièce.** Un seul workflow qui lance `hugo --minify` et l’export du CV, au lieu d’un serveur de développement dans un conteneur pour une pièce et d’un workflow pour une autre.
- **Garder les fichiers de traduction complets.** Chaque clé i18n appelée par un gabarit doit exister dans chaque langue, replis compris.
- **Ne versionner le CSS généré que s’il rapporte quelque chose.** Ici, oui : il permettait à Hugo standard de construire sans Node. Avec Hugo Pipes et une étape Node en CI, il devient du bruit dans les diffs.

## Depuis la semaine 1

Le site actuel a gagné des modules, des articles bilingues, des notes de conférence et des billets sur l’outillage de l’ère MCP. Journal complet : **[Refonte du site avec Hugo (partie 2)]({{< ref "/posts/portfolio-hugo-website-refonte/index.fr.md" >}})**. Voir aussi **[CV professionnel et JSON Resume]({{< ref "/posts/professional-resume-json-resume/index.fr.md" >}})** et l’index du blogue.

## Articles liés

- [Refonte du site avec Hugo (partie 2)]({{< ref "/posts/portfolio-hugo-website-refonte/index.fr.md" >}}) — Paper, modèle bilingue, boucle éditoriale MCP
- [Parcours en génie logiciel]({{< ref "/posts/software-engineering-journey/index.fr.md" >}}) — le contexte de carrière que le portfolio appuie
- [Prompts diagrammes ChatGPT et AIPRM]({{< ref "/posts/chatgpt-airprm-sequence-diagrams/index.fr.md" >}}) — des habitudes de documentation qui nourrissent le blogue

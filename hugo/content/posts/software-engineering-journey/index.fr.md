---
post_kind: article
title: "Mon parcours en génie logiciel"
date: 2023-12-30T10:00:00-04:00
lastmod: 2026-05-22T22:30:00-04:00
description: "Des jeux Flash et démos Unity à Algolux, aux projets à l’ÉTS, aux stages et au backend/plateforme/DevSecOps d’aujourd’hui — chronologie personnelle avec liens vers les projets."
translationKey: software-engineering-journey
tags:
  - Software Engineering
  - Career
  - Learning
  - Backend
  - DevSecOps
  - Platform Engineering
images:
  - featured.png
---

Je n’ai pas commencé dans Kubernetes. J’ai commencé dans des onglets de navigateur, des boucles de jeu et un makerspace qui sentait le PLA chaud. Cet article raconte ce chemin — **backend**, **plateforme** et **DevSecOps** sont où j’atterris, mais les étapes comptent. **[English version]({{< ref "/posts/software-engineering-journey/index.md" >}})**.

<!--more-->

## L’arc (en un coup d’œil)

Schéma du parcours ([`career-journey-flow.mmd`](./images/career-journey-flow.mmd), rendu avec [uml-mcp](https://github.com/antoinebou12/uml-mcp)) :

![Parcours — des jeux Flash et du makerspace au collège jusqu’au backend et à la plateforme aujourd’hui](./images/career-journey-flow.svg)

*Couleurs :* vert personnel · bleu école · violet club · gris coop · ardoise emploi temps plein · orange contrat · rose enseignement · ambre aujourd’hui.

## ~2010 — Jeux Flash et le web

Au secondaire, je faisais déjà de petits **jeux navigateur en Flash** et j’apprenais **HTML et JavaScript**. Le progrès, c’était quelque chose de cliquable : une boucle qui tourne, un score qui bouge, une page qui ne te ridiculise pas devant tes amis.

Cette habitude — livrer quelque chose de jouable, puis corriger ce qui gêne — n’a jamais vraiment disparu. Plus tard, j’ai emballé une partie de cette nostalgie dans [FlashGames](https://antoinebou12.github.io/FlashGames/) (Ruffle) et un conteneur {{< ref "/projects/retroarch-web-games" >}} pour les consoles classiques.

## ~2015 — Portfolio de jeux, moteurs plus lourds

Au cégep, je montais un **portfolio de projets jeu** et je refaisais des favoris dans **Unity**, **CryEngine** et **Unreal**. Même motivation, outils plus lourds : lumière, physique, assets qui prennent une semaine pour être « corrects ».

Ça m’a appris le **périmètre** : un jam et un projet de session n’ont pas la même barre — mais les deux méritent des vrais tests de jeu.

## ~2017 — Makerspace, voiture RC WiFi, le web pour de vrai

Au **Collégial International Sainte-Anne**, je gérais le **makerspace** : imprimantes 3D, VR, étudiants bloqués sur le câblage un vendredi à 16 h. J’ai aussi construit une **voiture télécommandée en WiFi** — le genre de projet où firmware, jeu mécanique et « pourquoi elle ne tourne qu’à gauche ? » partagent le même après-midi.

Cette année-là, je me suis vraiment orienté vers le **développement web** : moins « scène dans un moteur », plus « produit qu’on ouvre chaque semaine ».

## 2018 — Stage Algolux (imagerie computationnelle)

Mon **stage Algolux** : cinq semaines en photographie computationnelle — outils Python, analyse couleur RAW, flux de capture, piles Ansible pour valider l’ISP. J’ai encore l’affiche de recherche de cette période ; c’est le pont entre « j’aime le code » et « j’aime les systèmes qui touchent le monde physique ».

![Affiche de recherche — optimisation de la qualité d’image par l’IA, stage Algolux, Collégial Sainte-Anne](./images/algolux-research-poster.png)

Trace concrète sur le site : {{< ref "/projects/RawAnalyser" >}} (clipping et calibration RAW, lignée Algolux). Le labo, c’était tableurs, caméras et scripts — pas une page produit brillante — mais la même boucle qu’aujourd’hui : **mesurer, automatiser, documenter**.

## ÉTS — Hydroglisseur, AlgoÉTS, pile web

L’**École de technologie supérieure (ÉTS)** est l’endroit où les projets scolaires se sont empilés en parcours.

**Cheminement technologique (2017–2018)** — projet final **hydroglisseur** : jupe bleue, ventilateur de sustentation, pièces imprimées en 3D, bois, mousse et débogage tenace. Le genre de montage qui enseigne l’intégration avant les microservices.

![Prototype hydroglisseur à l’ÉTS — ventilateur, plateau en bois et jupe gonflable bleue dans l’atelier](./images/ets-hydroglisseur-prototype.png)

**Baccalauréat (2018–2023)** — cours et clubs. J’ai aidé à faire vivre **[AlgoÉTS](https://algoets.etsmtl.ca/)** (trading algorithmique) ; nous animions des ateliers comme **Python 101 — science des données** pour les membres qui voulaient passer de « j’utilise Python » à « je fais confiance à mon pandas ».

![AlgoÉTS Python 101 — atelier science des données sur l’écran d’une salle de classe](./images/algoets-python-101.png)

Ce club se relie à l’open source que je maintiens encore : la bibliothèque {{< ref "/projects/MarketWatch" >}} pour le jeu boursier sur MarketWatch. Même réflexe — **automatiser la partie ennuyeuse pour laisser les décisions aux humains**.

**Stages (2019–2022)** — Wandrian, Power Go, Intact : parseurs, API, tableaux de bord ELK, backend — les titres collaient enfin au travail quotidien.

**Temps plein (2023)** — [IONODES](https://ionodes.com/) : développeur infonuagique sur une plateforme IoT — paliers Auth0, Sentry, ONVIF/WebRTC, Azure DevOps.

**Maîtrise (2023–2026)** — ÉTS : **rendu en temps réel**, **physique interactive** et **usure de surface en temps réel**, avec frottement dynamique et textures — le fil qui rattache l’infographie au parcours.

## Années 2020 — Plateforme, sécurité, enseignement

Après le diplôme, les problèmes ont monté d’un cran :

- **GitLab CI/CD**, **GCP**, microservices Java, tests **Playwright** (recherche IMC2).
- Laboratoires **DevSecOps** à Polytechnique Montréal — gabarits GitLab pour ~20 équipes, Docker/Kubernetes, revues dans l’esprit OWASP.
- **Enseignement** à l’ÉTS : bases distribuées, mobile/UX, projets intégrateurs — le matériel de cours, c’est aussi de la livraison logicielle.
- Site {{< ref "/posts/graphquon-2024-ets" >}} ([graphquon.github.io](https://graphquon.github.io/)) et **[uml-mcp](https://github.com/antoinebou12/uml-mcp)** pour les diagrammes depuis le chat — parce qu’expliquer un système bat encore le deviner.

## Ce qui n’a pas changé

Au début, je mesurais le progrès en **features livrées**. Aujourd’hui, je regarde si le système reste compréhensible quand on n’est plus dans la pièce :

- **Backend** — frontières, modes de panne, API qui ne surprennent pas l’équipe suivante.
- **Plateforme** — CI, logs, dev local sans README héroïque.
- **DevSecOps** — secrets, dépendances, chemins de déploiement volontairement ennuyeux.

La fiabilité, c’est la confiance. La sécurité n’est pas une barrière de fin de sprint — ce sont des habitudes dans le pipeline. J’écris encore des billets et des schémas parce qu’expliquer mal, c’est souvent la première façon de voir ce qu’on ne comprend pas.

## Ce que j’optimise ensuite

Des plateformes plus claires, une livraison plus sûre, des systèmes lisibles en grandissant. Si vous débutez : suivez les problèmes où vous voyez **toute la boucle** — code, déploiement, exploitation, amélioration. Moi, j’ai commencé avec Flash et un hydroglisseur ; vous commencerez peut-être ailleurs. La boucle, c’est le métier.

D’autres notes concrètes sont sous [articles]({{< ref "/posts" >}}) et [projets]({{< ref "/projects" >}}) — dont {{< ref "/posts/rhino-lidar-apartment-scan" >}} et {{< ref "/posts/professional-resume-json-resume" >}} pour des chapitres plus récents.

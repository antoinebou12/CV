---
post_kind: article
title: "Mon parcours en génie logiciel"
date: 2023-12-30T10:00:00-04:00
description: "Réflexions sur la croissance comme ingénieur logiciel — systèmes backend, plateforme et DevSecOps : ce qui reste et ce que j’optimise aujourd’hui."
translationKey: software-engineering-journey
tags:
    - Software engineering
    - Career
    - Learning
    - Backend
    - DevSecOps
    - Platform engineering
---

La bio de ce site résume la facette du métier qui m’intéresse le plus : **backend**, **plateforme** et **DevSecOps**. Cet article prolonge ce regard — pas une chronologie d’emplois, mais les idées qui reviennent quand on cesse de ne mesurer que « les features livrées ».

## Des features aux systèmes

Au début, le progrès semble linéaire : tickets fermés, endpoints ajoutés, écrans livrés. Ce travail compte. Avec le temps, les problèmes intéressants se situent un cran au-dessus : comment les services communiquent, comment les pannes se propagent, comment un changement dans le dépôt d’une équipe affecte tout le monde le lundi matin. Le backend cesse d’être « écrire le handler » et devient « concevoir quelque chose qui reste compréhensible quand vous n’êtes plus dans la pièce ».

La pensée **plateforme** prolonge ça vers l’extérieur. Si vous avez déjà mis en place de la CI, standardisé les logs ou facilité le démarrage local pour un·e collègue, vous avez déjà fait du travail plateforme. L’objectif est de **réduire la taxe** sur le quotidien : moins de runbooks ad hoc, moins de fils « ça marche chez moi », plus de chemins reproductibles de l’idée à la prod.

## Fiabilité et ownership

La fiabilité, ce n’est pas seulement des graphiques de disponibilité. C’est aussi la confiance des équipes pour aller vite. Cette confiance vient d’un **ownership** clair (qui répare quoi quand ça casse), d’un comportement **observable** (métriques, traces, logs qui répondent à de vraies questions) et de changements assez petits pour être raisonnés.

J’ai appris à traiter incidents et quasi-incidents comme **retour de conception**. Les post-mortems aident, mais le gain durable, c’est d’intégrer ces leçons dans les défauts : meilleures alertes, déploiements plus sûrs, frontières plus nettes entre composants. L’ownership, c’est faire cette boucle même sans ticket assigné.

## La sécurité dans la livraison

Pour moi, le DevSecOps n’est pas une barrière en fin de sprint. C’est **décaler la vigilance vers l’amont** de façon réaliste pour les équipes : hygiène des dépendances, gestion des secrets, moindre privilège, menace modélisée en assez peu de temps pour tenir dans une planification normale. Une sécurité qui ne vit que dans la tête d’un·e spécialiste ne scale pas ; des habitudes dans les pipelines et les conventions, si.

Le même état d’esprit vaut pour les services tiers et le cloud. Si vous ne pouvez pas expliquer ce qui expose quoi, vous n’avez pas encore une histoire déployable — vous avez un pari avec une belle étiquette.

## Apprentissage et outils

Les outils changent sans cesse. Les cadres, les API cloud et les flux assistés par IA continueront d’évoluer. Ce qui **compose**, c’est le jugement : quand adopter, quand encapsuler, quand refuser. Je lis encore la doc, casse des choses en bac à sable et emprunte des idées à l’open source et aux retours d’autres devs (y compris les brouillons — c’est souvent là qu’on lit les vraies contraintes).

J’accorde aussi de la valeur à l’écrit — billets courts, schémas, notes internes — parce qu’expliquer mal est souvent la première étape vers une bonne compréhension.

## Ce que j’optimise ensuite

À suivre, les mêmes thèmes avec des arêtes plus nettes : **plateformes plus claires**, **livraison plus sûre**, **systèmes qui restent lisibles** en grandissant. Si vous débutez, mon conseil (biaisé) est de viser des problèmes où vous voyez toute la boucle : code, déploiement, exploitation, amélioration. C’est là que backend, plateforme et DevSecOps cessent d’être des buzzwords et deviennent le métier.

Merci de lire — si ça parle à quelqu’un, vous trouverez des notes plus concrètes ailleurs sur le site sous articles et projets.

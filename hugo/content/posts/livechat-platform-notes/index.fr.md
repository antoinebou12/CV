---
post_kind: article
title: "Plateformes de chat en direct et de support (3CX, ManyChat, Kommunicate, Chatwoot)"
date: 2022-09-06T10:00:00-04:00
lastmod: 2026-05-22T22:45:00-04:00
description: "Notes pour choisir chat web, bot et boîte d’équipe — différences entre 3CX, ManyChat, Kommunicate et Chatwoot, avec visuels et liens."
translationKey: livechat-platform-notes
tags:
  - Live Chat
  - Chatbot
  - Customer Support
  - Open Source
  - 3CX
  - Chatwoot
images:
  - featured.png
---

![Boîte de réception Chatwoot — vue unifiée des conversations (capture du projet open source, interface 2024)](./images/chatwoot-inbox.png)

J’ai rédigé ces notes en aidant une équipe de boutique bilingue à choisir un **chat en direct**, un **bot** et un outil que les agents pourraient vraiment utiliser. Les quatre produits ci-dessous ne sont **pas** interchangeables : l’un est une téléphonie avec du chat, l’un fait de l’automatisation marketing, l’un gère le passage bot → humain en SaaS, et le dernier est un helpdesk open source auto-hébergeable. **Tarifs et canaux changent souvent** — servez-vous de ce texte comme carte, puis validez chez chaque éditeur. **[English version]({{< ref "/posts/livechat-platform-notes/index.md" >}})**.

<!--more-->

## Commencer par le besoin, pas par le logo

Avant la matrice de fonctionnalités, clarifiez ce que vous achetez vraiment :

- **Une seule file pour la voix et le chat web** → pile téléphonie.
- **Campagnes et croissance sur Instagram/Facebook** → marketing conversationnel.
- **Le bot ouvre, l’humain finit** → SaaS CX géré.
- **Boîte partagée sur votre propre infra** → desk open source.

Schéma de décision ([`platform-picker-flow.mmd`](./images/platform-picker-flow.mmd), rendu avec [uml-mcp](https://github.com/antoinebou12/uml-mcp)) :

![Quelle plateforme de chat selon votre objectif — arbre de décision 3CX, ManyChat, Kommunicate, Chatwoot](./images/platform-picker-flow.svg)

| | | |
|:---:|:---:|:---:|
| ![Logo 3CX](./images/logo-3cx.svg) | **ManyChat** · [manychat.com](https://manychat.com) | **Kommunicate** · [kommunicate.io](https://www.kommunicate.io) |
| | ![Logo Chatwoot](./images/logo-chatwoot-brand.svg) | |

## 3CX — la téléphonie d’abord, le chat dans la même file

![Logo 3CX — communications d’entreprise et PBX](./images/logo-3cx.svg)

[3CX](https://www.3cx.com), c’est d’abord de l’**UCaaS / PBX** : postes, réunions, routage d’appels. Le **chat web** et les widgets **Talk** vivent dans cet écosystème. Si la voix passe déjà par 3CX, ajouter le chat peut donner **un fournisseur, un poste agent, un ensemble de files** au lieu d’empiler une inbox séparée.

C’était l’intérêt quand j’ai configuré **Live Chat and Talk** sur un site CommerceBuild : ventes et support restaient dans une pile déjà payée, avec un **chatbot 3CX** pour les questions simples. Le revers : vous achetez une **plateforme de communications**, pas un helpdesk neutre. Profondeur de ticketing, flexibilité CRM et scénarios « seulement courriel + chat SaaS » passent au second plan.

**Mise en place :** pour WordPress et autres plugins CMS, suivez la [documentation 3CX](https://www.3cx.com/docs/) **à jour** — les libellés d’assistant et les noms d’intégration bougent entre versions. J’avais des **notes FR** pour le plugin Live Chat and Talk d’après un ancien guide ; à **recouper avec la doc officielle** avant la prod.

**Connexe (hors 3CX) :** scénarios **Microsoft** bots + analytique : [YouTube — Microsoft ChatBot (Power BI)](https://www.youtube.com/watch?v=nWxguR5B5-s).

## ManyChat — campagnes et Meta, pas un helpdesk

[ManyChat](https://manychat.com) sert au **marketing conversationnel** : diffusions, séquences, capture de leads, surtout sur **Meta** (Instagram, Facebook). On l’utilise pour faire grandir et automatiser les DM, pas pour un desk support sobre avec SLA sur courriel, téléphone et web au même endroit.

**Adapté :** croissance, entonnoirs, scripts support orientés réseaux sociaux.  
**Moins adapté :** « une inbox open-core pour web + courriel + téléphone avec ticketing poussé ».

Voir la [tarification ManyChat](https://manychat.com/pricing) (sièges, contacts) avant de bâtir des flux dessus.

## Kommunicate — bot d’abord, humain quand ça compte

[Kommunicate](https://www.kommunicate.io) vise la **collaboration humain + bot** : le bot prend le premier tour, puis **transfère** vers des agents sur le site et les canaux de messagerie courants. Vous intégrez un **SaaS géré** — pas de week-end Kubernetes obligatoire.

Utile pour du câblage **type Dialogflow** et une interface agent soignée sans exploiter la pile. Comparez **coût total**, **résidence des données** et **dépendance aux modèles** (plusieurs fournisseurs LLM annoncés) à l’auto-hébergement si la conformité compte.

## Chatwoot — inbox partagée, cloud ou Docker maison

![Logo Chatwoot — engagement client open source](./images/logo-chatwoot-brand.svg)

[Chatwoot](https://www.chatwoot.com) est une suite **AGPL**. **Chatwoot Cloud** ou **auto-hébergement** (Docker, guides opérateur dans la doc développeur).

C’est plutôt **« boîte partagée + fils omnicanaux »**, proche d’Intercom/Zendesk qu’un PBX ou un bot marketing pur :

- **Inbox unifiée** pour widget web, courriel et autres canaux (liste exacte évolutive — voir leur doc).
- **Équipes, étiquettes, automatisations** et historique pour support et suivi commercial.
- **API et webhooks** quand l’UI par défaut ne suffit plus.

![Liste inbox Chatwoot — thème clair, rafraîchissement UI 2024 (capture via GitHub Chatwoot)](./images/chatwoot-inbox.png)

**Compromis :** l’auto-hébergement donne la maîtrise et peut réduire le coût par siège, mais vous assumez **sauvegardes, mises à jour et sécurité**. Voix et certaines intégrations CRM enterprise peuvent arriver après les grandes suites propriétaires — vérifiez vos must-have sur leur feuille de route.

- [Chatwoot sur GitHub](https://github.com/chatwoot/chatwoot)
- [Documentation développeur Chatwoot](https://developers.chatwoot.com)

## Comparaison rapide

| | Cœur de métier | Déploiement typique | Open source |
|---|----------------|---------------------|-------------|
| **3CX** | Téléphonie + UC + chat web dans une même pile | PBX cloud ou sur site + agents | Non |
| **ManyChat** | Automatisation marketing, souvent Meta d’abord | SaaS | Non |
| **Kommunicate** | Transfert bot → humain, CX géré | SaaS | Non |
| **Chatwoot** | Inbox omnicanale, orientée support | SaaS (cloud) ou auto-hébergé | Oui (AGPL) |

## Liens à vérifier avant d’acheter

- [Documentation 3CX](https://www.3cx.com/docs/)
- [Tarification ManyChat](https://manychat.com/pricing)
- [Kommunicate](https://www.kommunicate.io)
- [Chatwoot](https://www.chatwoot.com) · [GitHub](https://github.com/chatwoot/chatwoot) · [Documentation développeur](https://developers.chatwoot.com)
- [Microsoft ChatBot + Power BI (YouTube)](https://www.youtube.com/watch?v=nWxguR5B5-s)

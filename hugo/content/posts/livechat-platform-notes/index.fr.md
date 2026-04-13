---
post_kind: article
title: "Plateformes de chat en direct et de support (3CX, ManyChat, Kommunicate, Chatwoot)"
date: 2022-09-06T10:00:00-04:00
description: En quoi 3CX, ManyChat, Kommunicate et Chatwoot diffèrent pour le chat web, les bots et les boîtes de réception d’équipe—avec liens et tableau comparatif.
translationKey: livechat-platform-notes
tags:
    - Chat en direct
    - Chatbot
    - 3CX
    - Support client
    - Chatwoot
    - ManyChat
    - Kommunicate
    - Open source
---

Ces notes viennent d’une comparaison pour le **chat en direct sur site web**, les **chatbots** et une **boîte de réception partagée** pour le support. Les produits ci-dessous ne sont pas interchangeables : certains sont des piles de communications complètes, d’autres de l’automatisation marketing, et l’un est une solution open source de type helpdesk. **Les tarifs, canaux et fonctionnalités évoluent souvent**—utilisez ce texte comme repère, puis vérifiez sur le site de chaque éditeur.

## 3CX

[3CX](https://www.3cx.com) est surtout une offre **UCaaS / PBX** (téléphonie, réunions, postes). Le **chat web en direct** et les widgets associés s’inscrivent dans ce même écosystème, ce qui est pertinent si vous routez déjà la voix et le chat via 3CX et voulez un seul fournisseur pour les files et les agents.

Pour **Live Chat and Talk** (y compris les extensions CMS comme WordPress), suivez la procédure **à jour** dans la documentation officielle plutôt qu’une liste figée—les libellés et noms d’intégration changent entre versions. Point de départ : [documentation 3CX](https://www.3cx.com/docs/).

**Notes (FR)** : j’avais rédigé un guide de configuration pour le plugin Live Chat and Talk ; il doit être **recoupé** avec la doc officielle ci-dessus avant toute mise en production.

### Connexe : analytique et bots (pas spécifique à 3CX)

Lien tangentiel au chat web, utile si vous explorez des scénarios **Microsoft** mêlant bots et analytique :

- [YouTube — Microsoft ChatBot (Power BI)](https://www.youtube.com/watch?v=nWxguR5B5-s)

## ManyChat

[ManyChat](https://manychat.com) sert surtout au **marketing conversationnel et à l’automatisation**, avec une orientation forte vers **Meta** (Instagram/Facebook) : diffusions, séquences et capture de leads.

**Adapté** aux campagnes et entonnoirs sur les réseaux sociaux ; **moins** comme helpdesk multicanal neutre avec ticketing poussé et SLA sur e-mail, chat et téléphonie dans un même produit open-core.

- [Tarification ManyChat](https://manychat.com/pricing)

## Kommunicate

[Kommunicate](https://www.kommunicate.io) vise la **collaboration humain + bot** : le bot ouvre la conversation, puis **transfère** vers des agents sur le site et les canaux de messagerie courants. C’est du **SaaS géré**—vous intégrez et configurez plutôt que d’exploiter la pile vous-même.

Utile si vous voulez un **bot type plateforme NLU** et une interface agent sans self-hosting ; comparez le coût total et la résidence des données aux options auto-hébergées si c’est un critère pour votre organisation.

## Chatwoot

[Chatwoot](https://www.chatwoot.com) est une suite **open source** d’engagement client (licence **AGPL**). Vous pouvez utiliser **Chatwoot Cloud** ou **l’auto-héberger** (Docker et autres chemins documentés pour les opérations).

**Conceptuellement**, c’est plutôt « boîte de réception partagée + conversations omnicanales » qu’un PBX ou un bot marketing pur :

- **Inbox unifiée** pour widget web, courriel et autres canaux (la liste exacte évolue—voir leur documentation).
- **Équipes, étiquettes, automatisations** et historique orientés support et suivi commercial.
- **API et webhooks** pour intégrations et flux sur mesure.

**Compromis** : l’auto-hébergement donne la maîtrise et peut réduire le coût par siège, mais vous assumez **sauvegardes, mises à jour et sécurité**. La profondeur fonctionnelle par rapport aux grandes suites propriétaires dépend du canal ; vérifiez vos besoins (voix, CRM précis, etc.) sur leur feuille de route et leurs docs.

**Liens** :

- [Chatwoot sur GitHub](https://github.com/chatwoot/chatwoot)
- [Chatwoot](https://www.chatwoot.com) (aperçu produit)
- [Documentation développeur Chatwoot](https://developers.chatwoot.com) (API, installation, auto-hébergement)

## Comparaison rapide

| | Cœur de métier | Déploiement typique | Open source |
|---|----------------|---------------------|-------------|
| **3CX** | Téléphonie + UC + chat web dans une même pile | PBX cloud ou sur site + agents | Non |
| **ManyChat** | Automatisation marketing, souvent Meta d’abord | SaaS | Non |
| **Kommunicate** | Transfert bot → humain, CX géré | SaaS | Non |
| **Chatwoot** | Inbox omnicanale, orientée support | SaaS (cloud) ou auto-hébergé | Oui (AGPL) |

## Ressources

- [Documentation 3CX](https://www.3cx.com/docs/)
- [Tarification ManyChat](https://manychat.com/pricing)
- [Kommunicate](https://www.kommunicate.io)
- [Chatwoot](https://www.chatwoot.com)
- [Chatwoot — GitHub](https://github.com/chatwoot/chatwoot)
- [Chatwoot — documentation développeur](https://developers.chatwoot.com)
- [YouTube — Microsoft ChatBot (Power BI)](https://www.youtube.com/watch?v=nWxguR5B5-s)

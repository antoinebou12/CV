---
post_kind: article
title: "GPT-4 vs GPT-3.5 — capacités et cadre des coûts API"
date: 2023-04-10T10:00:00-04:00
description: Notes sur les cas d’usage GPT-4 et GPT-3.5-turbo, leurs forces, et une façon de raisonner sur les coûts d’API de chatbot à l’échelle.
translationKey: gpt4-api-costs-overview
tags:
    - AI
    - GPT-4
    - GPT-3.5
    - ChatGPT
    - OpenAI
    - NLP
    - API
---

![Image de couverture de l’article](https://media.licdn.com/dms/image/D5612AQHKus7rY_HvVQ/article-cover_image-shrink_720_1280/0/1681059889367?e=1709769600&v=beta&t=39LUP6caikwBW_QeEC7T-2peoci56x6v9xzNtCPdWxQ "Cover Image for AI Article")

Alors que l’intelligence artificielle progresse, de plus en plus d’entreprises intègrent des chatbots à leur service client. Ces chatbots couvrent un large spectre de demandes, des questions simples aux sujets plus complexes. Le coût de mise en œuvre et de maintenance reste un facteur important. Dans cet article, on estime les coûts d’utilisation des modèles **GPT-4** et **GPT-3.5-turbo** avec un plafond de **25 messages toutes les 3 heures** sur un mois, en supposant des tailles de prompt moyennes comparables (**50 à 200 jetons**).

## API OpenAI

L’API OpenAI sert à de nombreuses tâches de traitement du langage naturel (NLP), par exemple :

- **Traduction** de texte d’une langue à une autre.
- **Génération de texte** à partir d’un prompt (titres, résumés, articles).
- **Résumé** de documents longs en versions plus courtes.
- **Chatbots** pour le service client, assistants virtuels, etc.
- **Questions-réponses** avec précision et fluidité (disponible sur les moteurs GPT-3).
- **Compréhension** du sens du texte (feedback clients, sentiment, etc.).
- **Complétion** de texte (formulaires, e-mails, etc.).
- **Classification** (spam, sentiment, etc.).

## Comparaison des modèles

### GPT-4

GPT-4 apporte des capacités de raisonnement avancées et une culture générale plus large, avec une précision supérieure aux générations précédentes. Il se distingue notamment sur la créativité, les entrées visuelles et les **contextes longs** (plus de 25 000 mots de texte). Certaines de ces fonctionnalités étaient encore sur liste d’attente au moment de l’article.

Sur des benchmarks, GPT-4 se situe plus haut que ChatGPT sur des épreuves type barreau ou olympiade de biologie.

Les travaux sur **sécurité et alignement** incluent l’apprentissage avec retour humain, l’amélioration continue via l’usage réel et la recherche sur la sécurité assistée par GPT-4.

Plusieurs organisations ont collaboré avec OpenAI pour des produits sur GPT-4 (Duolingo, Be My Eyes, Stripe, Morgan Stanley, Khan Academy, gouvernement d’Islande, etc.).

Malgré ses capacités, GPT-4 conserve des limites connues : biais sociaux, hallucinations, prompts adverses. OpenAI s’engage à les traiter tout en poussant transparence et littératie IA. GPT-4 est disponible dans ChatGPT Plus et en API pour les développeurs.

### GPT-3.5-turbo

C’est le moteur utilisé dans la démo ChatGPT **sans** ChatGPT Plus.

- Rédiger un e-mail ou un texte
- Écrire du code Python
- Répondre à des questions sur un corpus de documents
- Créer des agents conversationnels
- Donner une interface langage naturel à un logiciel
- Tutorat dans plusieurs matières
- Traduire des langues
- Simuler des personnages de jeu vidéo, etc.

Le choix entre GPT-4 et GPT-3.5-turbo dépend de la **qualité**, de la **latence** et du **budget** : GPT-4 est plus fort sur le raisonnement difficile et les longs contextes ; GPT-3.5-turbo reste le cheval de bataille pour beaucoup de scénarios chat et outillage. Pour modéliser les coûts, combinez jetons par tour, trafic et limites de débit — surtout si vous plafonnez les messages par utilisateur et par heure.

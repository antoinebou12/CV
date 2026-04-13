---
post_kind: article
title: "Plugin ChatGPT avec FastAPI — plan d’implémentation"
date: 2024-06-01T10:00:00-04:00
description: Liste de contrôle pour un plugin ChatGPT minimal — service FastAPI, schéma OpenAPI, auth et hébergement.
translationKey: fastapi-chatgpt-plugin-overview
tags:
    - ChatGPT
    - OpenAI
    - FastAPI
    - Python
    - Plugins
    - OpenAPI
    - Tutorial
---

Les **plugins** de style OpenAI exposent une API HTTP décrite par un document **OpenAPI** pour que ChatGPT puisse appeler vos outils de façon contrôlée. **FastAPI** génère OpenAPI automatiquement, ce qui colle bien à ce modèle.

## 1. Définir l’API dans FastAPI

- Les routes renvoient du **JSON** avec des formes stables (éviter le texte libre ambigu quand la structure compte).
- Ajoutez **résumés et descriptions** sur les chemins et les champs — ça aide le modèle à choisir le bon outil.

## 2. Publier `openapi.json`

- FastAPI sert **`/openapi.json`** par défaut ; le manifeste du plugin pointe vers cette URL (ou une copie statique versionnée).
- Gardez les schémas **stricts** : énumérations, champs obligatoires et exemples réduisent les mauvais appels.

## 3. Manifeste du plugin

- Hébergez **`ai-plugin.json`** (ou le format exigé par la doc développeur OpenAI actuelle) en **HTTPS**.
- Le manifeste référence l’URL de base de l’API et l’emplacement d’OpenAPI.

## 4. Authentification

- Préférez **OAuth** ou **clés API** comme documenté pour votre intégration ; ne commitez jamais de secrets.
- Validez les jetons dans les dépendances ou le middleware FastAPI.

## 5. Déploiement

- Point de terminaison **HTTPS** joignable depuis les serveurs OpenAI.
- Journalisation et **idempotence** pour les routes à effets de bord.

## 6. Tests manuels

- Appelez les routes avec `curl` ou HTTPie en utilisant les mêmes charges que le modèle enverra.
- Itérez sur les descriptions et contraintes avant d’ouvrir le trafic.

> Les détails évoluent avec les mises à jour de la plateforme OpenAI — suivez toujours la doc la plus récente sur **plugins / tools / actions** pour la prod.

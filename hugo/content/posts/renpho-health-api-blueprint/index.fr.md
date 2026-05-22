---
post_kind: article
title: "Balance Renpho, Home Assistant et rétro-ingénierie de l’API"
date: 2021-10-10T10:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "Fork hass-renpho, APKLeaks sur l’app Android, tableaux Lovelace, habitudes honnêtes pour les métriques bio-impédance."
translationKey: renpho-health-api-blueprint
tags:
  - Health
  - API
  - Reverse Engineering
  - Home Assistant
  - Home Automation
images:
  - featured.jpeg
---

Je voulais les pesées dans **Home Assistant** avec le reste des automations — pas une app santé de plus. Résultat : fork **hass-renpho**, **APKLeaks** sur le client Android, tableau Lovelace que je consulte encore. **[English version]({{< ref "/posts/renpho-health-api-blueprint/index.md" >}})**.

<!--more-->

## Point de départ

Balance **Renpho** bio-impédance = plus que le poids. Esprit **[lab maison]({{< ref "/posts/home-networking-evolution/index.fr.md" >}})** : si les données comptent, elles atterrissent là où vivent alertes et graphiques.

![Inspiration suivi personnel](./images/blueprint.jpg)

Pas d’endorsement d’un protocole célébrité — photo = « je voulais des tendances ».

## Fork hass-renpho

`hass-renpho` intègre Renpho dans HA ; projet silencieux → **fork** pour étendre les métriques.

- Install **HACS**, identifiants
- **Entités** poids + composition
- **Issues** quand l’API bouge

Échanges avec le mainteneur quand possible.

![Tableau de bord Home Assistant](./images/health-dashboard-metrics.jpeg)

## APKLeaks

Pas de doc API publique — lire l’**app Android**.

```bash
pip install apkleaks
apkleaks -f renpho.apk
```

Aligner endpoints et champs JSON (poids, BMI, BMR, graisse, muscle, eau, etc.) → **entités** HA.

- [APKLeaks GitHub](https://github.com/dwisiswant0/apkleaks)
- [White Oak Security](https://www.whiteoaksecurity.com/blog/apkleaks-discover-leaks-within-apk-files/)

Contrat **instable** à chaque mise à jour app.

## Tableau et habitudes

Renpho = une entrée ; **Google Health** / **MyFitnessPal** pour activité et repas.

![Lovelace — métriques détaillées](./images/detailed-metrics-integration.jpeg)

| Habitude | Pourquoi |
|----------|----------|
| **Même heure** | Matin, hydratation stable |
| **Vêtements constants** | ~1 kg de bruit |
| **Tendances** | La composition estimée lag la réalité |

## Quand s’abstenir

- Besoin **médical** — ce n’est pas l’outil.
- Obsession sur le % graisse du jour — masquer les jauges inutiles.
- Pas de maintenance de fork — attendez-vous à des casses.

## Articles liés

- [Évolution réseau maison]({{< ref "/posts/home-networking-evolution/index.fr.md" >}})
- [Économie LEGO data science]({{< ref "/posts/economics-lego-data-science/index.fr.md" >}})

Vous self-hostez quoi côté santé : HA, Grafana, téléphone seulement ?

---
post_kind: article
title: "Renpho scale, Home Assistant, and reverse-engineering the API"
date: 2021-10-10T10:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "Forking hass-renpho, APKLeaks on the Android app, Lovelace dashboards, and honest habits for bio-impedance numbers at home."
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

I wanted scale readings in **Home Assistant** next to the rest of my apartment automations — not another siloed health app. That turned into forking **hass-renpho**, running **APKLeaks** on the Android client, and building a Lovelace board I still glance at. **[Version française]({{< ref "/posts/renpho-health-api-blueprint/index.fr.md" >}})**.

<!--more-->

## Starting point

A **Renpho** scale with bio-impedance exports more than weight — body fat estimates, water, muscle, the usual contested numbers. I already ran a **[home lab]({{< ref "/posts/home-networking-evolution/index.md" >}})** mindset: if data matters, it should land where dashboards and alerts already live.

![Blueprint-style self-tracking inspiration — the push to quantify](./images/blueprint.jpg)

I am not endorsing any celebrity protocol; the photo is shorthand for “I wanted trends, not a single morning panic number.”

## Forking hass-renpho

`hass-renpho` pulls Renpho data into Home Assistant. The project had gone quiet; with the maintainer unavailable I **forked** to extend metrics the hardware already exposes.

That meant:

- **HACS install** and credential config
- **Entity mapping** for weight + composition fields
- **Issues upstream** when API shapes drifted

Talking with the original maintainer when possible — share payloads, suggest fixes, avoid duplicate forks doing the same patch.

![Home Assistant dashboard — weight history, gauges, composition rows](./images/health-dashboard-metrics.jpeg)

## Reverse engineering with APKLeaks

No official public API doc — so read what the **Android app** calls.

**APKLeaks** scans the APK for strings (URLs, keys, hints) without a full decompile session:

```bash
pip install apkleaks
git clone https://github.com/dwisiswant0/apkleaks
cd apkleaks && pip install -r requirements.txt
apkleaks -f renpho.apk
```

I lined endpoints up with JSON fields I cared about: weight, BMI, BMR, body age, fat/muscle estimates, water, protein, visceral fat indices. In HA they become **entities** → Lovelace gauges and history cards.

Further reading:

- [APKLeaks on GitHub](https://github.com/dwisiswant0/apkleaks)
- [White Oak Security — APKLeaks overview](https://www.whiteoaksecurity.com/blog/apkleaks-discover-leaks-within-apk-files/)

Treat leaked strings as **unstable contract** — app updates break integrations.

## Dashboard and measurement habits

Renpho is one input. I still use **Google Health** / **MyFitnessPal** for activity and food so scale readings sit beside movement and calories.

![Lovelace — extra metrics and supporting integrations](./images/detailed-metrics-integration.jpeg)

Habits that kept the series usable:

| Habit | Why |
|-------|-----|
| **Same time of day** | Mornings, similar hydration |
| **Clothing constant** | ~1 kg swing is normal noise |
| **Trends over weeks** | Composition estimates lag reality |

## When not to do this

- You need **medical-grade** body composition — this is not it.
- You will obsess over daily fat % — hide gauges you do not act on.
- You cannot maintain a fork when the app updates — expect breakage.

## Related posts

- [Home networking evolution]({{< ref "/posts/home-networking-evolution/index.md" >}}) — same “own your infra” thread
- [Economics of LEGO with data science]({{< ref "/posts/economics-lego-data-science/index.md" >}}) — another dataset curiosity project

If you self-host health data, I am curious what stuck: HA, Grafana, or phone-only apps?

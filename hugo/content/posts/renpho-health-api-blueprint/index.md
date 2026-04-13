---
post_kind: article
title: "Renpho scale, Home Assistant, and reverse-engineering the API"
date: 2021-10-10T10:00:00-04:00
lastmod: 2026-04-13T12:00:00-04:00
description: Forking hass-renpho, surfacing Renpho API endpoints with APKLeaks, and wiring bio-impedance metrics into a Home Assistant Lovelace health dashboard.
translationKey: renpho-health-api-blueprint
tags:
    - Health
    - Renpho
    - API
    - Reverse engineering
    - Home Assistant
    - HACS
    - Fitness
    - Home automation
images:
    - featured.jpeg
---

## Inspiration from Bryan Johnson’s "Blueprint Protocol"

Personal health tracking, for me, started with Bryan Johnson’s "Blueprint Protocol"—a push for self-quantification that matched how I already thought about fitness. I wanted the same granularity for my own body, and a Renpho scale with bio-impedance turned out to be a practical way to get a steady stream of numbers beyond simple weight.

![Blueprint Protocol Inspiration](images/blueprint.jpg)

## Forking hass-renpho and the Home Assistant ecosystem

I found `hass-renpho`, a custom integration that pulls Renpho scale data into Home Assistant. The project had gone quiet, and with the original maintainer unavailable I forked it to extend support for more of the metrics the hardware exposes.

That fork dragged me through the normal Home Assistant custom-component path: installing via HACS, configuring credentials, and iterating on entities. Along the way I talked with the original maintainer where it made sense—suggesting fixes, sharing what I was seeing in the API, and trying to keep the integration useful for anyone else running a Renpho at home.

![Home Assistant dashboard showing Renpho vitals, weight history, and body-composition gauges](images/health-dashboard-metrics.jpeg)

## Reverse engineering and APKLeaks

The mobile app does not publish an official API document, so the next step was to learn what the Android client actually calls. **APKLeaks** scans the packaged APK for strings—URLs, keys, and other clues—rather than fully decompiling the app into readable source. Running it on the Renpho APK surfaced the HTTP endpoints and enough context to line those calls up with the JSON payloads I cared about (weight, BMI, BMR, body age, fat and muscle estimates, water, protein, visceral-fat indices, and the rest of the bio-impedance-derived fields). In Home Assistant those show up as entities and feed Lovelace cards—gauges for composition, history graphs for weight, and simple entity rows for the “extra” metrics.

```shell
# Simple PyPi installation
pip3 install apkleaks
# Delving into the source
git clone https://github.com/dwisiswant0/apkleaks
cd apkleaks/
pip3 install -r requirements.txt
```

Further reading:

- [APKLeaks on GitHub](https://github.com/dwisiswant0/apkleaks)
- [APKLeaks in-depth analysis](https://www.whiteoaksecurity.com/blog/apkleaks-discover-leaks-within-apk-files/)

## Dashboard, context, and measurement habits

Renpho data is only part of the picture. I still use tools like Google Health and MyFitnessPal for activity and food so the scale readings sit next to diet and movement, not in a vacuum.

![Lovelace layout with additional composition metrics and supporting integrations](images/detailed-metrics-integration.jpeg)

Day-to-day swings taught me to treat the numbers as trends, not verdicts. Clothing alone can move the needle by about a kilogram on a bad day; hydration and digestion matter too. Measuring at a consistent time (for me, mornings, similar conditions) keeps the series usable when I look at the history card in HA.

This started as a technical side project and became a steady habit: the dashboard is a single place to see weight trajectory, composition estimates, and the supporting stats the integration exposes—enough to decide whether training or sleep changes are showing up where I expect.

## Community and what works for you

None of this would be as practical without the Home Assistant and open-source integration ecosystem—forks, issues, and small patches add up. If you are quantifying your own health, I am curious what actually stuck for you: dedicated hardware, phone-only apps, or something self-hosted like this? Share what you use and what you ignore; the useful part is rarely the gadget alone, but how consistently the data fits your routine.

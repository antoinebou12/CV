---
post_kind: article
title: "Renpho scale, Home Assistant, and reverse-engineering the API"
date: 2021-10-10T10:00:00-04:00
lastmod: 2026-05-22T23:00:00-04:00
description: "Forking hass_renpho for Home Assistant — old Renpho app API, APKLeaks, Lovelace dashboards, proxy quirks, and habits that keep bio-impedance useful."
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

I wanted scale readings in **Home Assistant** next to the rest of my apartment automations — not another siloed health app. That turned into maintaining **[hass_renpho](https://github.com/antoinebou12/hass_renpho)** (a fork of the quiet community integration), running **APKLeaks** on the Android client, and a Lovelace board I still open when training or sleep changes. **[Version française]({{< ref "/posts/renpho-health-api-blueprint/index.fr.md" >}})**.

<!--more-->

## Why not only the Renpho app

A **Renpho** scale with bio-impedance spits out more than weight — BMI, BMR, body age, fat and muscle estimates, water, protein, visceral-fat indices, and a pile of resistance fields per limb if you pull the full payload. Useful only if the numbers live where you already look: history graphs, automations, and the same **[homelab]({{< ref "/posts/home-networking-evolution/index.md" >}})** mindset as everything else self-hosted at home.

## Inspiration (without the cult)

Personal tracking, for me, started around the same time people were talking about Bryan Johnson’s **“Blueprint”** push for self-quantification. I am not selling a protocol — the point was simpler: **trends over time**, same conditions, don’t panic on one morning spike. The photo below is mood board energy, not medical advice.

![Self-quantification mood board — inspiration for tracking habits, not a product endorsement](./images/blueprint.jpg)

## Where hass_renpho came from

Neil Allen’s write-ups — [reverse-engineering the Renpho app](https://neilgaryallen.dev/blog/reverse-engineering-the-renpho-app) and [Renpho → Home Assistant](https://neilgaryallen.dev/blog/renpho-to-home-assistant) — did the hard thinking first. The community repo **[neilzilla/hass-renpho](https://github.com/neilzilla/hass-renpho)** wrapped that into a Home Assistant custom component.

When activity slowed and I needed more entities exposed, I forked to **[antoinebou12/hass_renpho](https://github.com/antoinebou12/hass_renpho)**. The README is honest about constraints:

> This integration targets the **older Renpho app** cloud API. Newer app versions may not work; treat it as a hobby integration, not a supported product.

There is a small **API explorer** at [hass-renpho.vercel.app/docs](https://hass-renpho.vercel.app/docs) if you want to poke the JSON with your own credentials before touching HA.

### What the fork actually does

- Logs into Renpho’s cloud (`renpho.qnclouds.com`) with email/password (same as the phone app).
- Polls on a **`refresh`** interval you set in YAML or the UI.
- Exposes **sensors** for weight, composition, metabolic estimates, device metadata, and optional girth/goals when the account has them.
- Optional **`proxy`** URL when your home IP is throttled or blocked but the app works on cellular data.

I kept talking with the original maintainer when it made sense — share payload shapes, avoid duplicate fixes, keep one integration useful for anyone else with a scale in the closet.

## Install path I used

1. **[HACS](https://hacs.xyz/)** on Home Assistant (or copy `custom_components/renpho` from the repo).
2. Drop credentials in **`configuration.yaml`** (legacy platform style in my fork):

```yaml
renpho:
  email: you@example.com
  password: !secret renpho_password
  refresh: 600  # seconds between polls — logging in here can log you out of the app
  # proxy: http://127.0.0.1:8080  # optional — only this integration’s traffic

sensor:
  - platform: renpho
```

3. Restart HA, confirm entities appear, then build Lovelace.

**Heads-up:** polling logs you into the cloud API; Renpho may kick your phone session. I picked a **600s** refresh so I was not hammering login on every automation tick.

## Metrics the integration surfaces

The fork documents dozens of fields. In practice I watch a smaller set in Lovelace; the rest are there if you automate or debug.

| Group | Examples | Units |
|-------|----------|-------|
| **Core** | weight, BMI, body fat, water, muscle, bone | kg, % |
| **Shape** | waistline, hip, stature | cm |
| **Metabolic** | BMR, protein | kcal/day, % |
| **Age** | body age | years |
| **Visceral / subcutaneous** | visfat, subfat | level, % |
| **Device** | scale name, MAC, model, timezone | strings |
| **Bio-impedance raw** | resistance per limb (20 kHz / 100 kHz style fields) | ohms |

Full tables live in the **[repo README](https://github.com/antoinebou12/hass_renpho#supported-metrics)** — handy when APKLeaks shows a new key and you need a matching sensor.

## When the cloud API fights your network

Residential or datacenter egress sometimes fails against Renpho’s cloud even when the official app works on LTE. Symptoms: auth errors, empty lists, random HTTP failures in HA logs.

Mitigations from the README:

1. **VPN on the HA host** — change egress IP for everything on that machine.
2. **`proxy` in config** — only Renpho traffic goes through your HTTP/SOCKS proxy (credentials pass through that path — use something you trust).

I document this because it burned an evening that looked like “broken integration” but was really **IP reputation**.

## Reverse engineering with APKLeaks

Renpho does not ship a public API PDF. Next step: see what the **Android APK** calls.

**[APKLeaks](https://github.com/dwisiswant0/apkleaks)** scans the package for strings — hosts, paths, keys — without a full decompile session:

```bash
pip install apkleaks
git clone https://github.com/dwisiswant0/apkleaks
cd apkleaks && pip install -r requirements.txt
apkleaks -f /path/to/renpho.apk -o renpho-leaks.txt
```

I matched leaked URLs and parameter names to the JSON fields the integration already mapped, then filled gaps when Lovelace showed `unknown` for a new key after an app update.

Further reading:

- [APKLeaks on GitHub](https://github.com/dwisiswant0/apkleaks)
- [White Oak Security — APKLeaks overview](https://www.whiteoaksecurity.com/blog/apkleaks-discover-leaks-within-apk-files/)

Treat anything you extract as an **unstable contract** — store updates break custom integrations; that is the hobby tax.

## Lovelace dashboards

Two views I actually use: vitals + history, then girth/goals when Renpho syncs them.

![Home Assistant Lovelace — Renpho weight history, body-composition gauges, and supporting entity rows](./images/lovelace-metrics.png)

Weight trend at the top, composition gauges in the middle, “extra” metrics as entities you can hide if they noise you out.

![Home Assistant Lovelace — Renpho girth measurements and body goals from the cloud account](./images/lovelace-girth.png)

Girth and goals only matter if your Renpho profile has them; otherwise this panel stays empty and that is fine.

## Context outside HA

Renpho is one input. I still mirror activity and food elsewhere (**Google Health**, **MyFitnessPal**) so scale readings sit next to movement and calories, not alone in a vacuum.

### Habits that kept the series usable

| Habit | Why |
|-------|-----|
| **Same time of day** | Mornings, similar hydration — otherwise you are comparing apples to soup |
| **Clothing constant** | ~1 kg swing is normal noise, not “fat overnight” |
| **Trends over weeks** | Bio-impedance composition lags reality; react to slopes |
| **Hide gauges you ignore** | If you do not act on visceral fat %, remove the card |

This started as a technical side project and became a steady habit: enough signal to notice when training or sleep changes show up in weight and energy, not enough precision for clinic decisions.

## When not to do this

- You need **clinical** body composition — consumer scales estimate, they do not diagnose.
- You cannot run the **legacy app/API** path the integration expects.
- You will not maintain a fork when Renpho changes the app — budget breakage.
- Daily fat % will ruin your mood — curate the dashboard ruthlessly.

## Repo links (quick)

| Resource | URL |
|----------|-----|
| My fork | [github.com/antoinebou12/hass_renpho](https://github.com/antoinebou12/hass_renpho) |
| Upstream lineage | [github.com/neilzilla/hass-renpho](https://github.com/neilzilla/hass-renpho) |
| API docs / playground | [hass-renpho.vercel.app/docs](https://hass-renpho.vercel.app/docs) |
| Original RE blog | [neilgaryallen.dev — Renpho series](https://neilgaryallen.dev/blog/reverse-engineering-the-renpho-app) |

## Related posts

- [Home networking evolution]({{< ref "/posts/home-networking-evolution/index.md" >}}) — same “own your infra” thread
- [MediaBox homelab notes]({{< ref "/posts/mediabox-homelab-docker-catalog/index.md" >}}) — another self-hosted stack at home
- [Economics of LEGO with data science]({{< ref "/posts/economics-lego-data-science/index.md" >}}) — another dataset curiosity project

If you self-host health data, what actually stuck — Home Assistant, Grafana, or phone-only apps? The gadget is rarely the hard part; fitting the routine is.

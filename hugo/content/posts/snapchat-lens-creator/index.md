---
post_kind: article
title: "Snapchat Lens Creator"
date: 2022-09-06T10:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "Snapchat lenses with millions of plays (2017–2020), Fiverr clients, a GIF-to-PNG tool, Lens Studio feedback, and what I would do on Meta Spark next."
translationKey: snapchat-lens-creator
tags:
  - Snapchat
  - Lens Studio
  - AR
  - Side Project
---

*Updated May 2026 with current Lens Insights figures.* I started making **Snapchat lenses** for fun in **2017** and ended up with a small **Fiverr** side business, a utility other creators still use, and a phone call with Snapchat about **Lens Studio**. **[Version française]({{< ref "/posts/snapchat-lens-creator/index.fr.md" >}})**.

<!--more-->

## By the numbers (Lens Insights)

To date, my lenses have accumulated **13.97M plays**, **20.38M views**, **711.8k shares**, **10,092 favorites**, **753 posts**, and **428 unique posters** (all-time, Lens Insights). Plays and views are not the same metric — a lens can be opened once but watched multiple times — so I look at both when a client asks “did it work?”

Between **2017 and 2020** I shipped **42 lenses** for myself and for clients. Standouts by usage:

| Lens | Rough plays |
|------|-------------|
| **Go Crazy Facetime** | ~2.9M |
| **Face Ghosting** | ~1.2M |
| **BIG SMILE** | ~520k |

Snapchat’s audience tools also frame the ecosystem: a reported **~596M–623M** potential audience for lens users, with strong reach in **India** and the **United States**, and device mix roughly **Android (~70%)** vs **iOS (~30%)**. That split matters when you test only on your own phone.

## How I got started

Lens Studio was approachable before ARKit jargon was everywhere: face tracking, simple materials, publish to Snapchat. My first lenses were jokes for friends — face swaps, exaggerated expressions — then I noticed the **metrics tab** and started treating each release like a tiny product launch (thumbnail, preview video, one clear hook).

## Fiverr workflow

Paid work followed the same pipeline:

1. **Brief** — reference video or competitor lens, target vibe, deadline.
2. **Prototype** — greybox in Lens Studio, send screen recording before polish.
3. **Review cycles** — Snapchat review plus client taste (often stricter than Snapchat).
4. **Delivery** — publish under their account or mine, depending on contract.

I kept a short **reject checklist** per lens: licensed audio, readable thumbnail at phone size, effect triggers on the intended face region, and a 10-second preview that shows the hook without explanation. That list saved more client arguments than any shader tweak.

Pricing stayed modest; the learning was **scope control** and **revision limits**. The worst projects were “make it viral” with no creative direction.

## When review said no

Not every submission cleared **Snapchat review** or **client approval**. Common fails: copyrighted audio, unclear lens purpose, performance on low-end Android, or effects that trigger on the wrong face region. Each rejection became a checklist item for the next build — I kept a short notes file per lens.

## GIF / video → PNG sequences

Lens Studio wants image sequences for many effects. I wrote a small utility to turn **GIF or video into PNG sequences** for pipeline work; other Lens Studio creators picked it up too.

[GIF/Video to PNG for Lens Studio](https://lnkd.in/gN-DFZX7)

That tool saved more time than any single visual trick — batch export beats screenshotting frames by hand.

## Lens Studio product feedback

Snapchat called by phone to collect **Lens Studio** feedback from active creators. I shared friction I hit daily: project load times, preview fidelity vs phone, documentation gaps for shader-adjacent features. It felt good to be heard even when not every note shipped.

## Meta Spark next

I want to go deeper on **Meta Spark** for cross-platform AR. Official hub: [Spark AR / Meta Spark learn](https://spark.meta.com/spark-ar/learn/). If you have tutorials that map cleanly from a Lens Studio mental model, I am collecting recommendations.

## Takeaway

AR lenses were my first experience shipping creative work to **millions of anonymous users** with real analytics — closer to product than to portfolio art. The skills transfer elsewhere: tight loops, device testing, graceful failure when platforms change rules.

## Related posts

- [Diagram prompts with ChatGPT and AIPRM]({{< ref "/posts/chatgpt-airprm-sequence-diagrams/index.md" >}}) — another “tooling for makers” thread
- [Skate rack — from CAD to plywood]({{< ref "/posts/skate-rack-cad-to-object/index.md" >}}) — physical maker projects

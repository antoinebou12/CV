---
post_kind: article
title: "My journey in software engineering"
date: 2023-12-30T10:00:00-04:00
description: Reflections on growing as a software engineer across backend systems, platform work, and DevSecOps — what stuck and what I optimize for now.
translationKey: software-engineering-journey
tags:
    - Software Engineering
    - Career
    - Learning
    - Backend
    - DevSecOps
    - Platform Engineering
---

This site’s bio sums up the slice of the field I care about most: **backend**, **platform**, and **DevSecOps**. This post is a longer look at how I think about that journey — not a timeline of jobs, but the ideas that kept showing up once I stopped treating “shipping features” as the only scoreboard.

## From features to systems

Early on, progress often feels linear: tickets closed, endpoints added, screens shipped. That work matters. Over time, though, the interesting problems sit one level up: how services talk to each other, how failures propagate, how a change in one team’s repo affects everyone else on Monday morning. Backend engineering stops being “write the handler” and becomes “design something that stays understandable when you’re not in the room.”

Platform thinking extends that outward. If you have ever set up CI, standardized logging, or made it easier for another developer to run the stack locally, you have already done platform work. The goal is to **lower the tax** on everyday work: fewer one-off runbooks, fewer “works on my machine” threads, more repeatable paths from idea to production.

## Reliability and ownership

Reliability is not only uptime graphs. It is also whether teammates trust the system enough to move fast. That trust comes from clear ownership (who fixes what when it breaks), observable behavior (metrics, traces, logs that answer real questions), and changes that are small enough to reason about.

I have learned to treat incidents and near-misses as **design feedback**. Postmortems are useful, but the deeper win is folding those lessons into defaults: better alerts, safer deploys, clearer boundaries between components. Ownership means carrying that loop even when no one assigned a ticket for it.

## Security as part of delivery

DevSecOps, for me, is not a separate gate at the end of a sprint. It is **shifting concern left** in ways that fit real teams: dependency hygiene, secret handling, least-privilege access, and threat modeling that is short enough to happen in a normal planning conversation. Security work that only lives in a specialist’s head does not scale; security habits that live in pipelines and conventions do.

The same mindset applies to third-party services and cloud resources. If you cannot explain what exposes what, you do not yet have a deployable story — you have a gamble with good branding.

## Learning and tools

Tools change constantly. Frameworks, cloud APIs, and AI-assisted workflows will keep evolving. What compounds is **judgment**: knowing when to adopt something, when to wrap it, and when to say no. I still read docs, break things in sandboxes, and borrow ideas from open source and from other engineers’ write-ups (including the messier ones — those often contain the constraints that matter).

I also value writing — short posts, diagrams, internal notes — because explaining something badly is often the first step toward understanding it well.

## What I optimize for next

Going forward, I care about the same themes with sharper edges: **clearer platforms**, **safer delivery**, and **systems that stay legible** as they grow. If you are early in your career, my biased advice is to chase problems where you can see the whole loop: code, deploy, operate, improve. That loop is where backend, platform, and DevSecOps stop being buzzwords and become the job.

Thanks for reading — if any of this resonates, you will find more concrete notes elsewhere on this site under posts and projects.

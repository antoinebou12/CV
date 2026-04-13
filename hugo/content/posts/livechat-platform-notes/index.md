---
post_kind: article
title: "Live chat and support platforms compared (3CX, ManyChat, Kommunicate, Chatwoot)"
date: 2022-09-06T10:00:00-04:00
description: How 3CX, ManyChat, Kommunicate, and Chatwoot differ for website chat, bots, and team inboxes—plus links and a compact comparison table.
translationKey: livechat-platform-notes
tags:
    - Live chat
    - Chatbot
    - 3CX
    - Customer support
    - Chatwoot
    - ManyChat
    - Kommunicate
    - Open source
---

These notes come from comparing options for **website live chat**, **chatbots**, and a **shared support inbox**. The products below are not interchangeable: some are full communications stacks, others are marketing automation, and one is an open-source helpdesk. **Pricing, channels, and features change often**—treat this as orientation, then confirm on each vendor’s site.

## 3CX

[3CX](https://www.3cx.com) is primarily **UCaaS / PBX** (phones, meetings, extensions). Its **web live chat** and related widgets sit in that same ecosystem, which helps if you already route voice and chat through 3CX and want one vendor for queues and agents.

For **Live Chat and Talk** (including CMS plugins such as WordPress), follow the **current** steps in the official docs rather than a static checklist—wizard text and integration names move between releases. Start from the [3CX documentation](https://www.3cx.com/docs/).

I also kept **separate notes in French** for configuring the Live Chat and Talk plugin; those mirror whatever the official guide said at the time and should be validated against the docs above.

### Related: analytics and bots (not 3CX-specific)

This is only tangential to website live chat, but useful if you are exploring **Microsoft-side** bot patterns with analytics:

- [YouTube — Microsoft ChatBot (Power BI)](https://www.youtube.com/watch?v=nWxguR5B5-s)

## ManyChat

[ManyChat](https://manychat.com) is built for **conversational marketing and automation**, with a strong tilt toward **Meta** (Instagram/Facebook) and growth workflows: broadcasts, sequences, and lead capture.

**Good fit** when the goal is campaigns and funnel automation on social, less so when you need a **neutral, multi-channel helpdesk** with deep ticketing and SLAs across email, chat, and phone in one open-core product.

- [ManyChat pricing](https://manychat.com/pricing)

## Kommunicate

[Kommunicate](https://www.kommunicate.io) targets **human + bot collaboration**: bot handles the first turn, then **hands off** to agents on the website and common messaging channels. It is a **managed SaaS**—you integrate and configure rather than operating the stack yourself.

Useful when you want **dialogflow-style bot wiring** and a polished agent desk without self-hosting; compare total cost and data residency to self-hosted options if that matters for your org.

## Chatwoot

[Chatwoot](https://www.chatwoot.com) is an **open-source** customer engagement suite (license: **AGPL**). You can use **Chatwoot Cloud** or **self-host** (Docker and other paths are documented for operators).

**Conceptually**, it is closer to “shared inbox + omnichannel conversations” than to a PBX or a pure marketing bot:

- **Unified inbox** for web widget, email, and other channels (exact channel set evolves—see their docs).
- **Teams, labels, automation**, and conversation history aimed at support and sales follow-up.
- **APIs and webhooks** for integrations and custom workflows.

**Trade-offs**: self-hosting gives control and can reduce per-seat SaaS cost, but you own **backups, upgrades, and security**. Feature depth versus large proprietary suites varies by channel; verify what you need (e.g. voice, specific CRMs) against their roadmap and docs.

**Links**:

- [Chatwoot on GitHub](https://github.com/chatwoot/chatwoot)
- [Chatwoot](https://www.chatwoot.com) (product overview)
- [Chatwoot developer documentation](https://developers.chatwoot.com) (API, setup, and self-hosting guides)

## Quick comparison

| | Primary focus | Typical deployment | Open source |
|---|----------------|-------------------|-------------|
| **3CX** | Telephony + UC + web chat in one stack | Cloud or on-prem PBX + agents | No |
| **ManyChat** | Marketing automation, often Meta-first | SaaS | No |
| **Kommunicate** | Bot + human handoff, managed CX | SaaS | No |
| **Chatwoot** | Omnichannel inbox, support-oriented | SaaS (cloud) or self-hosted | Yes (AGPL) |

## Resources

- [3CX documentation](https://www.3cx.com/docs/)
- [ManyChat pricing](https://manychat.com/pricing)
- [Kommunicate](https://www.kommunicate.io)
- [Chatwoot](https://www.chatwoot.com)
- [Chatwoot — GitHub](https://github.com/chatwoot/chatwoot)
- [Chatwoot — developer docs](https://developers.chatwoot.com)
- [YouTube — Microsoft ChatBot (Power BI)](https://www.youtube.com/watch?v=nWxguR5B5-s)

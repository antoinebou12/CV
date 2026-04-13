---
post_kind: article
title: "Network architecture — Lucidchart to PlantUML C4"
description: Moving home-network diagrams to PlantUML C4, Cloudflare DNS, Terraform, and Kubernetes on Proxmox / XCP-ng.
date: 2022-09-06T10:00:00-04:00
translationKey: home-network-plantuml-c4
tags:
    - Network
    - PlantUML
    - C4 model
    - Kubernetes
    - Proxmox
    - Terraform
    - Cloudflare
    - Home lab
images:
    - featured.jpeg
---

I've recently embarked on a journey to overhaul my home network setup. The transition from Draw.io to PlantUML C4 for creating deployment diagrams has been a game-changer. 🏡

![1688937733753.jpeg](images/1688937735221.jpeg)

PlantUML C4 offers a text-based 📝approach that integrates seamlessly with version control systems, making it an ideal tool for infrastructure as code (IaC)🏗️ .

![1688937733753.jpeg](images/1688937733753.jpeg)

I am also moving to Cloudflare for DNS management ✅
I gonna also use Terraform and Github action as CD🔁

On the virtualization front, I am now using Proxmox and XCP-ng as hypervisors, with Talos OS powering my Kubernetes deployments from my personal project. 💻
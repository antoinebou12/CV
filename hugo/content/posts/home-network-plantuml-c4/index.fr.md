---
post_kind: article
title: "Architecture réseau — de Lucidchart à PlantUML C4"
description: Faire évoluer les schémas du réseau domestique vers PlantUML C4, DNS Cloudflare, Terraform et Kubernetes sur Proxmox / XCP-ng.
date: 2022-09-06T10:00:00-04:00
translationKey: home-network-plantuml-c4
tags:
    - PlantUML
    - C4 Model
    - Homelab
    - Kubernetes
    - Proxmox
    - Terraform
    - Cloudflare
images:
    - featured.jpeg
---

J’ai récemment entamé une refonte de mon réseau domestique. Le passage de Draw.io à **PlantUML C4** pour les diagrammes de déploiement change la donne. 🏡

![1688937733753.jpeg](images/1688937735221.jpeg)

PlantUML C4 propose une approche **textuelle** 📝 qui s’intègre bien au contrôle de version, ce qui en fait un outil adapté à l’infrastructure as code (IaC) 🏗️ .

![1688937733753.jpeg](images/1688937733753.jpeg)

Je migre aussi vers **Cloudflare** pour la gestion DNS ✅  
Je compte utiliser **Terraform** et **GitHub Actions** comme CD 🔁

Côté virtualisation, j’utilise **Proxmox** et **XCP-ng** comme hyperviseurs, avec **Talos OS** pour mes déploiements Kubernetes issus d’un projet perso. 💻

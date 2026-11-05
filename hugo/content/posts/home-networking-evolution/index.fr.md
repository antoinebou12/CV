---
image_alt: "Vue d’ensemble homelab"
post_kind: article
title: "Évolution réseau — monter un lab à la maison"
date: 2021-09-06T10:00:00-04:00
lastmod: 2026-11-05T12:00:00-05:00
description: "Évolution d’un homelab — Dell R710, câblage de placard, piles Docker, Caddy, WireGuard, Proxmox, et pourquoi je dessine encore le réseau au mur."
translationKey: home-networking-evolution
tags:
  - Networking
  - Homelab
  - Docker
  - WireGuard
  - Proxmox
  - Caddy
images:
  - images/featured.png
---

Les factures cloud m’ont poussé vers un **lab maison** : vieux PC, Docker là où un SaaS suffisait, et assez de scripts pour tout reconstruire après un mauvais week-end. Ce billet raconte comment le réseau a grandi — pas un design parfait, mais une école de routage, VPN et virtualisation en cassant des choses chez moi.

<!--more-->

## Pourquoi un lab

Les cours couvraient IP, VPN et routage sur papier. Faire tourner des services à la maison rend les compromis concrets : courant, bruit, sauvegardes, et « qui a SSH quand le routeur lâche ». Je voulais un endroit où casser des choses sans facture cloud — et une histoire à raconter en entrevue qui ne se résume pas à « j’ai utilisé AWS une fois ».

## Docker en premier

J’ai aligné des **stacks conteneur gratuites** sur des jobs payés dans le cloud — média, tableaux de bord, petits outils. Docker a été la porte d’entrée pour voir le homelab comme des services composables plutôt qu’un seul gros serveur « animal de compagnie ».

Leçon restée : **un fichier compose par sujet**. Quand Plex faisait des siennes, je ne reconstruisais pas toute la machine — je recyclais le volume et j’apprenais ce qui persistait vraiment.

## Bash et deux machines

Matériel : un **Dell** pas cher et une machine de 2004. Scripts **bash** pour **Ubuntu**, **CentOS** et **Proxmox** — assez reproductibles pour que les réinstallations après expériences fassent moins mal.



### Rack physique (octobre 2022)

Avant les schémas Lucidchart, le lab tenait dans des **placards et étagères** — nœud de câbles compris. Photos recadrées d’anciennes stories ; c’est le vrai câblage, pas un rendu 3D.

**Pile murale** — switch, modem, routeur, **serveur entreprise (génération ~2010)**, onduleur, étiquetée pendant que j’apprenais encore qui branchait quoi :

![Pile réseau homelab étiquetée — switch, modem, routeur, serveur, UPS](./images/homelab-wall-stack-labeled.jpeg)

**Dell PowerEdge R710** — deux **Xeon X5667** (quad ~3 GHz), **24 Go RAM**, à côté de mousse acoustique. Le ruban adhésif sur le bezel, c’était mon inventaire :

![Serveur homelab Dell PowerEdge R710 — Xeon X5667, 24 Go RAM](./images/dell-poweredge-r710-homelab.jpeg)

**Placard** — serveur rack à l’horizontale, switch jaune, écran pour les installs locales, et assez de câbles bleus pour apprendre la patience :

![Placard serveur homelab — rack, switch, écran et câblage](./images/homelab-closet-server-setup.jpeg)

La virtualisation compte quand on prend un snapshot avant d’essayer une idée douteuse. Un hôte hyperviseur dédié bat les réinstallations à répétition sur bare-metal.

Le schéma Lucidchart, c’était la version « expliquer au coloc » — quel sous-réseau, quelle machine, ce qui est permis depuis Internet.

![Schéma réseau (Lucidchart)](./images/lucidchart.jpeg)

## Accès distant et bordure

**Caddy** en reverse proxy ; exposition via un frontal **OVH** pour ne pas n’exposer que l’IP résidentielle. L’admin à distance et la santé des services sont devenues une partie du même travail que « rendre le service joignable ». Le HTTPS automatique a compté plus que prévu — moins de renouvellements de certificats à la main, moins de commandes openssl tard le soir. J’ai ensuite repris ce réflexe sur AWS ; voir **[Caddy + EC2 + CloudWatch]({{< ref "/posts/caddy-ec2-cloudwatch-lambda/index.fr.md" >}})**.

**WireGuard** pour le VPN — pénible la première fois, rapide une fois en place. J’ai contribué à de petits scripts d’installation pour que des ami·e·s puissent se connecter sans lire les pages man pendant une semaine. Tunnel partiel ou tunnel complet : chaque invité relançait le débat ; documentez votre choix sur la page wiki que vous oublierez de mettre à jour.

## Après le déménagement

Nouvel appartement, plus de curiosité pour les VLAN, des VM **Proxmox** pour des projets de club. **Lucidchart** pour le schéma mural ; vue type **C4** pour expliquer la pile.

![Vue type C4](./images/c4.jpeg)

Plus tard, j’ai déplacé les sites publics vers l’**hébergement statique** (S3/GitHub Pages) pour réduire le coût du toujours-allumé — le lab est resté pour les services privés.

## Pannes mémorables

- **Un seul disque, pas de sauvegarde** — un `apt upgrade` raté et un week-end de réinstall.
- **Ports admin exposés** — admin derrière VPN seulement, appris à la dure.
- **Bruit thermique** — le R710 m’a fait penser aux courbes ventilateur avant « serveur » = « chambre à côté ».

## Bilan

Un homelab, c’est un bac à sable pour les réflexes **plateforme** : automatiser, documenter la topologie, supposer la panne. Liens actuels : **[MediaBoxDockerCompose](https://github.com/antoinebou12/MediaBoxDockerCompose)** et les scripts d’installation dans la liste de projets du CV.

## Articles connexes

- [MediaBox homelab — notes sur la stack Docker]({{< ref "/posts/mediabox-homelab-docker-catalog/index.fr.md" >}}) — compose, ports et scripts Proxmox
- [Renpho + Home Assistant]({{< ref "/posts/renpho-health-api-blueprint/index.fr.md" >}}) — données santé à la maison
- [Rack à planches — CAO vers bois]({{< ref "/posts/skate-rack-cad-to-object/index.fr.md" >}}) — projets physiques entre les câbles
- [Caddy sur AWS]({{< ref "/posts/caddy-ec2-cloudwatch-lambda/index.fr.md" >}}) — mêmes idées de proxy, autre facture

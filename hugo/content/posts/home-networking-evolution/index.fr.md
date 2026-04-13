---
post_kind: article
title: "Évolution du réseau — construire un lab à la maison"
date: 2021-09-06T10:00:00-04:00
description: Docker sur matériel réutilisé, automatisation bash, Caddy, WireGuard, VMs Proxmox et schémas de l’installation.
translationKey: home-networking-evolution
tags:
    - Networking
    - Homelab
    - Docker
    - WireGuard
    - Proxmox
    - Caddy
    - VPN
images:
    - featured.png
---

## Introduction

Bienvenue dans un nouveau chapitre du blog : les détails de la mise en place d’un **réseau domestique** solide. En tant qu’ingénieur logiciel passionné par les protocoles et le calcul efficace, j’ai voulu un système qui équilibre performance, sécurité et coût. Ce billet raconte l’expérience et les choix techniques.

## Relever le défi du réseau maison

Mon intérêt pour le réseau remonte aux études (IP, VPN, etc.). Face au coût du cloud, j’ai visé une solution locale avec du **matériel ancien**, pour limiter dépenses hardware et services en ligne tout en gardant une bonne fonctionnalité.

### Conteneurs Docker : polyvalence

Une part importante du projet : explorer **Docker** et des services gratuits pouvant remplacer le cloud (scan de documents, gestion du foyer, etc.). Cette exploration a servi de base pour comprendre l’architecture conteneurisée.

## Bash et serveurs à la maison

Le cœur du système : un **serveur Dell** acheté à bas prix et un vieux PC de 2004. J’ai écrit plusieurs scripts **bash** pour Ubuntu, CentOS et Proxmox afin d’installer et gérer les machines — automatisation et scripting au centre du réseau domestique.

![featured.png](images/featured.png)

### Obstacles et apprentissage

La maintenance a montré l’importance d’un **hyperviseur** adapté. J’ai fini par utiliser un serveur dédié à la virtualisation pour stabiliser et simplifier l’ensemble.

![lucidchart.jpeg](images/lucidchart.jpeg)

## Gestion à distance et sécurité

Il fallait pouvoir **administrer à distance** et surveiller santé des services et du matériel. J’ai mis un **reverse proxy Caddy** et masqué mon IP derrière un serveur **OVH** pour réduire les risques et mieux router le trafic.

### WireGuard comme VPN

Pour le VPN, choix de **WireGuard** : rapide et fiable une fois la config maîtrisée. J’ai aussi contribué à des projets pour simplifier son déploiement.

## Élargir le réseau

Après un déménagement, extension multi-sites avec **Lucidchart** pour visualiser l’architecture et **Proxmox** pour de nombreuses VMs — aussi utilisé dans un projet de club pour partager l’expérience.

![c4.jpeg](images/c4.jpeg)

### Projets futurs

Envisager un site statique sur **AWS S3** pour réduire les coûts de déploiement, et poursuivre l’usage de **GitHub** pour les projets personnels.

## Conclusion

Ce parcours mélange passion personnelle et développement pro. L’équilibre performance / sécurité / coût est au centre ; avec les bons outils, un réseau maison efficace est tout à fait réalisable et gratifiant.

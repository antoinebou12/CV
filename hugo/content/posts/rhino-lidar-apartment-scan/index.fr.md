---
post_kind: article
title: "Scan LiDAR d’un appartement avec Rhino sur iPhone"
date: 2024-01-02T10:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "LiDAR pièce par pièce avec Rhino sur iPhone — validation d’aménagement, limites du scan grand public, quand ça bat la CAO complète."
translationKey: rhino-lidar-apartment-scan
tags:
  - LiDAR
  - Rhino
  - iOS
  - 3D Scanning
  - Architecture
images:
  - featured.jpg
---

Nous avons scanné l’appartement avec **Rhino sur iPhone** et le **LiDAR** en **janvier 2024** — pas pour des plans de permis, mais pour trancher des questions d’aménagement avant d’acheter des meubles. **[English version]({{< ref "/posts/rhino-lidar-apartment-scan/index.md" >}})**.

<!--more-->

## Pourquoi

Le LiDAR d’un iPhone récent capture la profondeur vite. **Rhino** produit une géométrie que l’on peut orbiter sur le téléphone et mesurer grossièrement. Plus léger qu’un job CAO bureau pour « est-ce que ce bureau passe ? ».

Pas de remplacement d’arpenteur — besoin de **confiance relative** : largeur couloir, profondeur placard, mur TV réaliste ou non.

## Limites rencontrées

| Limite | Réaction |
|--------|----------|
| **Surfaces brillantes / sombres** | Trous sur verre et écran TV |
| **Désordre** | Cartons et chaises = murs bosselés — scanner avant déménagement |
| **Dérive** | Longues boucles — refermer lentement le parcours |
| **Export** | Mesh téléphone suffit pour mesurer ; NURBS fines = bureau |

## Méthode

Pièce par pièce, marche lente pendant la mise à jour du maillage. Pas de trépied — matériel grand public et patience.

- **Salon** — plus grand volume, repère d’échelle.
- **Couloir / placard** — espaces étroits, dérive visible vite.
- **Chambre** — meubles laissés volontairement pour voir le bruit.

![Workflow de scan sur iPhone](./images/Screenshot-from-2024-01-02-22-41-35.png)

![Revue du maillage dans Rhino](./images/Screenshot-from-2024-01-02-22-42-01.png)

## Captures

![Capture pièce — vue large](./images/1781a950-9e10-4bcd-b142-1711d9e73881.jpg)

![Autre angle — trous de couverture](./images/f33bc6af-8bf5-4f68-b9f0-6c1572258bff.jpg)

## Bilan

LiDAR handheld + appli de modélisation ciblée = assez pour **explorer un layout tôt**. Un meuble acheté grâce au scan rembourse l’heure passée.

Même fil **numérique → physique** : **[rack skate]({{< ref "/posts/skate-rack-cad-to-object/index.fr.md" >}})**, **[figurines IA]({{< ref "/posts/ai-figurines-3d-printing/index.fr.md" >}})**.

## Articles liés

- [Évolution réseau — lab maison]({{< ref "/posts/home-networking-evolution/index.fr.md" >}})
- [Support à planches — CAO au contreplaqué]({{< ref "/posts/skate-rack-cad-to-object/index.fr.md" >}})

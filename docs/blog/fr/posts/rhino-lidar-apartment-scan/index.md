# Scan LiDAR d’un appartement avec Rhino sur iPhone

> LiDAR pièce par pièce avec Rhino sur iPhone — validation d’aménagement, limites du scan grand public, quand ça bat la CAO complète.

- Page HTML: https://antoineboucher.info/CV/blog/fr/posts/rhino-lidar-apartment-scan/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/posts/rhino-lidar-apartment-scan/index.md
- Publié: 2024-01-02
- Mis à jour: 2026-05-22
- Tags: LiDAR, Rhino, IOS, 3D Scanning, Architecture
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)Nous avons scanné l’appartement avec **Rhino sur iPhone** et le **LiDAR** en **janvier 2024** — pas pour des plans de permis, mais pour trancher des questions d’aménagement avant d’acheter des meubles.

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

![Workflow de scan sur iPhone](https://antoineboucher.info/CV/blog/posts/rhino-lidar-apartment-scan/images/Screenshot-from-2024-01-02-22-41-35.png)

![Revue du maillage dans Rhino](https://antoineboucher.info/CV/blog/posts/rhino-lidar-apartment-scan/images/Screenshot-from-2024-01-02-22-42-01.png)

## Captures

![Capture pièce — vue large](https://antoineboucher.info/CV/blog/posts/rhino-lidar-apartment-scan/images/1781a950-9e10-4bcd-b142-1711d9e73881.jpg)

![Autre angle — trous de couverture](https://antoineboucher.info/CV/blog/posts/rhino-lidar-apartment-scan/images/f33bc6af-8bf5-4f68-b9f0-6c1572258bff.jpg)

## Bilan

LiDAR handheld + appli de modélisation ciblée = assez pour **explorer un layout tôt**. Un meuble acheté grâce au scan rembourse l’heure passée.

Même fil **numérique → physique** : **[rack skate](https://antoineboucher.info/CV/blog/fr/posts/skate-rack-cad-to-object/)**, **[figurines IA](https://antoineboucher.info/CV/blog/fr/posts/ai-figurines-3d-printing/)**.

## Articles liés

- [Évolution réseau — lab maison](https://antoineboucher.info/CV/blog/fr/posts/home-networking-evolution/)
- [Support à planches — CAO au contreplaqué](https://antoineboucher.info/CV/blog/fr/posts/skate-rack-cad-to-object/)

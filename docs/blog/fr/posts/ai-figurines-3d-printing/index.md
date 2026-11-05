# Figurines IA pour impression 3D

> Figurines chibi, ComfyUI avec OmniGen2 et Hunyuan3D v2, et notes d’impression résine.

- Page HTML: https://antoineboucher.info/CV/blog/fr/posts/ai-figurines-3d-printing/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/index.md
- Publié: 2026-05-22
- Mis à jour: 2026-10-27
- Tags: Impression 3D, IA, Hunyuan3D, ComfyUI, Chibi
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)Une image de jouet en 2D bien définie donne au modèle image→3D un point de départ utile. Suivez les étapes avec les [diapositives](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/make-figurines-using-ai-for-3d-printing.pptx) et le [workflow ComfyUI](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/workflows/image_omnigen2_image_edit.json).

## Pipeline (ordre)

1. **Photo de référence** — profil ou face nette.
2. **Rendu chibi vinyle** — ChatGPT, Midjourney ou ComfyUI (OmniGen2).
3. **Maillage** — Hunyuan3D v2 (ComfyUI local ou outils en ligne).
4. **Impression** — orientation, supports, résine ; îlots avec **[UVtools](https://github.com/sn4k3/UVtools)** si besoin.

![Photo vers objet — photo, image IA jouet, modèle 3D, impression résine](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/photo-to-object-pipeline.png)

Diagramme de séquence ([source Mermaid](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/figurine-pipeline-sequence.mmd)) :

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Photo as Reference photo
    participant ComfyUI
    participant OmniGen2 as OmniGen2 stage
    participant Hunyuan3D as Hunyuan3D v2 stage
    participant Slicer as Resin slicer
    participant Printer

    User->>Photo: Side or front reference
    User->>ComfyUI: Load chibi workflow + reference-photo.jpg
    ComfyUI->>OmniGen2: ReferenceLatent + chibi vinyl prompt
    OmniGen2-->>ComfyUI: PNG (white background)
    ComfyUI->>Hunyuan3D: CLIPVision + image-to-mesh
    Hunyuan3D-->>ComfyUI: GLB (VoxelToMesh 0.7 / 0.6)
    ComfyUI-->>User: mesh/ComfyUI*.glb
    User->>Slicer: Orient, supports, hollow
    Slicer-->>User: Sliced job
    User->>Printer: Resin print
    Printer-->>User: Chibi figurine
```

**Diapositives** (~17 Mo) — captures et liens outils de la présentation :

## Étape 1 — Jouet / chibi en 2D

> Convert this image into a toy-style plastic figure. Keep features but simplify and smoothen as if molded in plastic.

![Avant / après](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/slide03-upload-before.png) ![Résultat](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/slide03-upload-after.png)

**Prompt chibi :** figurine vinyle chibi, plastique lisse, fond blanc, un personnage, pose stable sur socle.

![Bernois](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/gallery/chibi-bernese-puppy-snow.png) ![Golden](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/gallery/chibi-golden-retriever-puppy.png) ![Cowboy](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/gallery/chibi-cowboy-no-name.png) ![Piscine](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/gallery/chibi-pool-tube-cigar.png) ![Araignée](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/gallery/chibi-spider-toy.png)

## Étape 2 — ComfyUI (un graphe)

**Télécharger :** [image_omnigen2_image_edit.json](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/workflows/image_omnigen2_image_edit.json) — *Load* dans ComfyUI (OmniGen2 + Hunyuan3D v2). Photo dans `input/` : **`reference-photo.jpg`**.

| Étape | Rôle |
|-------|------|
| **A** | OmniGen2 + `ReferenceLatent` → PNG chibi |
| **B** | Hunyuan3D v2 → deux GLB (`mesh/ComfyUI*.glb`) |

Prompts et graines dans le JSON. Nœuds Hunyuan3D-2 ([GitHub](https://github.com/Tencent-Hunyuan/Hunyuan3D-2)). Sur 8–12 Go VRAM, baisser `octree_resolution` ou `num_chunks`.

## Étape 3 — Image vers 3D (hébergé)

![Hunyuan3D et Rodin](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/slide05-hunyuan-rodin.png)

La clarté du PNG jouet compte plus que la marque du générateur.

| Outil | Lien | Notes |
|------|------|--------|
| **Hunyuan3D-2** | [GitHub](https://github.com/Tencent-Hunyuan/Hunyuan3D-2) | Poids ouverts, local ou hébergé |
| **RodinHD** | [Démo](https://rodinhd.github.io/) | Figurines / avatars détaillés |
| **Hi3DGen** | [Space](https://huggingface.co/spaces/Stable-X/Hi3DGen) | Prior 2D + cohérence géométrie ([CHI 2024](https://doi.org/10.1145/3641520.3665304)) |
| **Hyper3D** | [hyper3d.ai](https://hyper3d.ai/) | Commercial rapide |
| **Meshy** | [meshy.ai](https://www.meshy.ai/) | Texte/image → 3D, remaillage |
| **Tripo3D** | [studio.tripo3d.ai](https://studio.tripo3d.ai/) | Studio navigateur |
| **Sparc3D** | [lizhihao6.github.io/Sparc3D](https://lizhihao6.github.io/Sparc3D/) | Reconstruction multi-vues |

![Tripo3D](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/slide06-tripo3d.png)

![Hyper3D](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/slide07-hyper3d.png)

![Sparc3D](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/slide08-sparc3d.png)

![Meshy](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/slide09-meshy.png)

## Quand utiliser quoi

| Situation | Piste |
|----------|--------|
| VRAM 8–12 Go, une photo | ComfyUI local (workflow fourni) |
| Test rapide sans GPU | Hi3DGen / Tripo3D en ligne |
| Figurine chibi déjà propre | Hunyuan3D ou RodinHD |
| Impression résine fine | Réduire faces, vérifier îlots UVtools |

## Pièges

- **Photo de profil floue** — le maillage fond les traits.
- **GLB énormes dans git** — garder hors dépôt ; exporter depuis `mesh/`.
- **Sous-estimer les supports** — cheveux et capes = îlots en slicer.

## Aperçu maillage

Les **GLB** d’exemple (Hunyuan3D, RodinHD, Hyper3D, Hi3DGen) ne sont pas versionnés ici (20–75 Mo chacun). Utilisez l’aperçu des outils ou exportez depuis ComfyUI (`mesh/ComfyUI*.glb`).

![Aperçu maillage dans l’UI](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/slide11-preview.gif)

## Étape 4 — Réglages maillage

![Réglages (animé)](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/slide10-settings.gif)

Ajuster faces, symétrie et remaillage avant export GLB/OBJ.

## Étape 5 — Impression résine

![Préparation impression](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/slide13-print-1.png)

![Plateau](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/slide13-print-2.png)

Résine pour petites pièces ; incliner les porte-à-faux vers le plateau.

![Îlots](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/slide14-islands.png)

Vérifier les îlots avec le slicer ou **[UVtools](https://github.com/sn4k3/UVtools)**.

## Résultats

![Figurine 1](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/slide15-result-1.jpeg)

![Figurine 2](https://antoineboucher.info/CV/blog/posts/ai-figurines-3d-printing/images/slide15-result-2.jpeg)

## Références

- Gao et al. (2024). *Hi3DGen.* CHI 2024. https://doi.org/10.1145/3641520.3665304
- Tencent Hunyuan. *Hunyuan3D-2.* https://github.com/Tencent-Hunyuan/Hunyuan3D-2

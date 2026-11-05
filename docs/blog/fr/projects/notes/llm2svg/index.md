# LLM2SVG : Analyser les données avant de parler de modèle

> Ce fork LLM2SVG contient des outils de données SVG et une structure d’évaluation. L’implémentation permet d’examiner exemples et contraintes, sans…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/llm2svg/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/llm2svg/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/antoinebou12/LLM2SVG
- Révision inspectée: a8337761b49bbdcbac24f58c6adc5f17d1ac2a07

## Résumé

Ce fork LLM2SVG contient des outils de données SVG et une structure d’évaluation. L’implémentation permet d’examiner exemples et contraintes, sans démontrer un modèle texte-vers-SVG terminé ou entraîné.

**Pourquoi il existe:** Générateur et validateur Python d'illustrations vectorielles SVG à partir de descriptions en langage naturel.

**Cas d’usage:** Génération automatisée d'icônes et d'illustrations vectorielles pour systèmes de design.

## Cas d’utilisation

Outils Python et données pour un défi texte vers SVG : charger les consignes, valider les SVG, créer et rendre des formes.

- **Charger consignes et SVG** (Chercheur en ML): SVGDataLoader (utils/data_loader.py) lit data/train/train.csv et data/test/test.csv et rassemble les SVG rangés sous data/train/svg/<id>/ ; SVGDataset (utils/svg_dataset.py) les expose comme Dataset PyTorch.
- **Valider les contraintes SVG** (Chercheur en ML): SVGConstraints.validate_svg (utils/svg_constraints.py) refuse les fichiers de plus de 10 000 octets et tout élément ou attribut hors de la liste permise, avec une analyse defusedxml.
- **Repérer les termes clés** (Chercheur en ML): TextParser (utils/text_parser.py) repère couleurs, formes, motifs, matières, vêtements, paysages et architecture dans une description et en déduit une catégorie principale.
- **Composer un SVG de formes** (Chercheur en ML): utils/svg_utils.py fournit des fonctions pour rect, circle, ellipse, path, polygon, line et group, un générateur de palette, generate_shapes et optimize_svg qui raccourcit les nombres.
- **Convertir un SVG en PNG** (Chercheur en ML, Moteur cairosvg): svg_to_png (utils/svg_utils.py) appelle cairosvg.svg2png et écrit un fichier ou renvoie les octets PNG.
- **Analyser le jeu de SVG** (Chercheur en ML): SVGAnalyzer (utils/svg_analyzer.py) compte les SVG, mesure leur taille, recense les éléments, valide chaque fichier et trace un histogramme des tailles face à la limite de 10 Ko.

### Scénario : Vérifier des SVG candidats avant soumission

1. Pointer SVGDataLoader vers le dossier data/ local (le chemin par défaut vise le disque Windows de l’auteur).
2. Lire les consignes de data/train/train.csv, par exemple « a starlit night over snow-covered peaks ».
3. Lancer SVGAnalyzer.validate_all_svgs("train") pour tester chaque SVG de data/train/svg/ avec SVGConstraints.
4. Appeler generate_summary_report pour obtenir un tableau des tailles et des sources déduites, puis plot_svg_size_distribution.
5. Rendre un SVG valide avec svg_to_png pour le comparer à la consigne.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Python | 100 |

## Démarrage (commandes du dépôt, non exécutées ici)

### README.md · Dependencies

```bash
pip install cairosvg torch torchvision
```


## Fonctions et composants

- **Chargement et contraintes** — SVGAnalyzer utilise SVGDataLoader et SVGConstraints. Il énumère les exemples, relève les tailles et vérifie les contraintes. Le chargement et la validation constituent des responsabilités distinctes.
- **Rapports sur les données** — L’analyseur compte les noms d’éléments et conserve des résultats de validation par exemple. Sa méthode de résumé retourne un DataFrame pandas. Le comptage utilise une expression régulière pour tolérer du SVG mal formé.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Fichiers du jeu de données → SVGDataLoader
- SVGDataLoader → Analyse des éléments et tailles
- SVGDataLoader → Vérifications des contraintes
- Analyse des éléments et tailles → Rapport de données
- Vérifications des contraintes → Rapport de données

```mermaid
flowchart LR
  n0["Fichiers du jeu de données"]
  n1["SVGDataLoader"]
  n2["Analyse des éléments et tailles"]
  n3["Vérifications des contraintes"]
  n4["Rapport de données"]
  n0 --> n1
  n1 --> n2
  n1 --> n3
  n2 --> n4
  n3 --> n4
```

**Un parcours dans le code:** Suivez validate_all_svgs et comparez-le à analyze_elements. Respecter les contraintes et posséder des noms d’éléments plausibles sont deux vérifications différentes; aucune ne prouve la ressemblance visuelle avec une consigne.

## Limites et points à vérifier

L’analyseur possède un chemin de données par défaut propre à une machine. Ces utilitaires ne permettent pas de déduire qualité du modèle, résultats d’entraînement ou scores.

## Fichiers à lire

- [utils/svg_analyzer.py](https://github.com/antoinebou12/LLM2SVG/blob/main/utils/svg_analyzer.py)
- [utils/data_loader.py](https://github.com/antoinebou12/LLM2SVG/blob/main/utils/data_loader.py)
- [utils/svg_constraints.py](https://github.com/antoinebou12/LLM2SVG/blob/main/utils/svg_constraints.py)



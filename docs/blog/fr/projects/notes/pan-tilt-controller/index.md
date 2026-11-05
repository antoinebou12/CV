# Pan-Tilt-Controller : Du clavier aux commandes série des moteurs

> Ce contrôleur pan-tilt archivé relie une interface desktop à une unité de positionnement série. L’implémentation combine une boucle Qt et des commandes…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/pan-tilt-controller/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/pan-tilt-controller/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Dépôt: https://github.com/antoinebou12/Pan-Tilt-Controller
- Révision inspectée: b565efdf9d3fc83096d18c667b6d7a7e21383377

## Résumé

Ce contrôleur pan-tilt archivé relie une interface desktop à une unité de positionnement série. L’implémentation combine une boucle Qt et des commandes pyserial, avec les positions demandées conservées dans des variables globales.

**Pourquoi il existe:** Contrôleur série et démon de mouvement pour unité robotique pan-tilt de précision PTU-46.

**Cas d’usage:** Positionnement robotique de caméras pour la vision par ordinateur.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Python | 100 |

## Fonctions et composants

- **Événements d’interface** — pantiltcontroller.py utilise PyQt5 et installe un filtre de touches. Les flèches et boutons modifient une position, puis construisent une commande pp ou tp. Ce code diffère de l’ancien framework décrit dans le README.
- **Initialisation du matériel** — Le module ouvre COM3 à 9600 bauds et écrit des commandes dès son chargement. L’interface dépend donc immédiatement du matériel, avant le choix d’un port ou la confirmation d’un mouvement.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Touche ou bouton Qt → Position demandée
- Position demandée → Commande série
- Commande série → Connexion pyserial
- Connexion pyserial → Matériel pan-tilt

```mermaid
flowchart LR
  n0["Touche ou bouton Qt"]
  n1["Position demandée"]
  n2["Commande série"]
  n3["Connexion pyserial"]
  n4["Matériel pan-tilt"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
```

**Un parcours dans le code:** Suivez une flèche depuis positionPan ou positionTilt jusqu’à ser.write. La variable représente la cible commandée, pas une mesure indépendante de la position physique.

## Limites et points à vérifier

Ne chargez pas ce script avec du matériel connecté sans vérifier les mouvements initiaux, limites et arrêts d’urgence. Il utilise aussi une syntaxe de l’époque Python 2.

## Fichiers à lire

- [pantiltcontroller.py](https://github.com/antoinebou12/Pan-Tilt-Controller/blob/master/pantiltcontroller.py)
- [PTC-command.py](https://github.com/antoinebou12/Pan-Tilt-Controller/blob/master/PTC-command.py)
- [README.md](https://github.com/antoinebou12/Pan-Tilt-Controller/blob/master/README.md)


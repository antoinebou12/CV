# WearMachine : les fichiers CAO d’un banc d’usure GelSight

> Fichiers STEP, STL, DXF et dessins d’un petit banc d’usure par glissement : rail, poussoir, porte-poids et porte-échantillons GelSight.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/wearmachine/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/wearmachine/index.md
- Publié: 2026-11-05
- Mis à jour: 2026-11-06
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/ETSim/WearMachine
- Révision inspectée: beff25e1c78c84d26598153a20afe76fbae6a9b9


## Cas d’utilisation

Fichiers CAO, d'impression et de dessin d'un petit banc d'usure par glissement dont les échantillons passent au GelSight.

- **Imprimer les pièces** (Constructeur du banc, Imprimante ou découpe): Print/ contient les STL du rail, du support de rail, du patin, du poussoir, de l'entretoise, du support de roulement, du support moteur, de l'écrou, des porte-échantillons et des porte-poids.
- **Modifier les pièces en CAO** (Constructeur du banc): Raw/ conserve les solides STEP des porte-échantillons, des pièces du rail et de la plupart des porte-poids pour modifier les cotes avant impression.
- **Découper les pièces DXF** (Constructeur du banc, Imprimante ou découpe): Drawing/ fournit les contours DXF, dont une plaque Base disponible seulement en DXF, ainsi qu'une feuille Inkscape A4 à 16 trous pour un moule.
- **Régler la charge normale** (Constructeur du banc): Les Weight Holder existent en versions 10, 20, 50, 100, 200, 500 et 1000 g pour appliquer une charge choisie sur l'échantillon.
- **Placer sous le GelSight** (Constructeur du banc, Scanner GelSight): Les porte-échantillons de 30 mm et 40 mm et un support carré de paillasse placent les échantillons usés pour la capture GelSight, comme le décrit le README.

### Scénario : Monter le banc et lancer un essai chargé

1. Ouvrir Picture/Assembly.png pour voir le cadre à deux rails et la traverse à cinq trous d'échantillons.
2. Imprimer Rail, Rail_Holder, Rail_Ski, Pusher, Seperator, Holder Berring, nema17bracket_v2 et t8_nut depuis Print/Rail/.
3. Découper la plaque Base depuis Drawing/Rail/Base.dxf et monter le rail avec un moteur NEMA 17 et une vis T8.
4. Imprimer le porte-poids de la charge visée, par exemple Weight Holder 200g.stl, et le poser sur l'échantillon.
5. Après chaque distance de glissement, placer l'échantillon dans le support 30 mm ou 40 mm et le numériser au GelSight.



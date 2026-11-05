# Maestro : Une partition dans un pipeline de conversion

> Ce fork Maestro relie une interface d’envoi React à un backend Spring et des outils de conversion musicale. Passer d’une image de partition au MIDI…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/maestro/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/maestro/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/antoinebou12/Maestro
- Licence: AGPL-3.0
- Révision inspectée: 6dca488e6e0e6bc444d3e57d6d3d62bad4ca4783

## Résumé

Ce fork Maestro relie une interface d’envoi React à un backend Spring et des outils de conversion musicale. Passer d’une image de partition au MIDI demande une reconnaissance optique et une représentation intermédiaire.

**Pourquoi il existe:** Pipeline de reconnaissance optique de partitions musicales (OMR) convertissant des images en fichiers MIDI.

**Cas d’usage:** Numérisation de partitions musicales physiques pour écoute et arrangement.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Java | 47.34 |
| TypeScript | 32.3 |
| Python | 16.02 |
| Dockerfile | 3.14 |
| HTML | 1 |
| Shell | 0.2 |

## Démarrage (commandes du dépôt, non exécutées ici)

### README.md · Getting Started

```bash
  git clone https://github.com/PrimePhil/PFE008
```

### README.md · Frontend

```bash
  cd maestro-app
```

### README.md · Frontend

```bash
  npm install
```

### README.md · Frontend

```bash
  npm run start
```

### README.md · Tests

```bash
gradle test
```


## Fonctions et composants

- **Frontière d’envoi** — ConvertController accepte des fichiers multipart sur /convert. Il rejette les fichiers vides, contrôle la limite de 10 Mio et vérifie la signature avant sauvegarde. Un tempo optionnel accompagne la demande.
- **Processus externes** — AudiverisController construit une commande selon le système et attend le processus Audiveris. Le backend comprend aussi MxlToMidi.py. Le démarrage, les fichiers intermédiaires et le téléchargement peuvent échouer séparément.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Envoi React → Validation Spring
- Validation Spring → Reconnaissance Audiveris
- Reconnaissance Audiveris → Conversion MusicXML
- Conversion MusicXML → Téléchargement MIDI

```mermaid
flowchart LR
  n0["Envoi React"]
  n1["Validation Spring"]
  n2["Reconnaissance Audiveris"]
  n3["Conversion MusicXML"]
  n4["Téléchargement MIDI"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
```

**Un parcours dans le code:** Suivez /convert dans ses validations, puis le choix de l’exécutable et du dossier de sortie. Un envoi HTTP réussi ne suffit pas: la conversion dépend aussi de l’outil externe et de ses fichiers.

## Limites et points à vérifier

La précision dépend de l’image et du moteur de reconnaissance. Les chemins partagés et commandes shell demandent une revue avant des envois publics simultanés.

## Fichiers à lire

- [backend/src/main/java/PFE008/backend/ConvertController.java](https://github.com/antoinebou12/Maestro/blob/main/backend/src/main/java/PFE008/backend/ConvertController.java)
- [backend/src/main/java/PFE008/backend/AudiverisController.java](https://github.com/antoinebou12/Maestro/blob/main/backend/src/main/java/PFE008/backend/AudiverisController.java)
- [backend/src/main/MxlToMidi.py](https://github.com/antoinebou12/Maestro/blob/main/backend/src/main/MxlToMidi.py)
- [maestro-app/package.json](https://github.com/antoinebou12/Maestro/blob/main/maestro-app/package.json)



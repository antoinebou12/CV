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

## Cas d’utilisation

Application web qui transforme une partition numérisée (PDF, PNG, JPG) en fichier MIDI, avec tempos ajustables.

- **Téléverser une partition** (Musicien): Le formulaire React (maestro-app/src/pages/MusicSheetUploadForm/MusicSheetUploadForm.tsx) reçoit le fichier déposé et un nom de MIDI ; useMaestroClient.ts vérifie GET /health avant d’envoyer à /convert.
- **Régler le tempo par mesure** (Musicien): Le formulaire garde une liste de tempos, mesures et options « forcer » (120 à la mesure 1 par défaut) et l’envoie dans le champ JSON tempos.
- **Lire les notes avec Audiveris** (Moteur OMR Audiveris): POST /convert (ConvertController.java) vérifie le fichier (10 Mo au plus, signature PDF/JPG/PNG) puis AudiverisController.java lance Audiveris en mode batch pour exporter un .mxl.
- **Convertir MusicXML en MIDI** (music21 (Python)): backend/src/main/MxlToMidi.py charge le .mxl avec music21, applique les nuances et les tempos demandés, puis écrit le .mid.
- **Télécharger le fichier MIDI** (Musicien): Le backend renvoie le .mid en pièce jointe et le frontend l’enregistre avec js-file-download ; les dossiers In et Out sont nettoyés trois secondes plus tard.
- **Basculer anglais ou français** (Musicien): LanguageSwitcher.tsx bascule i18next entre en-US et fr-CA à partir des textes de maestro-app/public/locales/.

### Scénario : Transformer une partition PDF en MIDI en local

1. Copier les dossiers bin et lib d’Audiveris dans backend/audiveris/dist, comme l’indique backend/README.md.
2. Démarrer les deux services avec docker-compose up -d (backend sur le port 8080, frontend sur le port 3000).
3. Ouvrir localhost:3000, déposer une partition PDF et saisir un nom de fichier MIDI.
4. Ajouter une ligne de tempo, par exemple 90 à la mesure 1, puis envoyer le formulaire.
5. Le backend lance Audiveris puis MxlToMidi.py, et le navigateur télécharge le .mid.

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



# AudioTranscript : Des segments WAV à la transcription

> AudioTranscript découpe un enregistrement WAV autour des silences, transmet les segments à un service de reconnaissance et rassemble le texte.…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/audiotranscript/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/audiotranscript/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Dépôt: https://github.com/antoinebou12/AudioTranscript
- Licence: MIT
- Révision inspectée: 91b458e4385f0be729d8af54d8b500dc9d00a274

## Résumé

AudioTranscript découpe un enregistrement WAV autour des silences, transmet les segments à un service de reconnaissance et rassemble le texte. L’implémentation utilise Amazon, même si ses docstrings mentionnent encore Google.

**Pourquoi il existe:** Pipeline de traitement et de transcription audio avec alignement temporel.

**Cas d’usage:** Transcription automatique par lots d'enregistrements audio.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Python | 100 |

## Démarrage (commandes du dépôt, non exécutées ici)

### README.md · Usage

```bash
python main.py --path <audio_file_path> --min-silence-len <min_silence_length> --silence-thresh <silence_threshold> --keep-silence <keep_silence_duration> --language <language_code>
```


## Fonctions et composants

- **Découpage audio** — main.py charge un WAV avec pydub et appelle split_on_silence. Le seuil est calculé par rapport au niveau dBFS de l’enregistrement. Chaque segment est exporté dans audio-chunks avant la reconnaissance.
- **Reconnaissance et sortie** — Un Recognizer de SpeechRecognition lit chaque fichier exporté et appelle recognize_amazon. La boucle ajoute le résultat à whole_text, ensuite affiché et retourné. Typer expose le fichier et les paramètres de découpage.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Enregistrement WAV → Découpage pydub
- Découpage pydub → Segments WAV temporaires
- Segments WAV temporaires → Reconnaissance Amazon
- Reconnaissance Amazon → Texte assemblé

```mermaid
flowchart LR
  n0["Enregistrement WAV"]
  n1["Découpage pydub"]
  n2["Segments WAV temporaires"]
  n3["Reconnaissance Amazon"]
  n4["Texte assemblé"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
```

**Un parcours dans le code:** Suivez transcribe_audio_file plutôt que sa docstring: la fonction vérifie les variables AWS juste avant recognize_amazon. L’argument de langue est exposé par la CLI, sans être transmis à cet appel.

## Limites et points à vérifier

L’audio quitte la machine pour la reconnaissance. Le code réutilise des noms fixes de tâche et de fichier; des exécutions simultanées nécessitent une gestion distincte des noms et fichiers temporaires.

## Fichiers à lire

- [main.py](https://github.com/antoinebou12/AudioTranscript/blob/main/main.py)
- [requirements.txt](https://github.com/antoinebou12/AudioTranscript/blob/main/requirements.txt)


# SpringBootFilesUploader : Séparer les octets et les métadonnées

> SpringBootFilesUploader est un backend Kotlin et Spring qui sépare stockage binaire et métadonnées. L’identifiant retourné au client relie ces deux…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/springbootfilesuploader/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/springbootfilesuploader/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Dépôt: https://github.com/antoinebou12/SpringBootFilesUploader
- Licence: MIT
- Révision inspectée: 3be3bbc6d828edf840ab6edaffee661db671d7db

## Résumé

SpringBootFilesUploader est un backend Kotlin et Spring qui sépare stockage binaire et métadonnées. L’identifiant retourné au client relie ces deux représentations lors du téléchargement.

**Pourquoi il existe:** Microservice Spring Boot en Kotlin avec téléversement multipart en flux et validation d'intégrité.

**Cas d’usage:** Backend ingestion de fichiers à haut débit.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Kotlin | 99.52 |
| Java | 0.31 |
| Dockerfile | 0.17 |

## Fonctions et composants

- **Validation HTTP** — FilesController reçoit un document multipart, vérifie l’extension et déclare des rôles modérateur/admin pour l’envoi. Le contrôle de taille est commenté. Le téléchargement utilise un identifiant, le type et la taille conservés.
- **Coordination du stockage** — FilesService crée un chemin fondé sur un UUID et envoie les octets à FileRepository. Il conserve ensuite FileModel par FilesMongo. La lecture cherche d’abord les métadonnées, puis utilise le chemin pour récupérer les octets.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Envoi multipart → FilesController
- FilesController → FilesService
- FilesService → Stockage binaire FileRepository
- FilesService → Métadonnées FilesMongo
- Métadonnées FilesMongo → Réponse avec identifiant

```mermaid
flowchart LR
  n0["Envoi multipart"]
  n1["FilesController"]
  n2["FilesService"]
  n3["Stockage binaire FileRepository"]
  n4["Métadonnées FilesMongo"]
  n5["Réponse avec identifiant"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n2 --> n4
  n4 --> n5
```

**Un parcours dans le code:** Suivez addDocument dans FilesService: les octets sont écrits avant les métadonnées. Si la seconde écriture échoue, la première peut laisser un fichier orphelin. Une version de production nécessite un nettoyage ou une stratégie de cohérence explicite.

## Limites et points à vérifier

Les annotations de rôles nécessitent la configuration de sécurité correspondante. L’extension ne valide pas le contenu et document.bytes charge le fichier en mémoire.

## Fichiers à lire

- [src/main/kotlin/com/api/project/controller/FilesController.kt](https://github.com/antoinebou12/SpringBootFilesUploader/blob/main/src/main/kotlin/com/api/project/controller/FilesController.kt)
- [src/main/kotlin/com/api/project/service/FilesService.kt](https://github.com/antoinebou12/SpringBootFilesUploader/blob/main/src/main/kotlin/com/api/project/service/FilesService.kt)
- [build.gradle.kts](https://github.com/antoinebou12/SpringBootFilesUploader/blob/main/build.gradle.kts)


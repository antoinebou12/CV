# SpringBootFilesUploader: File bytes and metadata on separate paths

> SpringBootFilesUploader is a Kotlin and Spring backend with a file-upload path that separates binary storage from document metadata. A file identifier…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/springbootfilesuploader/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/springbootfilesuploader/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/antoinebou12/SpringBootFilesUploader
- License: MIT
- Inspected revision: 3be3bbc6d828edf840ab6edaffee661db671d7db

## Summary

SpringBootFilesUploader is a Kotlin and Spring backend with a file-upload path that separates binary storage from document metadata. A file identifier returned to the client connects those two representations during download.

**Why it exists:** Spring Boot microservice written in Kotlin with streaming multipart file upload and integrity validation.

**Best fit:** High-throughput file ingestion and storage backend.

## Use cases

Kotlin Spring Boot API that stores uploaded files in MinIO/S3 behind JWT roles, with Docker and SSH admin endpoints.

- **Sign up and get a JWT** (API user, MinIO S3 and MongoDB): POST /auth/signup saves a user with hashed password and roles in MongoDB; POST /auth/signin returns a JwtResponse with the token and roles (AuthController.kt, JwtUtils.kt).
- **Upload a document** (Moderator or admin, MinIO S3 and MongoDB): POST /files/documents (moderator or admin) checks the extension against DOC_FILE_EXTENSION_REGEX, writes the bytes to the S3 bucket under files/<uuid>/<name> and records metadata in MongoDB.
- **Download a stored file** (API user, MinIO S3 and MongoDB): GET /files/{id} looks up the file record in MongoDB, reads the object from S3 and returns it as an attachment with its content type and size.
- **Manage Docker containers** (Moderator or admin): The /containers routes list, create, start, stop, restart and rename containers through docker-java against the Docker host set in application.yml (tcp://127.0.0.1:2375).
- **Run a remote SSH command** (Moderator or admin): POST /ssh/cli (admin only) opens an Apache SSHD session with the host, port and credentials in the request body and returns the command output.

### Scenario: Store a PDF and fetch it back

1. Start MongoDB on localhost:27017 and MinIO on localhost:9000, as configured in application.yml, then run ./gradlew bootRun.
2. POST /auth/signup with a username, email, password and the role "mod".
3. POST /auth/signin and copy the JWT from the response.
4. POST /files/documents with the PDF in the multipart field "document" and the Bearer token; the response returns fileId and fileName.
5. GET /files/{fileId} to download the PDF, or browse the routes in Swagger UI at /api-docs.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Kotlin | 99.52 |
| Java | 0.31 |
| Dockerfile | 0.17 |

## Features and components

- **HTTP validation** — FilesController accepts a multipart document, checks its filename extension and declares moderator/admin upload roles. The size-check block is commented out. Downloads use a file ID and return stored content type and length.
- **Storage coordination** — FilesService creates a UUID-based path and sends bytes to FileRepository. It then saves a FileModel through FilesMongo. Reads look up the metadata first, then use its path to retrieve the bytes.

## Architecture

Components and connections verified in the repository.

- Multipart upload → FilesController
- FilesController → FilesService
- FilesService → FileRepository binary storage
- FilesService → FilesMongo metadata
- FilesMongo metadata → File ID response

```mermaid
flowchart LR
  n0["Multipart upload"]
  n1["FilesController"]
  n2["FilesService"]
  n3["FileRepository binary storage"]
  n4["FilesMongo metadata"]
  n5["File ID response"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n2 --> n4
  n4 --> n5
```

**One path through the code:** Follow addDocument in FilesService: binary storage is written before metadata. If the second write fails, the first can leave an orphaned file. A production version needs cleanup or another explicit consistency strategy.

## Constraints and checks

Role annotations need the corresponding security configuration. Extension checks are not content validation, and buffering document.bytes loads the upload into memory.

## Files to read

- [src/main/kotlin/com/api/project/controller/FilesController.kt](https://github.com/antoinebou12/SpringBootFilesUploader/blob/main/src/main/kotlin/com/api/project/controller/FilesController.kt)
- [src/main/kotlin/com/api/project/service/FilesService.kt](https://github.com/antoinebou12/SpringBootFilesUploader/blob/main/src/main/kotlin/com/api/project/service/FilesService.kt)
- [build.gradle.kts](https://github.com/antoinebou12/SpringBootFilesUploader/blob/main/build.gradle.kts)



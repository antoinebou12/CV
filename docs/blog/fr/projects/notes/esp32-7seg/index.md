# ESP32-7SEG : Une horloge embarquée avec configuration réseau

> ESP32-7SEG relie une horloge sur ESP32 à une configuration réseau et une interface HTTP. Le démarrage détermine si les paramètres Wi-Fi sauvegardés…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/esp32-7seg/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/esp32-7seg/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Dépôt: https://github.com/antoinebou12/ESP32-7SEG
- Licence: MIT
- Révision inspectée: 6cac20eed8dc6293d011a0c8a8341654e0870b80

## Résumé

ESP32-7SEG relie une horloge sur ESP32 à une configuration réseau et une interface HTTP. Le démarrage détermine si les paramètres Wi-Fi sauvegardés peuvent être réutilisés ou si le parcours de configuration est nécessaire.

**Pourquoi il existe:** Firmware embarqué et contrôleur pour affichage 7 segments multi-chiffres sur microcontrôleur ESP32.

**Cas d’usage:** Affichage matériel déporté pour métriques ou domotique.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Kotlin | 58.26 |
| C++ | 39.56 |
| C | 2.18 |

## Fonctions et composants

- **Démarrage et connectivité** — setup initialise NVS et vérifie le résultat. Il charge les paramètres enregistrés, tente une connexion et revient à setupWiFi en cas d’échec. Ce parcours sert aussi lorsqu’aucun paramètre n’est sauvegardé.
- **Modules d’affichage et web** — Après la configuration réseau, main.cpp appelle startClockDisplay et setupWebServer. display.cpp, wifi.cpp et web_server.cpp séparent l’affichage matériel, la connexion et le traitement HTTP.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Démarrage ESP32 → Paramètres NVS
- Paramètres NVS → Connexion ou configuration Wi-Fi
- Connexion ou configuration Wi-Fi → Affichage de l’horloge
- Connexion ou configuration Wi-Fi → Interface HTTP

```mermaid
flowchart LR
  n0["Démarrage ESP32"]
  n1["Paramètres NVS"]
  n2["Connexion ou configuration Wi-Fi"]
  n3["Affichage de l’horloge"]
  n4["Interface HTTP"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n2 --> n4
```

**Un parcours dans le code:** Suivez la branche des paramètres sauvegardés dans setup. Le réseau mémorisé est essayé d’abord, mais un échec rejoint setupWiFi. L’affichage et le serveur web démarrent après cette branche.

## Limites et points à vérifier

Le câblage, l’affichage et le Wi-Fi doivent être vérifiés sur le matériel. Cette interface HTTP ne doit pas être supposée sûre pour une exposition Internet libre.

## Fichiers à lire

- [src/main.cpp](https://github.com/antoinebou12/ESP32-7SEG/blob/main/src/main.cpp)
- [src/display.cpp](https://github.com/antoinebou12/ESP32-7SEG/blob/main/src/display.cpp)
- [src/web_server.cpp](https://github.com/antoinebou12/ESP32-7SEG/blob/main/src/web_server.cpp)
- [platformio.ini](https://github.com/antoinebou12/ESP32-7SEG/blob/main/platformio.ini)


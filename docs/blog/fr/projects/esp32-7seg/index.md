# ESP32-7SEG

> Firmware ESP32 et interface web pour un afficheur 7 segments Adafruit — chronomètre, compte à rebours et WiFi.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/esp32-7seg/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/esp32-7seg/index.md
- Publié: 2026-04-13
- Mis à jour: 2026-04-13
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)# ESP32-7SEG

[![GitHub last commit](https://img.shields.io/github/last-commit/antoinebou12/ESP32-7SEG)](https://github.com/antoinebou12/ESP32-7SEG)

[Dépôt](https://github.com/antoinebou12/ESP32-7SEG) · [Licence MIT](https://github.com/antoinebou12/ESP32-7SEG/blob/main/LICENSE)

Firmware pour une carte **ESP32 FireBeetle** qui pilote un **afficheur 7 segments Adafruit** (backpack I2C) et expose une **interface web locale** pour les modes minuteur et la gestion WiFi.

## Interface web

Le serveur intégré sert un panneau **Timer Control** dans le navigateur :

- Modes **chronomètre** et **compte à rebours**
- Raccourcis **10 min**, **5 min**, **1 min**
- Saisie **minutes** et **secondes** manuelle, bouton **Start**
- **Reset WiFi** pour effacer les identifiants stockés et reconfigurer l’appareil

## Matériel

- ESP32 FireBeetle (v1.0)
- Afficheur 7 segments Adafruit avec backpack I2C
- Platine d’essai et fils de liaison (SCL, SDA, VCC, GND)

## Logiciel

- Projet [PlatformIO](https://platformio.org/) ; voir [`platformio.ini`](https://github.com/antoinebou12/ESP32-7SEG/blob/main/platformio.ini) pour la carte et les bibliothèques.
- Le dépôt inclut aussi des sous-projets **Android** et **firmware** pour une stack plus complète autour du même matériel.

## Démarrage rapide

```bash
git clone https://github.com/antoinebou12/ESP32-7SEG.git
cd ESP32-7SEG
```

Ouvrir le projet dans PlatformIO (ou Arduino IDE avec les bibliothèques équivalentes), compiler et flasher l’ESP32. Au démarrage, lire l’adresse IP dans le **moniteur série**, puis l’ouvrir dans un navigateur sur le même réseau pour utiliser l’interface web.

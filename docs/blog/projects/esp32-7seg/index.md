# ESP32-7SEG

> ESP32 firmware and web UI to drive an Adafruit 7-segment display—stopwatch, countdown, and WiFi setup.

- HTML page: https://antoineboucher.info/CV/blog/projects/esp32-7seg/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/esp32-7seg/index.md
- Published: 2026-04-13
- Updated: 2026-04-13
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)# ESP32-7SEG

[![GitHub last commit](https://img.shields.io/github/last-commit/antoinebou12/ESP32-7SEG)](https://github.com/antoinebou12/ESP32-7SEG)

[Repository](https://github.com/antoinebou12/ESP32-7SEG) · [MIT License](https://github.com/antoinebou12/ESP32-7SEG/blob/main/LICENSE)

Firmware for an **ESP32 FireBeetle** that drives an **Adafruit 7-segment display** (I2C backpack) and exposes a **local web interface** for timer modes and WiFi management.

## Web interface

The built-in server serves a **Timer Control** panel in the browser:

- **Stopwatch** and **Countdown** modes
- Quick presets: **10 Min**, **5 Min**, **1 Min**
- Manual **minutes** and **seconds** fields plus **Start**
- **Reset WiFi** to clear stored credentials when you need to re-provision the device

## Hardware

- ESP32 FireBeetle (v1.0)
- Adafruit 7-segment display with I2C backpack
- Breadboard and jumper wires (SCL, SDA, VCC, GND)

## Software

- [PlatformIO](https://platformio.org/) project; see [`platformio.ini`](https://github.com/antoinebou12/ESP32-7SEG/blob/main/platformio.ini) in the repo for board and library configuration.
- The repository also includes **Android** and **firmware** subprojects for a fuller stack around the same device.

## Quick start

```bash
git clone https://github.com/antoinebou12/ESP32-7SEG.git
cd ESP32-7SEG
```

Open the project in PlatformIO (or Arduino IDE with equivalent libraries), build, and flash the ESP32. After boot, check the **serial monitor** for the device IP address, then open it in a browser on the same network to use the web UI.

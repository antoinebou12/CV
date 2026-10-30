---
title: "ESP32-7SEG"
date: 2026-04-13T12:00:00Z
description: "ESP32 firmware and web UI to drive an Adafruit 7-segment display—stopwatch, countdown, and WiFi setup."
draft: false
---

# ESP32-7SEG

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

# ESP32-7SEG: An embedded clock with network setup

> ESP32-7SEG connects an ESP32 clock display to network configuration and an HTTP interface. The firmware startup decides whether saved Wi-Fi settings can…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/esp32-7seg/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/esp32-7seg/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/antoinebou12/ESP32-7SEG
- License: MIT
- Inspected revision: 6cac20eed8dc6293d011a0c8a8341654e0870b80

## Summary

ESP32-7SEG connects an ESP32 clock display to network configuration and an HTTP interface. The firmware startup decides whether saved Wi-Fi settings can be reused or whether the device needs its setup path.

**Why it exists:** Embedded microcontroller firmware and mobile controller for driving multi-digit 7-segment displays.

**Best fit:** Physical computing status dashboards and hardware displays.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Kotlin | 58.26 |
| C++ | 39.56 |
| C | 2.18 |

## Features and components

- **Boot and connectivity** — setup initializes NVS and checks its result. It loads saved credentials, attempts a connection and falls back to setupWiFi if needed. The same fallback runs when no saved credentials exist.
- **Display and web modules** — After connectivity setup, main.cpp calls startClockDisplay and setupWebServer. display.cpp, wifi.cpp and web_server.cpp keep hardware display, connection management and HTTP handling in separate modules.

## Architecture

Components and connections verified in the repository.

- ESP32 boot → NVS saved settings
- NVS saved settings → Connect or setup Wi-Fi
- Connect or setup Wi-Fi → Clock display
- Connect or setup Wi-Fi → HTTP interface

```mermaid
flowchart LR
  n0["ESP32 boot"]
  n1["NVS saved settings"]
  n2["Connect or setup Wi-Fi"]
  n3["Clock display"]
  n4["HTTP interface"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n2 --> n4
```

**One path through the code:** Follow the saved-credentials branch in setup. A stored network is attempted first, but failure still reaches setupWiFi. Only after that branch does the code start the display and web server.

## Constraints and checks

Hardware wiring, display support and Wi-Fi setup must be checked on the device. This HTTP interface should not be assumed safe for unrestricted Internet exposure.

## Files to read

- [src/main.cpp](https://github.com/antoinebou12/ESP32-7SEG/blob/main/src/main.cpp)
- [src/display.cpp](https://github.com/antoinebou12/ESP32-7SEG/blob/main/src/display.cpp)
- [src/web_server.cpp](https://github.com/antoinebou12/ESP32-7SEG/blob/main/src/web_server.cpp)
- [platformio.ini](https://github.com/antoinebou12/ESP32-7SEG/blob/main/platformio.ini)



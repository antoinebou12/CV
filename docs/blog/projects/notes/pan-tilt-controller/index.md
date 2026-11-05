# Pan-Tilt-Controller: Keyboard input to serial motor commands

> This archived pan-tilt controller connects a desktop interface to a serial-controlled positioning unit. The implementation mixes a Qt event loop with…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/pan-tilt-controller/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/pan-tilt-controller/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/antoinebou12/Pan-Tilt-Controller
- Inspected revision: b565efdf9d3fc83096d18c667b6d7a7e21383377

## Summary

This archived pan-tilt controller connects a desktop interface to a serial-controlled positioning unit. The implementation mixes a Qt event loop with pyserial commands and keeps the requested pan and tilt positions in global state.

**Why it exists:** Serial interface and motion control daemon for Directed Perception PTU-46 precision pan-tilt robotic camera units.

**Best fit:** Automated camera positioning for computer vision experiments.

## Use cases

Python 2 desktop and command-line tools that drive a PTU-46-17.5 pan-tilt unit over a serial port.

- **Initialize the unit on start** (PTU-46-17.5 unit): On start, pantiltcontroller.py opens COM3 at 9600 baud and sends speed, acceleration, reset, home position and pan and tilt limit commands (pxu1500, pnu-1000, tnu-850, txu585).
- **Move to a pan/tilt position** (Lab operator, PTU-46-17.5 unit): The PyQt5 window in pantiltcontroller.py has Pan and Tilt fields; OK sends pp<value> and tp<value> and shows the unit's reply in a log box.
- **Jog with arrows or buttons** (Lab operator, PTU-46-17.5 unit): The Control menu (Ctrl+O) opens a dialog whose arrow buttons, and the keyboard arrow keys, move pan or tilt by 5 positions per press.
- **Return to home position** (Lab operator, PTU-46-17.5 unit): The Reset button sends pp0 and tp0 and sets the stored positions back to zero.
- **Send raw serial commands** (Lab operator, PTU-46-17.5 unit): PTC-command.py is a prompt that forwards each typed line (for example r, pnu 1000, pp0) to the unit and prints the reply until exit is typed.

### Scenario: Point the pan-tilt unit at a target

1. Connect the PTU-46-17.5 to COM3 (the port is hard-coded) on a Windows PC with Python 2.7, pyserial, PyQt5 and pywin32.
2. Run python pantiltcontroller.py; the script sets limits and moves the unit to 0,0.
3. Type 500 in Pan and -200 in Tilt, then click OK.
4. Open Control, Control and fine-tune with the arrow keys in steps of 5.
5. Click Reset to bring the unit back to home.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Python | 100 |

## Features and components

- **Interface events** — pantiltcontroller.py imports PyQt5 and installs a key event filter. Arrow keys and buttons adjust a position variable, then build a pp or tp command. This differs from the older framework description in the README.
- **Device initialization** — The module opens COM3 at 9600 baud and writes initialization commands at import time. The UI therefore has an immediate hardware dependency, before a user selects a port or confirms movement.

## Architecture

Components and connections verified in the repository.

- Qt key or button event → Requested position state
- Requested position state → Serial command string
- Serial command string → pyserial connection
- pyserial connection → Pan-tilt hardware

```mermaid
flowchart LR
  n0["Qt key or button event"]
  n1["Requested position state"]
  n2["Serial command string"]
  n3["pyserial connection"]
  n4["Pan-tilt hardware"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
```

**One path through the code:** Follow one arrow-key branch from positionPan or positionTilt to ser.write. The variable records the command target, not independently measured physical position.

## Constraints and checks

Do not import or run this script against attached hardware without reviewing startup motion, travel limits and emergency-stop behavior. It also uses Python 2-era syntax.

## Files to read

- [pantiltcontroller.py](https://github.com/antoinebou12/Pan-Tilt-Controller/blob/master/pantiltcontroller.py)
- [PTC-command.py](https://github.com/antoinebou12/Pan-Tilt-Controller/blob/master/PTC-command.py)
- [README.md](https://github.com/antoinebou12/Pan-Tilt-Controller/blob/master/README.md)



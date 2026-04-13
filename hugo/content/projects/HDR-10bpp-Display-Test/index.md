---
title: "HDR-10bpp-Display-Test"
date: 2024-01-01T12:00:00Z
description: "A test to verify HDR 4K display on Linux with 10-bit color depth."
draft: false
---

## HDR-10bpp-Display-Test

The HDR-10bpp-Display-Test is a simple yet effective way to verify the HDR 4K display capabilities on Linux systems, specifically testing the color depth of 10 bits per channel. This test is essential for anyone looking to ensure the highest quality display performance on their Linux environment.

### Getting Started

[HDR-10bpp-Display-Test](https://github.com/antoinebou12/hdr-10bpp-display-test): A test project for HDR 4K display on Linux.

#### Prerequisites

Before running the test, ensure your system has the following software installed:

- X server
- Python 3
- GTK 3
- ImageJ (for 10-bit color depth image display)
- ImageIO (for reading image files)

On Ubuntu or Debian-based systems, install these packages using the command:

```bash
sudo apt-get install xserver-xorg python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0 imagej
```

#### Installing

ImageIO is a necessary component and can be installed via pip:

```bash
pip3 install imageio
```

#### Running the Test

To conduct the test, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/HDR-10bpp-Display-Test.git
   ```

2. Navigate to the project directory:
   ```bash
   cd HDR-10bpp-Display-Test
   ```

3. Stop the display manager and X server:
   ```bash
   sudo systemctl stop lightdm || sudo systemctl stop gdm
   sudo pkill Xorg
   ```

4. Start the X server with a color depth of 30:
   ```bash
   startx -- -depth 30
   ```

5. Verify the X server's color depth:
   ```bash
   xwininfo -root | grep Depth
   ```

6. Launch the viewer application:
   ```bash
   python3 Viewer.py
   python3 Viewer3.py # for video support
   ```

7. To display an image, use:
   ```bash
   imagej --no-splash /path/to/image
   ```

   Check if the image is displayed correctly with accurate colors.

### Troubleshooting

If the X server fails to start with a color depth of 30, attempt to start it with a depth of 24 instead:

```bash
startx -- -depth 24
```

### License

This project is licensed under the MIT License - see the LICENSE.md file for details.

---

With this setup, the HDR-10bpp-Display-Test project aims to streamline the process of verifying and ensuring optimal display settings on Linux systems, particularly for those requiring high-fidelity visual outputs.

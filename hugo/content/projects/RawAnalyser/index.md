---
title: RawAnalyser
date: 2021-09-06T22:42:23+08:00
description: "Python tool for raw image analysis: clipping, gamma, vignette, and Bayer pixel inspection."
draft: false
---

[here](https://github.com/antoinebou12/RawAnalyser)

# RawAnalyser
RawAnalyser is a simple Python-based tool designed for analyzing raw images. It provides functionality for black and white clipping detection, gamma calculation, and flatness with vignette detection (Algolux). 

## Prerequisites
You need to have Python 2.7 installed and the following libraries:
- json
- time
- numpy
- scipy
- pyqt5
- argparse
- argcomplete
- watchdog
- logging
- colorama
- plotly
- matplotlib

## Usage
1. Run the RawAnalyser script: 
```bash
python RawAnalyser.py <pathfolder> <pointfile> --func <clipping,gamma,vignette,histogram,noHist,basic, default all> --bl <black level, default 1024> --vignette <pathvignette>
```
2. Start the GUI:
```bash
python GUI.py
```
3. Check the value of the pixel and the color with the bayer pattern:
```bash
python RawPixel.pt input<file> x y  --bitdepth <8,10,16,default 16>
```

## Scripts Description

### RawAnalyser.py
A script designed for checking black and white level of clipping in a raw image. You need to provide a path to the folder to be checked and a json file with the region of interest and the gray patches.

#### points.json
The JSON file specifying the region of interest. An example of its structure is as follows:
```json
{
    "last_y": 798,
    "last_x": 1353,
    "gray_first_y": 691,
    "gray_first_x": 606,
    "first_x": 603,
    "first_y": 315,
    "gray_last_x": 1347,
    "gray_last_y": 795
}
```

### GUI.py
A GUI script for image selection. It allows you to select the region of interest and the gray patches in a raw or TIFF file, which are then saved in a JSON file. It also constantly checks for new files in the raw folder.

### RawPixel.py
A script to inspect the value of a specific pixel and determine its color using the Bayer pattern.

### 20MPto5MP.py
A script for converting 20-megapixel images to 5-megapixel images, specifically designed for the new OV20880 sensor.

#### Camera
Example of camera sensor information:

```text
Camera: OV2740
Resolution: (1088, 1928)
ImageType: BINARY16U
Sensor value: 10 bit
Bayer pattern: 'bggr'
```

This tool provides a simple and efficient way to analyze raw images, making it a vital part of any image processing workflow.

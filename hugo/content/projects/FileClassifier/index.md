---
title: File Classifier
date: 2021-09-06T22:42:23+08:00
description: "Python CLI that organizes files into categories by type, with optional topic modeling."
draft: false
---

# FileClassifier

FileClassifier is a Python CLI that organizes files in a directory into categories by type (images, documents, videos, and so on). An extendable classifier can add topic modeling.

## Features

- Automatic file organization based on file types.
- Predefined categories for common file formats.
- Extendable classifier with topic modeling support.
- Customizable output directory structure.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/antoinebou12/FileClassifier.git
cd FileClassifier
pip install poetry
poetry install
```

## Usage

To use FileClassifier, navigate to the project directory and run the `main.py` script with the required arguments:

```bash
python main.py [OPTIONS] INPUT_DIRECTORY OUTPUT_DIRECTORY
```

### Arguments

- `INPUT_DIRECTORY`: The directory containing the files to be organized.
- `OUTPUT_DIRECTORY`: The directory where the organized files will be moved to.

### Options

- `--version`: Show the version and exit.
- `--types`: List supported file types and their categories.
- `--topic-modeling`: Enable topic modeling (requires additional setup).

### Example

```bash
python main.py /path/to/input /path/to/output
```

This command will organize the files in `/path/to/input` and move them to the appropriate folders in `/path/to/output`.

## Extending the Classifier

To add topic modeling to the classifier, you need to modify the `Classifier.py` script and install additional dependencies. Please refer to the script comments and the provided documentation for more information on how to implement topic modeling.

## License

MIT License. See the `LICENSE` file.

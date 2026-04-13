---
title: File Classifier
date: 2021-09-06T22:42:23+08:00
description: "Python CLI that organizes files into categories by type, with optional topic modeling."
draft: false
---

# FileClassifier

FileClassifier is a Python-based command-line tool that automatically organizes files in a specified directory into predefined categories based on their file types. The tool supports multiple file formats, such as images, documents, videos, and more. It also comes with an extendable classifier that allows you to add topic modeling for better organization.

## Features

- Automatic file organization based on file types.
- Predefined categories for common file formats.
- Extendable classifier with topic modeling support.
- Customizable output directory structure.
- Lightweight and easy to use.

## Installation

To install FileClassifier, simply clone the repository and install the required dependencies:

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
- `--topic-modeling`: Enable topic modeling for better organization (requires additional setup).

### Example

```bash
python main.py /path/to/input /path/to/output
```

This command will organize the files in `/path/to/input` and move them to the appropriate folders in `/path/to/output`.

## Extending the Classifier

To add topic modeling to the classifier, you need to modify the `Classifier.py` script and install additional dependencies. Please refer to the script comments and the provided documentation for more information on how to implement topic modeling.

## Contributing

Contributions are welcome! If you would like to contribute to FileClassifier, please submit a pull request or open an issue with your ideas and suggestions.

## License

FileClassifier is released under the MIT License. See the `LICENSE` file for more information.

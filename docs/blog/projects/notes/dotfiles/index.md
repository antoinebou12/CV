# .dotfiles: A shell environment in scripts

> These dotfiles collect the shell and editor setup I used across machines. The interesting part is the installer: it turns a set of personal preferences…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/dotfiles/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/dotfiles/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Repository: https://github.com/antoinebou12/.dotfiles
- License: MIT
- Inspected revision: 52ff3c19bdebfbebf1d9e320fff199044bdf5e13

## Summary

These dotfiles collect the shell and editor setup I used across machines. The installer manages packages, configuration files and upstream projects.

**Why it exists:** Idempotent multi-distribution installer supporting apt, dnf, pacman with modular Zsh and Vim configurations.

**Best fit:** Reproducible shell and developer environment across macOS and Linux servers.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Shell | 100 |

## Getting started (repository commands, not run here)

### README.md · Installation

```bash
bash install.sh
source install.sh
install_vimrc
```


## Features and components

- **Package installation** — install.sh reads the distribution from /etc/os-release, then selects apt, pacman, dnf or yum. exec_root wraps commands that need elevated privileges. Package installation and configuration changes therefore share one script.
- **Editor and shell setup** — The Vim path installs amix/vimrc and applies local changes, including line numbers and the file-tree position. Other functions install Oh My Zsh. update.sh and uninstall.sh are separate maintenance entry points.

## Architecture

Components and connections verified in the repository.

- install.sh → Distribution detection
- Distribution detection → System packages
- System packages → Vim and Zsh configuration

```mermaid
flowchart LR
  n0["install.sh"]
  n1["Distribution detection"]
  n2["System packages"]
  n3["Vim and Zsh configuration"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
```

**One path through the code:** Follow install_vimrc from its package request to the upstream clone, then to the edits in ~/.vim_runtime. This shows which files the installer owns and which belong to another project.

## Constraints and checks

The script edits home-directory files and runs privileged package commands. Back up existing configuration and inspect each function before running it on a current machine.

## Files to read

- [install.sh](https://github.com/antoinebou12/.dotfiles/blob/main/install.sh)
- [update.sh](https://github.com/antoinebou12/.dotfiles/blob/main/update.sh)
- [uninstall.sh](https://github.com/antoinebou12/.dotfiles/blob/main/uninstall.sh)


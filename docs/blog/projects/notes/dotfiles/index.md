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

## Use cases

Bash scripts that install, update and remove a Linux shell setup: vimrc, Oh My Zsh, tmux and dev tools.

- **Install the vimrc setup** (Developer, Upstream projects): install_vimrc in install.sh installs vim and git, clones amix/vimrc into ~/.vim_runtime and runs its installer; edit_vimrc moves NERDTree to the left and turns on line numbers.
- **Set up Oh My Zsh and tmux** (Developer, Upstream projects): install_oh_my_zsh downloads the official Oh My Zsh installer with wget; edit_oh_my_zsh switches the theme and writes a minimal prompt theme; install_tmux writes a full ~/.tmux.conf.
- **Install dev toolchains** (Developer, OS package manager): bash install.sh <option> runs one installer (Python, JDK, nvm, .NET, Go, Rust, Docker, kubectl, AWS CLI, Azure CLI, JupyterLab, network tools); install_package reads /etc/os-release to pick apt-get, pacman, dnf, yum or brew.
- **Update the scripts and vimrc** (Developer, Upstream projects): update.sh defines update_install_script (git pull, then bash install.sh) and update_vimrc (git pull --rebase in ~/.vim_runtime, then update_plugins.py); the file only defines them, so it is meant to be sourced.
- **Remove tools with backups** (Developer, OS package manager): uninstall.sh copies ~/.vimrc and ~/.tmux.conf to .backup files before deleting them, and purges JDK, Python, Rust, Go, Jupyter, AWS CLI, Azure CLI and nvm; run with bash, it calls every uninstall function in turn.
- **Show neofetch at login** (Developer, OS package manager): motd/motd.sh installs neofetch with apt-get when missing and writes /etc/update-motd.d/10-neofetch so the system summary appears in the login banner.

### Scenario: Set up a fresh Ubuntu machine

1. Clone the repository and run bash install.sh with no option to print the usage() list.
2. Run bash install.sh install_vimrc to install vim and git and clone amix/vimrc into ~/.vim_runtime.
3. Run bash install.sh install_oh_my_zsh, then install_tmux, to get zsh and a written ~/.tmux.conf.
4. Run bash install.sh install_docker; it fetches get.docker.com and Docker Compose 1.29.2.
5. On a server, run motd/motd.sh as root so neofetch shows at each SSH login.

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



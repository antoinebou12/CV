# another-install-script: A menu for homelab installation

> another-install-script is a shell entry point for choosing system setup and container installations. Its structure separates the menu from the service…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/another-install-script/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/another-install-script/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/antoinebou12/another-install-script
- License: GPL-3.0
- Inspected revision: 6e1e193260504106593f6b92bb799aacafdf0e2b

## Summary

another-install-script is a shell entry point for choosing system setup and container installations. Its structure separates the menu from the service definitions so that adding a service does not require putting every command in setup.sh.

**Why it exists:** Interactive TUI shell installer automating deployment of Docker containers and server configurations.

**Best fit:** One-command server provisioning for homelabs and development VPS.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Shell | 93.8 |
| Dockerfile | 3.12 |
| Python | 3.07 |

## Getting started (repository commands, not run here)

### README.md · How to install

```bash
git clone https://github.com/antoinebou13/another-install-script.git
cd another-install-script
sudo bash setup.sh
```

### README.md · Project Structure

```bash
+-- docs
|   +-- vendor
|       +-- ...
|   +-- docs.md
|   +-- generate_docs.md
|   +-- ...
+-- containers
|   +-- $container_name
|   |   |   +-- docker-compose.yml
|   |   |   +-- $container_name.sh
|   |   |   +-- ...
+-- src
```

### README.md · How to run coverage and tests

```bash
cd tests
bash test.sh
```

### README.md · How to run coverage and tests

```bash
cd tests
bash coverage.sh
```

### README.md · How to generate the documentation

```bash
git submodule update --init --recursive
git pull --recurse-submodules
git submodule update --remote
cd docs/generator
chmod +x generate_docs.sh
bash generate_docs.sh ../docs.md
```


## Features and components

- **Entry point and menus** — setup.sh sources src/menu.sh and calls main_setup_menu. The root script handles arguments, while the sourced module controls navigation. config.yml sits beside the launcher as the project’s configuration surface.
- **Service definitions** — The containers directory holds installation material for individual services. Keeping that material outside the menu makes the repository easier to extend, but each installation still changes the host or its Docker environment.

## Architecture

Components and connections verified in the repository.

- setup.sh → src/menu.sh
- src/menu.sh → Configuration and selection
- Configuration and selection → Container installation

```mermaid
flowchart LR
  n0["setup.sh"]
  n1["src/menu.sh"]
  n2["Configuration and selection"]
  n3["Container installation"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
```

**One path through the code:** Start with the main_setup_menu call, then inspect the selected service under containers before executing it. The menu is a dispatcher; the selected service determines the actual side effects.

## Constraints and checks

The README calls this a work in progress and records testing on an older Ubuntu release. Those notes do not establish compatibility with a current server.

## Files to read

- [setup.sh](https://github.com/antoinebou12/another-install-script/blob/master/setup.sh)
- [src/menu.sh](https://github.com/antoinebou12/another-install-script/blob/master/src/menu.sh)
- [config.yml](https://github.com/antoinebou12/another-install-script/blob/master/config.yml)



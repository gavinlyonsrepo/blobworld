# Blob World

[![Website](https://img.shields.io/badge/Website-Link-blue.svg)](https://gavinlyonsrepo.github.io/)  [![Rss](https://img.shields.io/badge/Subscribe-RSS-yellow.svg)](https://gavinlyonsrepo.github.io//feed.xml)  [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/paypalme/whitelight976)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)] [![pygame](https://img.shields.io/badge/pygame-2.1%2B-green)] [![PyPI](https://img.shields.io/pypi/v/blobworld)]

## Description

A pygame blob survival game written in Python 3.
Guide your blue blob through 10 levels of increasing difficulty.

![title screen](https://raw.githubusercontent.com/gavinlyonsrepo/blobworld/master/blobworld/assets/images/title.jpg)

## File System

| Path | Purpose |
| ------ | --------- |
| `~/.config/blobworld/config.ini` | User configuration file — created on first run with defaults. Edit with any text editor to change screen resolution, player speed, volume, and more. Delete to restore defaults. |
| `~/.local/share/blobworld/scores.db` | SQLite highscore database — stores the top 10 scores with name, score, level reached, and time played. |
| `~/.local/share/icons/blobworld.png` | Desktop icon (installed via in-game DESKTOP menu) |
| `~/.local/share/applications/blobworld.desktop` | Desktop entry (installed via in-game DESKTOP menu) |

### Desktop entry

A desktop entry and icon can be installed from the **DESKTOP** option in the
main menu. This requires `curl` and a network connection to download the files
from GitHub. Once installed the game will appear in your application launcher.

## Dependencies

| Package | Purpose |
| --------- | --------- |
| [pygame](https://www.pygame.org/) >= 2.1 | Game engine — display, input, audio |
| [numpy](https://numpy.org/) | Collision distance calculations |

---

## Installation

### From PyPI (recommended)

```bash
pip install blobworld
```

### From source

```bash
git clone https://github.com/gavinlyonsrepo/blobworld
cd blobworld
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

> **Note:** On newer Linux distributions (Ubuntu 23.04+, Fedora 38+) the system
> Python is externally managed. Always install inside a virtual environment.

---

## How to Run

```bash
blobworld
```

Or if running from source without installing:

```bash
python -m blobworld.main
```

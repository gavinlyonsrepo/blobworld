"""
config.py — User configuration via ~/.config/blobworld/config.ini

On first run a default config file is written to disk.
Users can edit it with any text editor between sessions.
Call config.load() once at startup before pygame initialises.
"""

from __future__ import annotations

import configparser
import pathlib

import blobworld.settings as cfg

# Location of the user config file
_CONFIG_DIR  = pathlib.Path.home() / ".config" / "blobworld"
_CONFIG_PATH = _CONFIG_DIR / "config.ini"


# Default values — mirrors settings.py, used when writing a fresh config
_DEFAULTS: dict[str, dict[str, str]] = {
    "display": {
        "# screen resolution": "",
        "screen_w":   str(cfg.SCREEN_W),
        "screen_h":   str(cfg.SCREEN_H),
        "fps":        str(cfg.FPS),
        "fullscreen": str(cfg.FULLSCREEN).lower(),
    },
    "gameplay": {
        "# Difficult level, easy medium or hard": "",
        "difficulty":    str(cfg.DEFAULT_DIFFICULTY),
    },
    "audio": {
        "# volume range 0.0 to 1.0": "",
        "music_volume": "0.5",
        "sfx_volume":   "0.8",
    },
}

# === Public API ===

def load() -> None:
    """
    Read the user config file and patch settings.py values in-place.
    Creates the file with defaults if it does not exist.
    """
    if not _CONFIG_PATH.exists():
        _write_defaults()

    parser = configparser.ConfigParser(inline_comment_prefixes=("#",))
    parser.read(_CONFIG_PATH)

    # --- display ---
    display = parser["display"] if "display" in parser else {}
    cfg.SCREEN_W   = int(display.get("screen_w",   cfg.SCREEN_W))
    cfg.SCREEN_H   = int(display.get("screen_h",   cfg.SCREEN_H))
    cfg.FPS        = int(display.get("fps",         cfg.FPS))
    cfg.FULLSCREEN = display.get("fullscreen", str(cfg.FULLSCREEN)).lower() == "true"

    # --- gameplay ---
    gameplay = parser["gameplay"] if "gameplay" in parser else {}
    cfg.DEFAULT_DIFFICULTY = gameplay.get("difficulty", str(cfg.DEFAULT_DIFFICULTY)).lower()

    # --- audio ---
    audio = parser["audio"] if "audio" in parser else {}
    cfg.MUSIC_VOLUME = float(audio.get("music_volume", 0.5))
    cfg.SFX_VOLUME   = float(audio.get("sfx_volume",   0.8))

    _apply_difficulty()


def config_path() -> pathlib.Path:
    """Return the path to the active config file (useful for logging)."""
    return _CONFIG_PATH

# Internal helpers

def _apply_difficulty() -> None:
    """Patch gameplay settings based on the chosen difficulty level."""
    d = cfg.DEFAULT_DIFFICULTY

    if d == cfg.DIFFICULT_LEVELS[0]:
        cfg.PLAYER_SPEED          = 4.3
        cfg.YELLOW_FREEZE_SECONDS = 12.0
        cfg.WHITE_SHRINK          = 5
        cfg.SCORE_PER_GREEN       = 3
    elif d == cfg.DIFFICULT_LEVELS[1]:
        cfg.PLAYER_SPEED          = 4.2
        cfg.YELLOW_FREEZE_SECONDS = 6.0
        cfg.WHITE_SHRINK          = 6
        cfg.SCORE_PER_GREEN       = 6
    elif d == cfg.DIFFICULT_LEVELS[2]:
        cfg.PLAYER_SPEED          = 4.1
        cfg.YELLOW_FREEZE_SECONDS = 3.0
        cfg.WHITE_SHRINK          = 7
        cfg.SCORE_PER_GREEN       = 10
    else:
        print(f"[config] unknown difficulty '{d}', defaulting to easy")
        print(cfg.DIFFICULT_LEVELS)
        cfg.DEFAULT_DIFFICULTY    = "easy"
        _apply_difficulty()

def _write_defaults() -> None:
    """Write a commented default config file to disk."""
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    lines: list[str] = [
        "# Blob World configuration",
        "# Edit this file to customise the game.",
        "# Delete it to restore all defaults.",
        "",
    ]

    for section, keys in _DEFAULTS.items():
        lines.append(f"[{section}]")
        for key, value in keys.items():
            if key.startswith("#"):
                lines.append(key)          # comment line
            elif value == "":
                pass                       # skip blank sentinel
            else:
                lines.append(f"{key} = {value}")
        lines.append("")

    _CONFIG_PATH.write_text("\n".join(lines))
    print(f"[blobworld] config created at {_CONFIG_PATH}")

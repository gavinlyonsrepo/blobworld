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
        "# blob counts (fixed pools)": "",
        "green_count":          str(cfg.GREEN_COUNT),
        "red_count":            str(cfg.RED_COUNT),
        "purple_count":         str(cfg.PURPLE_COUNT),
        "# player settings": "",
        "player_speed":         str(cfg.PLAYER_SPEED),
        "# how much purple shrinks the player per touch": "",
        "purple_shrink":        str(cfg.PURPLE_SHRINK),
        "# seconds reds are frozen after catching yellow": "",
        "yellow_freeze_seconds": str(cfg.YELLOW_FREEZE_SECONDS),
        "# scoring": "",
        "score_per_green":      str(cfg.SCORE_PER_GREEN),
        "score_per_yellow":     str(cfg.SCORE_PER_YELLOW),
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
    cfg.GREEN_COUNT           = int(gameplay.get("green_count",            cfg.GREEN_COUNT))
    cfg.RED_COUNT             = int(gameplay.get("red_count",              cfg.RED_COUNT))
    cfg.PURPLE_COUNT          = int(gameplay.get("purple_count",           cfg.PURPLE_COUNT))
    cfg.PLAYER_SPEED          = float(gameplay.get("player_speed",         cfg.PLAYER_SPEED))
    cfg.PURPLE_SHRINK         = float(gameplay.get("purple_shrink",        cfg.PURPLE_SHRINK))
    cfg.YELLOW_FREEZE_SECONDS = float(gameplay.get("yellow_freeze_seconds",cfg.YELLOW_FREEZE_SECONDS))
    cfg.SCORE_PER_GREEN       = int(gameplay.get("score_per_green",        cfg.SCORE_PER_GREEN))
    cfg.SCORE_PER_YELLOW      = int(gameplay.get("score_per_yellow",       cfg.SCORE_PER_YELLOW))

    # --- audio ---
    audio = parser["audio"] if "audio" in parser else {}
    cfg.MUSIC_VOLUME = float(audio.get("music_volume", 0.5))
    cfg.SFX_VOLUME   = float(audio.get("sfx_volume",   0.8))


def config_path() -> pathlib.Path:
    """Return the path to the active config file (useful for logging)."""
    return _CONFIG_PATH

# Internal helpers

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

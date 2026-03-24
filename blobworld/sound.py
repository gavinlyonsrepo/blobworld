"""
 sound.py — All audio: sound effects and menu music
 Call sound.init() once after pygame.init().
 Then use sound.play("name") anywhere in the codebase.
 All errors are silently swallowed so missing files never crash the game.
"""

# pylint: disable=broad-exception-caught

from __future__ import annotations

import pygame
from blobworld.settings import asset, MUSIC_VOLUME, SFX_VOLUME

# Internal sound registry — loaded once at init
_sounds: dict[str, pygame.mixer.Sound] = {}


def init() -> None:
    """Initialise the mixer and load all sound effects."""
    try:
        pygame.mixer.init()
    except Exception as e:
        print(f"[sound] mixer init failed: {e}")
        return

    _load("pause",        "pause.wav")
    _load("start",        "start.wav")
    _load("end",          "end.wav")
    _load("eat_green",    "eat_green.wav")
    _load("eat_yellow",   "eat_yellow.wav")
    _load("eat_purple",   "eat_purple.wav")
    _load("level_end",    "level_end.wav")
    _load("eaten_by_red", "eaten_by_red.wav")

    # Apply sfx volume to all loaded sounds
    for s in _sounds.values():
        s.set_volume(SFX_VOLUME)


def _load(name: str, filename: str) -> None:
    """Load a sound effect into the registry."""
    try:
        _sounds[name] = pygame.mixer.Sound(asset("sounds", filename))
    except Exception as e:
        print(f"[sound] could not load '{filename}': {e}")


def play(name: str) -> None:
    """Play a sound effect by name. Silently ignores unknown names."""
    s = _sounds.get(name)
    if s:
        s.play()


def play_music(filename: str, loops: int = -1) -> None:
    """
    Load and play background music.
    loops=-1 means loop forever.
    Supports .ogg and .mp3 (ogg preferred on Linux).
    """
    try:
        pygame.mixer.music.load(asset("sounds", filename))
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(loops)
    except Exception as e:
        print(f"[sound] could not play music '{filename}': {e}")


def stop_music() -> None:
    """Stop background music playback."""
    try:
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"[sound] could not stop music : {e}")


def set_sfx_volume(volume: float) -> None:
    """Set volume for all sound effects (0.0–1.0)."""
    for s in _sounds.values():
        s.set_volume(max(0.0, min(1.0, volume)))


def set_music_volume(volume: float) -> None:
    """Set background music volume (0.0–1.0)."""
    try:
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
    except Exception as e:
        print(f"[sound] could set music volume: {e}")

"""
  settings.py — All game constants and configuration
  Speeds and counts are defined per-level in levels.py
"""
import pathlib
import importlib.resources as _pkg

# --- Display ---
SCREEN_W: int = 1280
SCREEN_H: int = 720
FPS: int = 60
TITLE: str = "Blob World"
FULLSCREEN: bool = False

# --- Game play ---
DIFFICULT_LEVELS = ("easy", "medium" , "hard")
DEFAULT_DIFFICULTY = "easy"

# --- Colours (R, G, B) ---
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
DARK_BG    = (15,  15,  30)
HUD_COLOUR = (200, 200, 220)

COLOUR_PLAYER = (80,  140, 255)
COLOUR_GREEN  = (60,  210, 90)
COLOUR_RED    = (220, 50,  50)
COLOUR_PURPLE = (160, 60,  220)
COLOUR_YELLOW = (240, 210, 40)
COLOUR_ORANGE = (255,140,0)

# --- Blob sizes ---
BLOB_MIN_RADIUS: int    = 6
BLOB_MAX_RADIUS: int    = 30

PLAYER_START_RADIUS: int = 12
GREEN_START_RADIUS: int  = 10
RED_START_RADIUS: int    = 11
PURPLE_START_RADIUS: int = 13
ORANGE_START_RADIUS: int = 15
YELLOW_START_RADIUS: int = 8
WHITE_START_RADIUS: int = 8

# --- Player ---
PLAYER_SPEED: float = 4.0

# --- Purple ---
PURPLE_SPEED_MIN: float  = 1.0
PURPLE_SPEED_MAX: float  = 2.0
PURPLE_SHRINK: float     = 3.0

# --- Orange ---
ORANGE_SPEED_MIN: float  = 0.1
ORANGE_SPEED_MAX: float  = 1.0
ORANGE_EXPAND: float     = 3.0

# --- Fixed counts ---
GREEN_COUNT: int  = 15
RED_COUNT: int = 5
PURPLE_COUNT: int = 4
ORANGE_COUNT: int = 2
YELLOW_COUNT: int = 1
WHITE_COUNT: int = 1

# --- Flee / chase detection radii ---
FLEE_RADIUS: float  = 180.0
CHASE_RADIUS: float = 300.0

# --- Collision ---
COLLISION_THRESHOLD: float = 0.85

# --- Red clustering ---
CLUSTER_RADIUS: float = 80.0
CLUSTER_FORCE: float  = 0.08

# --- bonus ---
YELLOW_FREEZE_SECONDS: float = 3.0
WHITE_SHRINK: int = 5

# --- Scoring ---
SCORE_PER_GREEN: int  = 10

# --- Levels ---
TOTAL_LEVELS: int = 10

# --- Highscores ---
DB_DIR  = pathlib.Path.home() / ".local" / "share" / "blobworld"
DB_PATH = DB_DIR / "scores.db"
MAX_HIGH_SCORES: int = 10

# --- Audio ---
MUSIC_VOLUME: float = 0.5
SFX_VOLUME: float   = 0.8

# --- Assets ---
_ASSETS = _pkg.files("blobworld") / "assets"

def asset(subfolder: str, filename: str) -> str:
    """ aquire global asset path for given asset """
    return str(_ASSETS / subfolder / filename)

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

# --- Blob sizes ---
BLOB_MIN_RADIUS: int    = 8
BLOB_MAX_RADIUS: int    = 32

PLAYER_START_RADIUS: int = 12
GREEN_START_RADIUS: int  = 10
RED_START_RADIUS: int    = 11
PURPLE_START_RADIUS: int = 14
YELLOW_START_RADIUS: int = 9

# --- Player ---
PLAYER_SPEED: float = 4.0

# --- Purple ---
PURPLE_SPEED_MIN: float  = 1.0
PURPLE_SPEED_MAX: float  = 2.0
PURPLE_SHRINK: float     = 3.0
PLAYER_MIN_RADIUS: float = 6.0

# --- Fixed counts ---
GREEN_COUNT: int  = 15
RED_COUNT: int = 5
PURPLE_COUNT: int = 4
YELLOW_COUNT: int = 1

# --- Flee / chase detection radii ---
FLEE_RADIUS: float  = 180.0
CHASE_RADIUS: float = 300.0

# --- Collision ---
COLLISION_THRESHOLD: float = 0.85

# --- Red clustering ---
CLUSTER_RADIUS: float = 80.0    # reds attract each other within this distance
CLUSTER_FORCE: float  = 0.08    # cohesion pull strength

# --- Yellow bonus ---
YELLOW_FREEZE_SECONDS: float = 3.0

# --- Scoring (per level total = 100) ---
SCORE_PER_GREEN: int  = 5       # 15 x 5  = 75
SCORE_PER_YELLOW: int = 25      # 1  x 25 = 25  → total 100 per level x 10 = 1000

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

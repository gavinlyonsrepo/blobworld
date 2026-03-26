"""
    levels.py — Configuration for all 10 levels

    Difficulty increases each level:
    - greens and yellow get faster
    - more red enemies, moving faster

    Points per level = 100 (15 greens x 5 = 75, 1 yellow x 25 = 25)
    Total across all 10 levels = 1000
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class LevelConfig:
    """ Class to generate levels """
    level: int

    # Green blob speeds
    green_speed_min: float
    green_speed_max: float
    green_flee_speed: float

    # Yellow blob speeds
    yellow_speed_min: float
    yellow_speed_max: float
    yellow_flee_speed: float

    # Red blob counts and speeds
    red_count: int
    red_speed_min: float
    red_speed_max: float
    red_chase_speed: float


# fmt: off
LEVELS: list[LevelConfig] = [
    LevelConfig(level=1,
        green_speed_min=1.2,  green_speed_max=1.8,  green_flee_speed=3.0,
        yellow_speed_min=2.0, yellow_speed_max=3.0, yellow_flee_speed=4.0,
        red_count=2, red_speed_min=1.2, red_speed_max=1.6, red_chase_speed=1.8),

    LevelConfig(level=2,
        green_speed_min=1.3,  green_speed_max=2.0,  green_flee_speed=3.1,
        yellow_speed_min=2.2, yellow_speed_max=3.0, yellow_flee_speed=4.2,
        red_count=2, red_speed_min=1.3, red_speed_max=1.7, red_chase_speed=2.0),

    LevelConfig(level=3,
        green_speed_min=1.4,  green_speed_max=2.1,  green_flee_speed=3.2,
        yellow_speed_min=2.7, yellow_speed_max=3.1, yellow_flee_speed=4.3,
        red_count=2, red_speed_min=1.4, red_speed_max=1.8, red_chase_speed=2.2),

    LevelConfig(level=4,
        green_speed_min=1.4,  green_speed_max=2.2,  green_flee_speed=3.3,
        yellow_speed_min=3.0, yellow_speed_max=3.2, yellow_flee_speed=4.4,
        red_count=3, red_speed_min=1.5, red_speed_max=1.9, red_chase_speed=2.3),

    LevelConfig(level=5,
        green_speed_min=1.6,  green_speed_max=2.3,  green_flee_speed=3.4,
        yellow_speed_min=3.1, yellow_speed_max=3.3, yellow_flee_speed=4.5,
        red_count=3, red_speed_min=1.6, red_speed_max=2.0, red_chase_speed=2.4),

    LevelConfig(level=6,
        green_speed_min=1.7,  green_speed_max=2.4,  green_flee_speed=3.6,
        yellow_speed_min=3.2, yellow_speed_max=3.4, yellow_flee_speed=4.6,
        red_count=3, red_speed_min=2.0, red_speed_max=2.1, red_chase_speed=2.5),

    LevelConfig(level=7,
        green_speed_min=1.8,  green_speed_max=2.5,  green_flee_speed=3.7,
        yellow_speed_min=3.2, yellow_speed_max=4.0, yellow_flee_speed=4.7,
        red_count=4, red_speed_min=2.0, red_speed_max=2.4, red_chase_speed=2.6),

    LevelConfig(level=8,
        green_speed_min=1.9,  green_speed_max=2.6,  green_flee_speed=3.9,
        yellow_speed_min=3.3, yellow_speed_max=4.1, yellow_flee_speed=5.0,
        red_count=4, red_speed_min=2.0, red_speed_max=2.6, red_chase_speed=2.7),

    LevelConfig(level=9,
        green_speed_min=2.0,  green_speed_max=2.6,  green_flee_speed=4.0,
        yellow_speed_min=3.3, yellow_speed_max=4.3, yellow_flee_speed=5.1,
        red_count=4, red_speed_min=2.0, red_speed_max=2.7, red_chase_speed=2.8),

    LevelConfig(level=10,
        green_speed_min=2.0,  green_speed_max=2.7,  green_flee_speed=4.1,
        yellow_speed_min=3.5, yellow_speed_max=4.4, yellow_flee_speed=5.3,
        red_count=5, red_speed_min=2.0, red_speed_max=2.8, red_chase_speed=2.9),
]
# fmt: on


def get_level(n: int) -> LevelConfig:
    """Return config for level n (1-indexed). Clamps to valid range."""
    return LEVELS[max(0, min(n - 1, len(LEVELS) - 1))]


TOTAL_LEVELS: int = len(LEVELS)

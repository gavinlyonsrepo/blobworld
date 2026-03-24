"""
    highscores.py — SQLite highscore persistence
    Schema: name, score, level_reached, time_seconds, date
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime

from blobworld import settings as cfg


@dataclass
class ScoreEntry:
    """ dataclass to store high score details"""
    name:          str
    score:         int
    level_reached: int
    time_seconds:  float
    date:          str
    rank:          int = 0

    @property
    def time_display(self) -> str:
        """Format seconds as M:SS"""
        m, s = divmod(int(self.time_seconds), 60)
        return f"{m}:{s:02d}"


def _connect() -> sqlite3.Connection:
    cfg.DB_DIR.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(cfg.DB_PATH)


def init_db() -> None:
    """ init the highscores database, create if it does not exist """
    with _connect() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT    NOT NULL,
                score         INTEGER NOT NULL,
                level_reached INTEGER NOT NULL DEFAULT 1,
                time_seconds  REAL    NOT NULL DEFAULT 0,
                date          TEXT    NOT NULL
            )
        """)



def save_score(name: str, score: int,
               level_reached: int = 1, time_seconds: float = 0.0) -> None:
    """ Save the high score to the data base """
    name = name.strip()[:16] or "PLAYER"
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    with _connect() as con:
        con.execute(
            "INSERT INTO scores (name, score, level_reached, time_seconds, date) "
            "VALUES (?, ?, ?, ?, ?)",
            (name, score, level_reached, time_seconds, date),
        )
        con.execute("""
            DELETE FROM scores WHERE id NOT IN (
                SELECT id FROM scores ORDER BY score DESC LIMIT ?
            )
        """, (cfg.MAX_HIGH_SCORES,))


def get_top_scores(limit: int = cfg.MAX_HIGH_SCORES) -> list[ScoreEntry]:
    """ Read the high scores database for display """
    with _connect() as con:
        rows = con.execute(
            "SELECT name, score, level_reached, time_seconds, date "
            "FROM scores ORDER BY score DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [
        ScoreEntry(name=r[0], score=r[1], level_reached=r[2],
                   time_seconds=r[3], date=r[4], rank=i + 1)
        for i, r in enumerate(rows)
    ]


def is_high_score(score: int) -> bool:
    """ detect if a score makes it to the database table"""
    entries = get_top_scores()
    if len(entries) < cfg.MAX_HIGH_SCORES:
        return True
    return score > entries[-1].score

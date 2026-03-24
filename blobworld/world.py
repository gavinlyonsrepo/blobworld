"""
world.py — Game world: level management, spawning, collision resolution
"""

from __future__ import annotations

import time

import pygame

from blobworld import settings as cfg
from blobworld import sound
from blobworld.levels import get_level, TOTAL_LEVELS
from blobworld.blob import PlayerBlob, GreenBlob, RedBlob, PurpleBlob, YellowBlob


class World:
    """Owns all blobs and drives the simulation. Manages level progression."""

    def __init__(self) -> None:
        self.current_level: int  = 1
        self.total_score:   int  = 0
        self.game_over:     bool = False
        self.won:           bool = False
        self.final_score:   int  = 0
        self.level_start_time: float = time.time()
        self.total_time:    float = 0.0
        self._total_score_at_level_start: int = 0
        self.greens:  list[GreenBlob]  = []
        self.reds:    list[RedBlob]    = []
        self.purples: list[PurpleBlob] = []
        self.yellows: list[YellowBlob] = []
        self._advance_pending: bool = False
        self._load_level(self.current_level)

    def _load_level(self, n: int) -> None:
        lv = get_level(n)
        self.player  = PlayerBlob()
        self.greens  : list[GreenBlob]  = [GreenBlob(lv)  for _ in range(cfg.GREEN_COUNT)]
        self.reds    : list[RedBlob]    = [RedBlob(lv)    for _ in range(lv.red_count)]
        self.purples : list[PurpleBlob] = [PurpleBlob()   for _ in range(cfg.PURPLE_COUNT)]
        self.yellows : list[YellowBlob] = [YellowBlob(lv) for _ in range(cfg.YELLOW_COUNT)]
        self._purple_cooldown: dict[int, int] = {}
        self._advance_pending: bool = False
        self.level_start_time = time.time()

    # Level queries

    @property
    def greens_remaining(self) -> int:
        """Return number of alive green blobs."""
        return sum(1 for g in self.greens if g.alive)

    @property
    def elapsed_this_level(self) -> float:
        """Return elapsed time (seconds) for current level."""
        return time.time() - self.level_start_time

    def update(self) -> None:
        """ Update the level"""
        if self.game_over:
            return
        p = self.player
        p.update()
        alive_reds = [r for r in self.reds if r.alive]
        for g in self.greens:
            if g.alive:
                g.update(player=p)
        for r in alive_reds:
            r.update(player=p, peers=alive_reds)
        for pu in self.purples:
            if pu.alive:
                pu.update(player=p)
        for y in self.yellows:
            if y.alive:
                y.update(player=p)

        self._resolve_player_green()
        self._resolve_player_red()
        self._resolve_player_purple()
        self._resolve_player_yellow()
        self._tick_purple_cooldowns()
        self._cull_dead()
        self._check_level_complete()

    # Collision handlers

    def _resolve_player_green(self) -> None:
        p = self.player
        for g in self.greens:
            if g.alive and p.collides_with(g):
                g.alive = False
                p.score += cfg.SCORE_PER_GREEN
                p.radius = min(p.radius + 1.5, cfg.BLOB_MAX_RADIUS)
                sound.play("eat_green")

    def _resolve_player_red(self) -> None:
        p = self.player
        for r in self.reds:
            if r.alive and not r.frozen and p.collides_with(r):
                sound.play("eaten_by_red")
                pygame.time.wait(1000)
                self._end_game(won=False)
                return

    def _resolve_player_purple(self) -> None:
        p = self.player
        for pu in self.purples:
            if not pu.alive:
                continue
            pid = id(pu)
            if self._purple_cooldown.get(pid, 0) > 0:
                continue
            if p.collides_with(pu):
                p.shrink(cfg.PURPLE_SHRINK)
                self._purple_cooldown[pid] = cfg.FPS
                pu.alive = False
                sound.play("eat_purple")

    def _resolve_player_yellow(self) -> None:
        p = self.player
        for y in self.yellows:
            if y.alive and p.collides_with(y):
                y.alive = False
                p.score += cfg.SCORE_PER_YELLOW
                sound.play("eat_yellow")
                for r in self.reds:
                    r.freeze(cfg.YELLOW_FREEZE_SECONDS)

    # Helpers

    def _tick_purple_cooldowns(self) -> None:
        for pid in list(self._purple_cooldown):
            self._purple_cooldown[pid] -= 1
            if self._purple_cooldown[pid] <= 0:
                del self._purple_cooldown[pid]

    def _cull_dead(self) -> None:
        self.greens  = [b for b in self.greens  if b.alive]
        self.yellows = [b for b in self.yellows if b.alive]
        self.purples = [b for b in self.purples if b.alive]

    def _check_level_complete(self) -> None:
        if self.greens_remaining == 0:
            level_time = time.time() - self.level_start_time
            self.total_time  += level_time
            self.total_score += self.player.score

            if self.current_level >= TOTAL_LEVELS:
                self._end_game(won=True)
            else:
                self._advance_pending = True

    def advance_level(self) -> None:
        """Called by main loop after showing level-complete screen."""
        self.current_level += 1
        prev_score = self.total_score
        self._load_level(self.current_level)
        self.player.score = 0
        self._total_score_at_level_start = prev_score
        self._advance_pending = False

    def _end_game(self, won: bool) -> None:
        self.won         = won
        self.game_over   = True
        self.final_score = self.total_score + self.player.score

    def draw(self, surface: pygame.Surface) -> None:
        """ Draw level """
        for b in self.purples:
            if b.alive:
                b.draw(surface)
        for b in self.greens:
            if b.alive:
                b.draw(surface)
        for b in self.reds:
            if b.alive:
                b.draw(surface)
        for b in self.yellows:
            if b.alive:
                b.draw(surface)
        self.player.draw(surface)

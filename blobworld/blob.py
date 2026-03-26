"""
blob.py — All blob entity classes
"""

from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING

import numpy as np
import pygame
from blobworld import settings as cfg

if TYPE_CHECKING:
    from blobworld.levels import LevelConfig

_WHITE_DIM = (180, 180, 180)


class Blob:
    """Base blob class."""

    def __init__(self, x: float, y: float, radius: float, colour: tuple) -> None:
        self.x = x
        self.y = y
        self.radius = float(radius)
        self.colour = colour
        self.alive = True
        self.vx: float = 0.0
        self.vy: float = 0.0

    @property
    def pos(self) -> np.ndarray:
        """Return x and y position of a blob."""
        return np.array([self.x, self.y])

    def dist_to(self, other: "Blob") -> float:
        """Return distance between two blobs."""
        return float(np.linalg.norm(self.pos - other.pos))

    def collides_with(self, other: "Blob") -> bool:
        """Return whether this blob has collided with another blob."""
        return self.dist_to(other) < (self.radius + other.radius) * cfg.COLLISION_THRESHOLD

    def _bounce(self) -> None:
        r = self.radius
        if self.x - r < 0:
            self.x, self.vx = r, abs(self.vx)
        elif self.x + r > cfg.SCREEN_W:
            self.x, self.vx = cfg.SCREEN_W - r, -abs(self.vx)

        if self.y - r < 0:
            self.y, self.vy = r, abs(self.vy)
        elif self.y + r > cfg.SCREEN_H:
            self.y, self.vy = cfg.SCREEN_H - r, -abs(self.vy)

    def _wander(self, nudge: float = 0.03) -> None:
        if random.random() < nudge:
            angle = math.atan2(self.vy, self.vx) + random.uniform(-0.5, 0.5)
            speed = math.hypot(self.vx, self.vy) or 1.5
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed

    def _set_toward(self, target: "Blob", speed: float) -> None:
        dx = target.x - self.x
        dy = target.y - self.y
        dist = math.hypot(dx, dy) or 1
        self.vx = (dx / dist) * speed
        self.vy = (dy / dist) * speed

    def _set_away(self, threat: "Blob", speed: float) -> None:
        dx = self.x - threat.x
        dy = self.y - threat.y
        dist = math.hypot(dx, dy) or 1
        self.vx = (dx / dist) * speed
        self.vy = (dy / dist) * speed

    def update(self, player: "PlayerBlob | None" = None,
           peers: "Sequence[Blob] | None" = None) -> None:
        """Default update behaviour: move with velocity and bounce off walls.

        Subclasses often override this method and use the `player` and `peers`
        arguments. They are kept here (even if unused in the base class)
        to maintain a consistent interface across all blob types.
        """
        # pylint: disable=unused-argument
        self.x += self.vx
        self.y += self.vy
        self._bounce()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the blob as a filled circle with a light border."""
        r = int(self.radius)
        pygame.draw.circle(surface, self.colour, (int(self.x), int(self.y)), r)
        pygame.draw.circle(surface, _WHITE_DIM, (int(self.x), int(self.y)), r, 1)


class GreenBlob(Blob):
    """Green blob — flees from the player."""

    def __init__(self, level_cfg: "LevelConfig") -> None:
        super().__init__(
            x=random.uniform(60, cfg.SCREEN_W - 60),
            y=random.uniform(60, cfg.SCREEN_H - 60),
            radius=cfg.GREEN_START_RADIUS,
            colour=cfg.COLOUR_GREEN,
        )
        self._lv = level_cfg

        speed = random.uniform(level_cfg.green_speed_min, level_cfg.green_speed_max)
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def update(
        self, player: "PlayerBlob | None" = None, peers: "list[Blob] | None" = None
    ) -> None:
        if player and self.dist_to(player) < cfg.FLEE_RADIUS:
            self._set_away(player, self._lv.green_flee_speed)
        else:
            self._wander(nudge=0.04)

        self.x += self.vx
        self.y += self.vy
        self._bounce()


class RedBlob(Blob):
    """Red blob — hunts the player when in range"""

    def __init__(self, level_cfg: "LevelConfig") -> None:
        super().__init__(
            x=random.uniform(60, cfg.SCREEN_W - 60),
            y=random.uniform(60, cfg.SCREEN_H - 60),
            radius=cfg.RED_START_RADIUS,
            colour=cfg.COLOUR_RED,
        )
        self._lv = level_cfg
        self.frozen: bool = False
        self.frozen_timer: float = 0.0
        self.delay = cfg.FPS * 3  # frozen for 3 seconds at start

        speed = random.uniform(level_cfg.red_speed_min, level_cfg.red_speed_max)
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def freeze(self, seconds: float) -> None:
        """Freeze the red blob (used on start-up and when a yellow is eaten)."""
        self.frozen = True
        self.frozen_timer = seconds

    def shrink(self, amount: float) -> None:
        """Shrink the player blob by the given amount (clamped to minimum size)."""
        self.radius = amount

    def update(self, player: "PlayerBlob | None" = None,
           peers: "Sequence[Blob] | None" = None) -> None:
        if self.delay > 0:
            self.delay -= 1
            return

        if self.frozen:
            self.frozen_timer -= 1 / cfg.FPS
            if self.frozen_timer <= 0:
                self.frozen = False
            return

        # Separation from other reds
        if peers:
            for other in peers:
                if other is self or not other.alive:
                    continue
                d = self.dist_to(other)
                if 0 < d < cfg.CLUSTER_RADIUS:
                    dx = self.x - other.x
                    dy = self.y - other.y
                    push = (cfg.CLUSTER_RADIUS - d) / cfg.CLUSTER_RADIUS
                    self.vx += (dx / d) * push * cfg.CLUSTER_FORCE * 3
                    self.vy += (dy / d) * push * cfg.CLUSTER_FORCE * 3

                # Chase player if close
                if player and self.dist_to(player) < cfg.CHASE_RADIUS:
                    self._set_toward(player, self._lv.red_chase_speed)
                else:
                    self._wander(nudge=0.03)

        self.x += self.vx
        self.y += self.vy
        self._bounce()

    def draw(self, surface: pygame.Surface) -> None:
        r = int(self.radius)
        colour = (100, 30, 30) if self.frozen else self.colour

        pygame.draw.circle(surface, colour, (int(self.x), int(self.y)), r)

        if self.frozen:
            pygame.draw.circle(surface, (140, 200, 255), (int(self.x), int(self.y)), r, 2)
        else:
            pygame.draw.circle(surface, _WHITE_DIM, (int(self.x), int(self.y)), r, 1)


class PurpleBlob(Blob):
    """Purple blob — wanders slowly and shrinks the player on contact."""

    def __init__(self) -> None:
        super().__init__(
            x=random.uniform(60, cfg.SCREEN_W - 60),
            y=random.uniform(60, cfg.SCREEN_H - 60),
            radius=cfg.PURPLE_START_RADIUS,
            colour=cfg.COLOUR_PURPLE,
        )
        speed = random.uniform(cfg.PURPLE_SPEED_MIN, cfg.PURPLE_SPEED_MAX)
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def update(
        self, player: "PlayerBlob | None" = None, peers: "list[Blob] | None" = None
    ) -> None:
        self._wander(nudge=0.03)
        self.x += self.vx
        self.y += self.vy
        self._bounce()

class OrangeBlob(Blob):
    """Orange blob — wanders very slowly expands player on contact.
    also takes 5 points"""

    def __init__(self) -> None:
        super().__init__(
            x=random.uniform(60, cfg.SCREEN_W - 60),
            y=random.uniform(60, cfg.SCREEN_H - 60),
            radius=cfg.ORANGE_START_RADIUS,
            colour=cfg.COLOUR_ORANGE,
        )
        speed = random.uniform(cfg.ORANGE_SPEED_MIN, cfg.ORANGE_SPEED_MAX)
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def update(
        self, player: "PlayerBlob | None" = None, peers: "list[Blob] | None" = None
    ) -> None:
        self._wander(nudge=0.07)
        self.x += self.vx
        self.y += self.vy
        self._bounce()

class YellowBlob(Blob):
    """Yellow blob — fast, flees the player, and freezes reds when eaten."""

    def __init__(self, level_cfg: "LevelConfig") -> None:
        super().__init__(
            x=random.uniform(60, cfg.SCREEN_W - 60),
            y=random.uniform(60, cfg.SCREEN_H - 60),
            radius=cfg.YELLOW_START_RADIUS,
            colour=cfg.COLOUR_YELLOW,
        )
        self._lv = level_cfg

        speed = random.uniform(level_cfg.yellow_speed_min, level_cfg.yellow_speed_max)
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def update(
        self, player: "PlayerBlob | None" = None, peers: "list[Blob] | None" = None
    ) -> None:
        if player and self.dist_to(player) < cfg.FLEE_RADIUS:
            self._set_away(player, self._lv.yellow_flee_speed)
        else:
            self._wander(nudge=0.05)

        self.x += self.vx
        self.y += self.vy
        self._bounce()

    def draw(self, surface: pygame.Surface) -> None:
        r = int(self.radius)
        pygame.draw.circle(surface, self.colour, (int(self.x), int(self.y)), r)


class WhiteBlob(Blob):
    """
    White blob — very fast, flees the player, and skrinks reds when eaten
    speed = yellow blob level config speeds + 0.5
    """

    def __init__(self, level_cfg: "LevelConfig") -> None:
        super().__init__(
            x=random.uniform(60, cfg.SCREEN_W - 60),
            y=random.uniform(60, cfg.SCREEN_H - 60),
            radius=cfg.WHITE_START_RADIUS,
            colour=cfg.WHITE,
        )
        self._lv = level_cfg

        speed = random.uniform(level_cfg.yellow_speed_min+0.5, level_cfg.yellow_speed_max+0.5)
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

    def update(
        self, player: "PlayerBlob | None" = None, peers: "list[Blob] | None" = None
    ) -> None:
        if player and self.dist_to(player) < cfg.FLEE_RADIUS:
            self._set_away(player,  self._lv.yellow_flee_speed+0.5)
        else:
            self._wander(nudge=0.02)

        self.x += self.vx
        self.y += self.vy
        self._bounce()

    def draw(self, surface: pygame.Surface) -> None:
        r = int(self.radius)
        pygame.draw.circle(surface, self.colour, (int(self.x), int(self.y)), r)
        pygame.draw.circle(surface, (255, 240, 120), (int(self.x), int(self.y)), r, 2)


class PlayerBlob(Blob):
    """Player-controlled blob."""

    def __init__(self) -> None:
        super().__init__(
            x=cfg.SCREEN_W / 2,
            y=cfg.SCREEN_H / 2,
            radius=cfg.PLAYER_START_RADIUS,
            colour=cfg.COLOUR_PLAYER,
        )
        self.score: int = 0

    def update(
        self, player: "PlayerBlob | None" = None, peers: "list[Blob] | None" = None
    ) -> None:
        keys = pygame.key.get_pressed()
        dx = dy = 0.0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1

        if dx and dy:
            dx *= 0.7071  # ≈ 1/sqrt(2)
            dy *= 0.7071

        r = self.radius
        self.x = max(r, min(cfg.SCREEN_W - r, self.x + dx * cfg.PLAYER_SPEED))
        self.y = max(r, min(cfg.SCREEN_H - r, self.y + dy * cfg.PLAYER_SPEED))

    def shrink(self, amount: float) -> None:
        """Shrink the player blob by the given amount (clamped to minimum size)."""
        self.radius = max(cfg.BLOB_MIN_RADIUS, self.radius - amount)

    def expand(self, amount: float) -> None:
        """Expand the player blob by the given amount (clamped to maximum size)."""
        self.radius = min(cfg.BLOB_MAX_RADIUS, self.radius + amount)

    def draw(self, surface: pygame.Surface) -> None:
        r = int(self.radius)
        pygame.draw.circle(surface, cfg.COLOUR_PLAYER, (int(self.x), int(self.y)), r)
        pygame.draw.circle(surface, (160, 200, 255), (int(self.x), int(self.y)), r, 2)

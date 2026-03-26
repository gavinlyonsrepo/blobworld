"""
 hud.py — In-game heads-up display
"""

from __future__ import annotations

import pygame

from blobworld import settings as cfg
from blobworld.levels import TOTAL_LEVELS


class HUD: # pylint: disable=too-few-public-methods
    """ In-game heads-up display class control"""
    def __init__(self) -> None:
        self.font_large = pygame.font.SysFont("monospace", 20, bold=True)
        self.font_small = pygame.font.SysFont("monospace", 14)
        self.pad = 14 # edge padding

    def draw(self, surface: pygame.Surface, world) -> None:
        """ Draw the heads-up display """
        p = world.player

        # --- Top-left: Score ---
        total = world.total_score + p.score
        self._blit(surface, f"{total:>7}", self.font_large, (self.pad, self.pad))
        self._blit(surface, "SCORE", self.font_small, (self.pad, self.pad), (80, 80, 110))

        # --- Top-right: Level ---
        lv_text = f"{world.current_level}/{TOTAL_LEVELS}"
        self._blit_right(surface, lv_text, self.font_large, cfg.SCREEN_W - self.pad, self.pad, (240, 210, 40))
        self._blit_right(surface, "Level", self.font_small, cfg.SCREEN_W - self.pad, self.pad + 24, (80, 80, 110))

        # --- Bottom-left: Greens + size bar ---
        remaining = world.greens_remaining
        g_col = (60, 210, 90) if remaining > 3 else (220, 200, 40)
        self._blit(surface, f"G  {remaining:>2}/{cfg.GREEN_COUNT}", self.font_large,
                   (self.pad, cfg.SCREEN_H - 58), g_col)
        self._draw_size_bar(surface, p.radius, self.pad, cfg.SCREEN_H - 28)

        # --- Bottom-right: Reds + difficulty ---
        red_text, r_col = self._red_status(world)
        self._blit_right(surface, red_text, self.font_large,
                         cfg.SCREEN_W - self.pad, cfg.SCREEN_H - 58, r_col)
        self._blit_right(surface, cfg.DEFAULT_DIFFICULTY, self.font_small,
                         cfg.SCREEN_W - self.pad, cfg.SCREEN_H - 28, (80, 80, 110))

    def _draw_size_bar(self, surface: pygame.Surface, radius: float, x: int, y: int) -> None:
        bar_w, bar_h = 120, 8
        if cfg.BLOB_MAX_RADIUS > cfg.BLOB_MIN_RADIUS:
            pct = (radius - cfg.BLOB_MIN_RADIUS) / (cfg.BLOB_MAX_RADIUS - cfg.BLOB_MIN_RADIUS)
            pct = max(0.0, min(pct, 1.0))
        else:
            pct = 0.0
        pygame.draw.rect(surface, (40, 40, 70), (x, y, bar_w, bar_h), border_radius=4)
        if pct > 0:
            pygame.draw.rect(surface, cfg.COLOUR_PLAYER,
                             (x, y, int(bar_w * pct), bar_h), border_radius=4)
        pygame.draw.rect(surface, cfg.HUD_COLOUR, (x, y, bar_w, bar_h), 1, border_radius=4)
        label = self.font_small.render("Size", True, (80, 80, 110))
        surface.blit(label, (x + bar_w + 6, y - 2))

    def _blit(self, surface, text, font, pos, colour=None):
        surf = font.render(text, True, colour or cfg.HUD_COLOUR)
        surface.blit(surf, pos)

    def _blit_right(self, surface, text, font, rx, y, colour=None):
        """Blit text right-aligned to rx."""
        surf = font.render(text, True, colour or cfg.HUD_COLOUR)
        surface.blit(surf, (rx - surf.get_width(), y))

    def _red_status(self, world) -> tuple[str, tuple]:
        """Return red display text and colour."""
        active = sum(1 for r in world.reds if r.alive and not r.frozen)
        frozen = sum(1 for r in world.reds if r.alive and r.frozen)
        text   = f"R  {active}" + (f"  {frozen}❄" if frozen else "")
        colour = (220, 60, 60) if active > 0 else (80, 80, 100)
        return text, colour

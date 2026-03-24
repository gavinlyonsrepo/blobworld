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
        self.font_large = pygame.font.SysFont("monospace", 26, bold=True)
        self.font_small = pygame.font.SysFont("monospace", 17)

    def draw(self, surface: pygame.Surface, world) -> None:
        """ Draw the heads-up display """
        p = world.player
        # --- Top-left column ---
        # Score (level + total)
        level_score = p.score
        total       = world.total_score + level_score
        self._blit(surface, f"SCORE  {total:>6}", self.font_large, (16, 10))

        # Greens remaining
        remaining = world.greens_remaining
        g_col = (60, 210, 90) if remaining > 3 else (220, 200, 40)
        self._blit(surface, f"GREENS  {remaining:>2} / {cfg.GREEN_COUNT}",
                   self.font_large, (16, 42), g_col)

        # Size bar
        self._draw_size_bar(surface, p.radius)

        # --- Top-right column ---
        # Level indicator
        lv_text = f"LEVEL  {world.current_level} / {TOTAL_LEVELS}"
        self._blit(surface, lv_text, self.font_large,
                   (cfg.SCREEN_W - 230, 10), (240, 210, 40))

        # Red count / frozen status
        red_text, r_col = self._red_status(world)
        self._blit(surface, red_text, self.font_large, (cfg.SCREEN_W - 230, 42), r_col)

        # Yellow status
        y_alive = any(y.alive for y in world.yellows)
        y_text  = "★ YELLOW ACTIVE" if y_alive else "  yellow caught"
        y_col   = (240, 210, 40) if y_alive else (80, 80, 100)
        self._blit(surface, y_text, self.font_small,
                   (cfg.SCREEN_W - 218, 76), y_col)

        # --- Bottom legend ---
        self._blit(surface,
                   "WASD/↑↓←→ move   P pause   ESC menu",
                   self.font_small, (16, cfg.SCREEN_H - 24), (80, 80, 110))

    def _draw_size_bar(self, surface: pygame.Surface, radius: float) -> None:
        bar_w, bar_h = 150, 10
        x, y = 16, 78
        pct = min(radius / cfg.BLOB_MAX_RADIUS, 1.0)
        pygame.draw.rect(surface, (40, 40, 70), (x, y, bar_w, bar_h), border_radius=4)
        if pct > 0:
            pygame.draw.rect(surface, cfg.COLOUR_PLAYER,
                             (x, y, int(bar_w * pct), bar_h), border_radius=4)
        pygame.draw.rect(surface, cfg.HUD_COLOUR, (x, y, bar_w, bar_h), 1, border_radius=4)
        label = self.font_small.render("SIZE", True, cfg.HUD_COLOUR)
        surface.blit(label, (x + bar_w + 8, y - 2))

    def _blit(self, surface, text, font, pos, colour=None): # pylint: disable=too-many-positional-arguments
        surf = font.render(text, True, colour or cfg.HUD_COLOUR)
        surface.blit(surf, pos)

    def _red_status(self, world) -> tuple[str, tuple]:
        """Return red display text and colour."""
        active = sum(1 for r in world.reds if r.alive and not r.frozen)
        frozen = sum(1 for r in world.reds if r.alive and r.frozen)
        text   = f"RED  {active}" + (f"  +{frozen}❄" if frozen else "")
        colour = (220, 60, 60) if active > 0 else (80, 80, 100)
        return text, colour

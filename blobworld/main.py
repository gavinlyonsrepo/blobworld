""" 
    main.py — Entry point and main game loop
"""
from __future__ import annotations

import sys

import pygame

from blobworld import config
from blobworld import settings as cfg
from blobworld import highscores
from blobworld import sound
from blobworld.hud import HUD
from blobworld.world import World
from blobworld import screens


def main() -> None:
    """ main game loop"""
    config.load()
    pygame.init()
    sound.init()
    highscores.init_db()
    _show_menu()

def _screen_init():
    pygame.display.set_caption(cfg.TITLE)
    flags  = pygame.FULLSCREEN if cfg.FULLSCREEN else 0
    screen = pygame.display.set_mode((cfg.SCREEN_W, cfg.SCREEN_H), flags)
    clock  = pygame.time.Clock()
    icon = pygame.image.load(cfg.asset("images", "blobicon.png"))
    pygame.display.set_icon(icon)
    return screen, clock

def _show_menu():
    screen , clock = _screen_init()
    state = "splash"
    while True:
        if state == "splash":
            state = screens.show_splash(screen, clock)
        elif state == "menu":
            sound.play_music("eight_bit.ogg")
            state = screens.show_menu(screen, clock)
            sound.stop_music()
        elif state == "play":
            sound.play("start")
            state = _run_game(screen, clock)
        elif state == "quit":
            pygame.quit()
            sys.exit()


def _run_game(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    world = World()
    hud   = HUD()

    while not world.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sound.play("end")
                    pygame.time.wait(1000)
                    return "menu"
                if event.key == pygame.K_p:
                    _pause(screen, clock)

        world.update()

        # Level complete — show interstitial then advance
        if getattr(world, "_advance_pending", False):
            level_score = world.player.score
            total_score = world.total_score
            result = screens.show_level_complete(
                screen, clock,
                level=world.current_level,
                level_score=level_score,
                total_score=total_score,
            )
            if result == "quit":
                return "quit"
            world.advance_level()

        screen.fill(cfg.DARK_BG)
        world.draw(screen)
        hud.draw(screen, world)
        pygame.display.flip()
        clock.tick(cfg.FPS)

    return screens.show_game_over(screen, clock, world)


def _pause(screen: pygame.Surface, clock: pygame.time.Clock) -> None:
    sound.play("pause")

    font    = pygame.font.SysFont("monospace", 48, bold=True)
    surf    = font.render("PAUSED  —  P to resume", True, cfg.WHITE)
    overlay = pygame.Surface((cfg.SCREEN_W, cfg.SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    screen.blit(overlay, (0, 0))
    screen.blit(surf, (cfg.SCREEN_W // 2 - surf.get_width() // 2,
                        cfg.SCREEN_H // 2 - surf.get_height() // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                sound.play("pause")
                return
        clock.tick(15)


if __name__ == "__main__":
    main()

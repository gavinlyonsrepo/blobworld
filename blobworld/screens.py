"""
    Screens.py — All non-gameplay screens
"""

from __future__ import annotations

import os
import sys
import subprocess
import pygame

from blobworld import __version__
from blobworld import settings as cfg
from blobworld import highscores as hs
from blobworld import sound
from blobworld.levels import TOTAL_LEVELS
from blobworld.config import _CONFIG_PATH


def _centre(surface: pygame.Surface, text: str, font: pygame.font.Font,
            y: int, colour: tuple) -> None:
    surf = font.render(text, True, colour)
    surface.blit(surf, (cfg.SCREEN_W // 2 - surf.get_width() // 2, y))


def _load_image(filename: str) -> pygame.Surface | None:
    """Load and scale an image to screen size. Returns None on failure."""
    try:
        img = pygame.image.load(cfg.asset("images", filename)).convert()
        return pygame.transform.scale(img, (cfg.SCREEN_W, cfg.SCREEN_H))
    except (pygame.error, FileNotFoundError, OSError) as e:
        print(f"[screens] could not load image '{filename}': {e}")
        return None


def show_splash(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    """
    Splash screen — image 1 (title art), fade in, hold, any key to skip
    Fade in the title art, hold for a few seconds, then go to menu.
    Any keypress or click skips immediately.
    Returns 'menu'.
    """
    art = _load_image("title.jpg")       # image 1 — with BLOB WORLD text
    # If image missing just skip straight to menu
    if art is None:
        return "menu"

    fade_in_frames  = cfg.FPS * 3        # 1 second fade in
    hold_frames     = cfg.FPS * 3        # hold for 3 seconds
    total_frames    = fade_in_frames + hold_frames
    frame           = 0
    overlay = pygame.Surface((cfg.SCREEN_W, cfg.SCREEN_H))
    overlay.fill((0, 0, 0))
    hint_font = pygame.font.SysFont("monospace", 20)

    while frame < total_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return "menu"            # any key skips

        screen.blit(art, (0, 0))
        # Fade in: alpha goes 255 → 0 over FADE_IN_FRAMES
        if frame < fade_in_frames:
            alpha = int(255 * (1 - frame / fade_in_frames))
            overlay.set_alpha(alpha)
            screen.blit(overlay, (0, 0))
        # Show "press any key" hint once fully visible
        if frame >= fade_in_frames:
            _centre(screen, "press any key to continue",
                    hint_font, cfg.SCREEN_H - 40, (180, 180, 200))
        pygame.display.flip()
        clock.tick(cfg.FPS)
        frame += 1

    return "menu"


def show_menu(screen: pygame.Surface, clock: pygame.time.Clock) -> str:
    """
    Main menu — image 2 as background (no title text)
    """
    title_font = pygame.font.SysFont("monospace", 36, bold=True)
    hint_font  = pygame.font.SysFont("monospace", 20)
    bg = _load_image("menu_bg.jpg")      # image 2 — characters, no title
    options  = ["PLAY", "HIGH SCORES", "SETTINGS", "HELP", "ABOUT", "QUIT"]
    selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    selected = (selected - 1) % len(options)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    selected = (selected + 1) % len(options)
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    choice = options[selected]
                    actions = {
                        "PLAY": lambda: "play",
                        "HIGH SCORES": lambda: show_leaderboard(screen, clock),
                        "SETTINGS": lambda: show_settings(screen, clock),
                        "HELP": lambda: show_help(screen, clock),
                        "ABOUT": lambda: show_about(screen, clock),
                        "QUIT": lambda: "quit",
                    }
                    result = actions[choice]()
                    if result:
                        return result
        # Draw background
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill(cfg.DARK_BG)

        panel_x = cfg.SCREEN_W // 2 - 170
        panel_y = 60
        _draw_menu_panel(screen, panel_x, panel_y, options, selected, title_font)
        _centre(screen, "↑ ↓  navigate     ENTER  select",
                hint_font, cfg.SCREEN_H - 40, (160, 160, 190))
        pygame.display.flip()
        clock.tick(cfg.FPS)

def _draw_menu_panel(surface, panel_x, panel_y, options, selected, font): # pylint: disable=too-many-arguments
    """Draw the semi-transparent menu panel and options."""
    panel = pygame.Surface((340, len(options) * 60 + 20), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 140))
    surface.blit(panel, (panel_x, panel_y))
    for i, option in enumerate(options):
        colour = (80, 200, 120) if i == selected else cfg.HUD_COLOUR
        if i == selected:
            highlight_bar = pygame.Surface((340, 52), pygame.SRCALPHA)
            highlight_bar.fill((80, 200, 120, 40))
            surface.blit(highlight_bar, (panel_x, panel_y + 10 + i * 60))
        _centre(surface, option, font, panel_y + 18 + i * 60, colour)

def show_help(screen: pygame.Surface, clock: pygame.time.Clock) -> None: # pylint: disable=too-many-locals
    """ Help screen — controls and blob guide """
    title_font   = pygame.font.SysFont("monospace", 40, bold=True)
    section_font = pygame.font.SysFont("monospace", 20, bold=True)
    body_font    = pygame.font.SysFont("monospace", 18)
    hint_font    = pygame.font.SysFont("monospace", 18)
    bg = _load_image("menu_bg.jpg")
    # Blob legend: (colour, label, description)
    blob_guide = [
        ((80,  140, 255), "BLUE (You)", "Eat green blobs to grow. Avoid red."),
        ((60,  210,  90), "GREEN",      "Your prey — eat all 15 to complete level."),
        ((220,  50,  50), "RED",        "Hunts you. One touch = game over."),
        ((160,  60, 220), "PURPLE",     "Wanderer — shrinks you on contact."),
        ((255, 140,   0), "ORANGE",     "Wanderer — expands you on contact."),
        ((240, 210,  40), "YELLOW",     "Catch it: freezes reds."),
        ((255, 255, 255), "WHITE",      "Catch it: shrinks reds."),
    ]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_ESCAPE, pygame.K_RETURN):
                return
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill(cfg.DARK_BG)
        overlay = pygame.Surface((cfg.SCREEN_W, cfg.SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 172))
        screen.blit(overlay, (0, 0))
        _centre(screen, "HOW TO PLAY", title_font, 20, (80, 200, 120))
        # --- Controls ---
        _centre(screen, "CONTROLS", section_font, 105, (240, 210, 40))
        controls = [
            "WASD  or  Arrow Keys — move your blob",
            "P — pause / unpause ESC — return to menu",
        ]
        for i, line in enumerate(controls):
            _centre(screen, line, body_font, 125 + i * 18, cfg.HUD_COLOUR)
        # --- Objective ---
        _centre(screen, "OBJECTIVE", section_font, 190, (220, 210, 40))
        _centre(screen, "Eat all 15 GREEN blobs to complete each level.", body_font, 210, cfg.HUD_COLOUR)
        _centre(screen, "Perfect score of 1500 pts.", body_font, 230, cfg.HUD_COLOUR)
        # --- Scoring ---
        _centre(screen, "SCORING - Hard mode", section_font, 260, (240, 210, 40))
        _centre(screen, "Green = 10,  150 pts per level"\
                , body_font, 280, cfg.HUD_COLOUR)
        # --- Blob guide ---
        _centre(screen, "BLOBS", section_font, 320, (240, 210, 40))
        for i, (colour, label, desc) in enumerate(blob_guide):
            y = 360 + i * 46
            # coloured circle indicator
            pygame.draw.circle(screen, colour, (cfg.SCREEN_W // 2 - 320, y + 10), 10)
            label_surf = section_font.render(f"{label:<16}", True, colour)
            desc_surf  = body_font.render(desc, True, cfg.HUD_COLOUR)
            screen.blit(label_surf, (cfg.SCREEN_W // 2 - 300, y))
            screen.blit(desc_surf,  (cfg.SCREEN_W // 2 - 300 + label_surf.get_width() + 10, y + 2))
        _centre(screen, "ESC / ENTER to return", hint_font,
                cfg.SCREEN_H - 30, (100, 100, 140))
        pygame.display.flip()
        clock.tick(cfg.FPS)

def show_about(screen: pygame.Surface, clock: pygame.time.Clock) -> None:
    """ Display About screen to user"""
    title_font = pygame.font.SysFont("monospace", 48, bold=True)
    body_font  = pygame.font.SysFont("monospace", 24)
    hint_font  = pygame.font.SysFont("monospace", 20)

    bg = _load_image("menu_bg.jpg")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_ESCAPE, pygame.K_RETURN):
                return
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill(cfg.DARK_BG)
        # Dark overlay so text is readable over the art
        overlay = pygame.Surface((cfg.SCREEN_W, cfg.SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        _centre(screen, "ABOUT", title_font, 40, (80, 200, 120))

        lines = [
            ("Blob World", True,  (240, 210,  40)),
            (f"Version  {__version__}", False, cfg.HUD_COLOUR),
            ("", False, cfg.HUD_COLOUR),
            ("On planet K2-18b, Life finds a way.", False, cfg.HUD_COLOUR),
            ("A survival game.", False, cfg.HUD_COLOUR),
            ("Author :  Gavin Lyons", False, cfg.HUD_COLOUR),
            ("License:  GPL-3.0", False, cfg.HUD_COLOUR),
            ("Source :  github.com/gavinlyonsrepo/blobworld", False, (100, 160, 255)),
            ("", False, cfg.HUD_COLOUR),
            ("Built with Python 3 + pygame", False, (120, 120, 150)),
        ]
        for i, (text, bold, colour) in enumerate(lines):
            font = body_font
            if bold:
                font = pygame.font.SysFont("monospace", 26, bold=True)
            _centre(screen, text, font, 110 + i * 34, colour)

        _centre(screen, "ESC / ENTER to return", hint_font,
        cfg.SCREEN_H - 30, (100, 100, 140))
        pygame.display.flip()
        clock.tick(cfg.FPS)

def show_settings(screen, clock):
    """ 
    Settings note and 
    display install desktop button option to user
    """
    title_font  = pygame.font.SysFont("monospace", 48, bold=True)
    hint_font   = pygame.font.SysFont("monospace", 18)
    btn_font    = pygame.font.SysFont("monospace", 22, bold=True)
    btn_rect    = pygame.Rect(0, 0, 320, 50)
    btn_rect.center = (cfg.SCREEN_W // 2, 480)
    messages    = []
    success     = None

    while True:
        mouse_pos = pygame.mouse.get_pos()
        hover     = btn_rect.collidepoint(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_ESCAPE, pygame.K_RETURN):
                return
            if event.type == pygame.MOUSEBUTTONDOWN and hover:
                success, messages = install_desktop_entry()

        screen.fill(cfg.DARK_BG)
        _centre(screen, "Settings", title_font, 60, (80, 200, 120))
        set_text = f"Settings are in the config.ini file at {_CONFIG_PATH}"
        _centre(screen, set_text, btn_font,
        150, (100, 100, 140))
        # Install button
        _draw_button(screen, "INSTALL DESKTOP ENTRY", btn_rect, btn_font, hover)
        # Feedback messages after install
        if messages:
            col = (80, 200, 120) if success else (220, 60, 60)
            for i, msg in enumerate(messages):
                _centre(screen, msg, hint_font, 550 + i * 26, col)

        _centre(screen, "ESC to return", hint_font,
                cfg.SCREEN_H - 35, (100, 100, 140))

        pygame.display.flip()
        clock.tick(cfg.FPS)

def _draw_button(surface, text, rect, font, hover=False):
    colour = (80, 200, 120) if hover else (50, 130, 80)
    pygame.draw.rect(surface, colour, rect, border_radius=6)
    pygame.draw.rect(surface, (180, 180, 180), rect, 1, border_radius=6)
    surf = font.render(text, True, (255, 255, 255))
    surface.blit(surf, (rect.centerx - surf.get_width() // 2,
                         rect.centery - surf.get_height() // 2))


def install_desktop_entry() -> tuple[bool, list[str]]:
    """
    Install the desktop entry files, uses curl subprocess
    needs network and github.com
    """
    messages = []
    if not sys.platform.startswith("linux"):
        messages.append("Desktop install is Linux only.")
        return False, messages
    try:
        path_list = [
            os.environ["HOME"] + "/.local/share/icons/",
            os.environ["HOME"] + "/.local/share/applications/",
        ]
        github_list = [
            "https://raw.githubusercontent.com/gavinlyonsrepo/blobworld/master/desktop/blobworld.png",
            "https://raw.githubusercontent.com/gavinlyonsrepo/blobworld/master/desktop/blobworld.desktop",
        ]
        file_list = ["blobworld.png", "blobworld.desktop"]

        for my_file, my_path, my_url in zip(file_list, path_list, github_list):
            os.makedirs(my_path, exist_ok=True)
            dest = os.path.join(my_path, my_file)
            subprocess.run(
                    ["curl", "-s", "--fail", "-o", dest, my_url],
                    check=True
                )
            if os.path.isfile(dest):
                messages.append(f"Installed: {dest}")
            else:
                messages.append(f"Not Installed: {dest}")
        return True, messages
    except (subprocess.SubprocessError, OSError, KeyError) as e:
        messages.append("Install failed — check network or curl.")
        messages.append(str(e))
        return False, messages

#

def show_level_complete(screen: pygame.Surface, clock: pygame.time.Clock,
                        level: int, level_score: int, total_score: int) -> str:
    """ Level complete interstitial """
    sound.play("level_end")
    title_font = pygame.font.SysFont("monospace", 56, bold=True)
    body_font  = pygame.font.SysFont("monospace", 30)
    hint_font  = pygame.font.SysFont("monospace", 20)
    countdown = cfg.FPS * 5

    while countdown > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return "play"

        screen.fill(cfg.DARK_BG)
        _centre(screen, f"LEVEL {level} COMPLETE", title_font, 140, (80, 200, 120))
        _centre(screen, f"Level score :  {level_score:>6}", body_font, 260, cfg.WHITE)
        _centre(screen, f"Total score :  {total_score:>6}", body_font, 305, cfg.HUD_COLOUR)
        _centre(screen, f"Next: LEVEL {level + 1} of {TOTAL_LEVELS}",
                body_font, 385, (240, 210, 40))
        _centre(screen, "ENTER to continue   (auto-advancing...)",
                hint_font, cfg.SCREEN_H - 40, (100, 100, 140))

        pygame.display.flip()
        clock.tick(cfg.FPS)
        countdown -= 1

    return "play"


def show_game_over(screen: pygame.Surface, clock: pygame.time.Clock, # pylint: disable=too-many-locals
                   world) -> str:
    """ Game over / victory """
    sound.play("end")

    header_font = pygame.font.SysFont("monospace", 64, bold=True)
    body_font   = pygame.font.SysFont("monospace", 32)
    hint_font   = pygame.font.SysFont("monospace", 20)

    score  = world.final_score
    won    = world.won
    level  = world.current_level
    t      = world.total_time
    header = "YOU WIN!" if won else "GAME OVER"
    h_col  = (80, 220, 120) if won else (220, 60, 60)

    player_name = ""
    if hs.is_high_score(score):
        player_name = _name_entry(screen, clock, score, header, h_col,
                                  header_font, body_font, hint_font)
        hs.save_score(player_name, score,
                      level_reached=level, time_seconds=t)
        show_leaderboard(screen, clock, highlight_name=player_name)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "play"
                if event.key == pygame.K_m:
                    return "menu"
                if event.key == pygame.K_ESCAPE:
                    return "quit"

        screen.fill(cfg.DARK_BG)
        _centre(screen, header, header_font, 100, h_col)
        _centre(screen, f"SCORE :  {score}", body_font, 230, cfg.WHITE)
        _centre(screen, f"LEVEL REACHED :  {level} / {TOTAL_LEVELS}",
                body_font, 278, cfg.HUD_COLOUR)
        m, s = divmod(int(t), 60)
        _centre(screen, f"TIME  :  {m}:{s:02d}", body_font, 326, cfg.HUD_COLOUR)
        _centre(screen, "[R] Play Again   [M] Menu   [ESC] Quit",
                hint_font, cfg.SCREEN_H - 50, (100, 100, 140))

        pygame.display.flip()
        clock.tick(cfg.FPS)


def _name_entry(screen, clock, score, header, h_col, # pylint: disable=too-many-arguments
                header_font, body_font, hint_font) -> str:
    name        = ""
    max_len     = 12
    prompt_font = pygame.font.SysFont("monospace", 36, bold=True)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return name or "PLAYER"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    return name
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isprintable() and len(name) < max_len:
                    name += event.unicode.upper()

        screen.fill(cfg.DARK_BG)
        _centre(screen, header, header_font, 80, h_col)
        _centre(screen, f"SCORE: {score}", body_font, 180, cfg.WHITE)
        _centre(screen, "NEW HIGH SCORE!", prompt_font, 260, (220, 200, 40))
        _centre(screen, "Enter your name:", body_font, 320, cfg.HUD_COLOUR)
        _centre(screen, name + "_", body_font, 370, cfg.WHITE)
        _centre(screen, "ENTER to confirm", hint_font,
                cfg.SCREEN_H - 60, (100, 100, 140))

        pygame.display.flip()
        clock.tick(cfg.FPS)


def show_leaderboard(screen: pygame.Surface, clock: pygame.time.Clock,
                     highlight_name: str = "") -> None:
    """ Show Leaderboard highscores table to user"""
    title_font = pygame.font.SysFont("monospace", 44, bold=True)
    head_font  = pygame.font.SysFont("monospace", 19, bold=True)
    row_font   = pygame.font.SysFont("monospace", 21)
    hint_font  = pygame.font.SysFont("monospace", 18)

    entries = hs.get_top_scores()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_ESCAPE, pygame.K_RETURN):
                return

        screen.fill(cfg.DARK_BG)
        _centre(screen, "HIGH SCORES", title_font, 30, (220, 200, 40))
        header = "#   NAME                SCORE    LVL   TIME   DATE         MODE"
        _centre(screen, header, head_font, 100, (140, 140, 180))
        pygame.draw.line(screen, (60, 60, 90),
                         (60, 126), (cfg.SCREEN_W - 60, 126), 1)

        if not entries:
            _centre(screen, "No scores yet!", row_font, 200, cfg.HUD_COLOUR)
        else:
            for entry in entries:
                y      = 136 + entry.rank * 38
                colour = (220, 200, 40) if entry.name == highlight_name else cfg.HUD_COLOUR
                line = (f"{entry.rank:>2}.  {entry.name:<14}"
                        f"{entry.score:>7}  {entry.level_reached:>3}  "
                        f"{entry.time_display:>6}  {entry.date[:10]} {entry.difficulty}")
                _centre(screen, line, row_font, y, colour)

        _centre(screen, "ESC / ENTER to return", hint_font,
                cfg.SCREEN_H - 35, (100, 100, 140))

        pygame.display.flip()
        clock.tick(cfg.FPS)

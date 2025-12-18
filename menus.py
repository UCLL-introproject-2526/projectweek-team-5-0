# menus.py
import pygame
import pygame_gui
import os

################################
# Main Menu
################################
def main_menu(screen):
    clock = pygame.time.Clock()

    # Load background and images **once**
    background = pygame.image.load("sprites/background/space.jpg").convert()
    background = pygame.transform.scale(background, screen.get_size())

    logo_image = pygame.image.load("sprites/logo/logo.jpg").convert_alpha()
    logo_width = 300
    logo_height = int(logo_image.get_height() * (logo_width / logo_image.get_width()))
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    logo_rect = logo_image.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 200))

    title_font = pygame.font.Font(None, 80)
    title_text = title_font.render("Meteo Beats", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 50))

    manager = pygame_gui.UIManager(screen.get_size(), "gui-themes/theme.json")

    # Buttons
    start_btn = pygame_gui.elements.UIButton(pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2, 200, 50), "Start Game", manager)
    settings_btn = pygame_gui.elements.UIButton(pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2 + 60, 200, 50), "Settings", manager)
    how_to_play_btn = pygame_gui.elements.UIButton(pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2 + 120, 200, 50), "How to Play", manager)
    quit_btn = pygame_gui.elements.UIButton(pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2 + 180, 200, 50), "Quit", manager)

    while True:
        time_delta = clock.tick(60)/1000.0
        screen.blit(background, (0, 0))
        screen.blit(logo_image, logo_rect)
        screen.blit(title_text, title_rect)

        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_btn:
                    return "start"
                elif event.ui_element == settings_btn:
                    return "settings"
                elif event.ui_element == how_to_play_btn:  # NEW
                    pygame_gui.windows.UIMessageWindow(
                        rect=pygame.Rect((screen.get_width()//2 - 300, screen.get_height()//2 - 200), (600, 400)),
                        html_message="""
<b>EARTH'S LAST DEFENSE</b><br><br>
A massive meteoroid stream is headed straight for Earth! You're piloting humanity's last hope - a prototype spacecraft equipped with an experimental Plasma Cannon.<br><br>
The cannon is incredibly powerful, but there's a catch: it can only fire when synchronized with your ship's powercore rhythm. Listen for the steady pulse - that's your core charging. Fire ON THE BEAT and unleash devastating shots. When you fire off-beat and the unstable energy will backfire, damaging your own systems! <br>
There are upgrades in the debris that make you more powerful but they might need more charge and thus change the rythm of your power core!<br>
<b>Your Mission:</b> Destroy every meteoroid before they reach Earth!<br><br>
<b>Controls:</b><br>
- WASD - Maneuver your ship<br>
- Mouse - Aim<br>
- Left Click - Fire (only on the beat!)<br><br>
<b>Remember:</b><br>
- Listen to the metronome pulse<br>
- Off-beat shots hurt YOU<br>
- Collect health packs from debris<br>
- Tip: the easiest way to survive is to keep shooting every beat, even if there is nothing there just to keep the rythm!
""",
                        manager=manager,
                        window_title="How to Play"
                    )
                elif event.ui_element == quit_btn:
                    pygame.quit()
                    exit()

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

################################
# Settings Menu
################################
def settings_menu(screen):
    clock = pygame.time.Clock()

    background = pygame.image.load("sprites/background/space.jpg").convert()
    background = pygame.transform.scale(background, screen.get_size())

    logo_image = pygame.image.load("sprites/logo/logo.jpg").convert_alpha()
    logo_width = 300
    logo_height = int(logo_image.get_height() * (logo_width / logo_image.get_width()))
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    logo_rect = logo_image.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 200))

    title_font = pygame.font.Font(None, 80)
    title_text = title_font.render("Meteo Beats", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 70))

    subtitle_font = pygame.font.Font(None, 60)
    subtitle_text = subtitle_font.render("Settings", True, (255, 255, 255))
    subtitle_rect = subtitle_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))

    manager = pygame_gui.UIManager(screen.get_size(), "gui-themes/theme.json")

    keyboard_btn = pygame_gui.elements.UIButton(pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2 + 40, 200, 50), "Keyboard", manager)
    video_btn = pygame_gui.elements.UIButton(pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2 + 100, 200, 50), "Video", manager)
    skins_btn = pygame_gui.elements.UIButton(pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2 + 160, 200, 50), "Skins", manager)
    back_btn = pygame_gui.elements.UIButton(pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2 + 220, 200, 50), "Back", manager)

    while True:
        time_delta = clock.tick(60)/1000.0
        screen.blit(background, (0, 0))
        screen.blit(logo_image, logo_rect)
        screen.blit(title_text, title_rect)
        screen.blit(subtitle_text, subtitle_rect)

        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_btn:
                    return "back"
                elif event.ui_element == keyboard_btn:
                    return "keyboard"
                elif event.ui_element == video_btn:
                    return "video"
                elif event.ui_element == skins_btn:
                    return "skins"

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

################################
# Sub Menus
################################

# keyboard sebmenu
def keyboard_menu(surface):
    clock = pygame.time.Clock()

    background = pygame.image.load("sprites/background/space.jpg").convert()
    background = pygame.transform.scale(background, surface.get_size())

    logo_image = pygame.image.load("sprites/logo/logo.jpg").convert_alpha()
    logo_width = 300
    logo_height = int(logo_image.get_height() * (logo_width / logo_image.get_width()))
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    logo_rect = logo_image.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 200))

    title_font = pygame.font.Font(None, 80)
    title_text = title_font.render("Meteo Beats", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 70))

    subtitle_font = pygame.font.Font(None, 60)
    subtitle_text = subtitle_font.render("Keyboard Settings", True, (255, 255, 255))
    subtitle_rect = subtitle_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))

    manager = pygame_gui.UIManager(surface.get_size(), "gui-themes/theme.json")

    # buttons
    qwearty_btn = pygame_gui.elements.UIButton(pygame.Rect(surface.get_width() // 2 - 100, surface.get_height() // 2 + 40, 200, 50), "Qwearty", manager)
    azerty_btn = pygame_gui.elements.UIButton(pygame.Rect(surface.get_width() // 2 - 100, surface.get_height() // 2 + 100, 200, 50), "Azerty", manager)
    back_btn = pygame_gui.elements.UIButton(pygame.Rect(surface.get_width() // 2 - 100, surface.get_height() // 2 + 160, 200, 50), "Back", manager)

    while True:
        time_delta = clock.tick(60) / 1000.0
        surface.blit(background, (0, 0))
        surface.blit(logo_image, logo_rect)
        surface.blit(title_text, title_rect)
        surface.blit(subtitle_text, subtitle_rect)

        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_btn:
                    return "back"
                elif event.ui_element == azerty_btn:
                    print('azerty')
                elif event.ui_element == qwearty_btn:
                    print('qwearty')

        manager.update(time_delta)
        manager.draw_ui(surface)
        pygame.display.flip()

# video sebmenu
def video_menu(surface):
    clock = pygame.time.Clock()

    background = pygame.image.load("sprites/background/space.jpg").convert()
    background = pygame.transform.scale(background, surface.get_size())

    logo_image = pygame.image.load("sprites/logo/logo.jpg").convert_alpha()
    logo_width = 300
    logo_height = int(logo_image.get_height() * (logo_width / logo_image.get_width()))
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    logo_rect = logo_image.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 200))

    title_font = pygame.font.Font(None, 80)
    title_text = title_font.render("Meteo Beats", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 70))

    subtitle_font = pygame.font.Font(None, 60)
    subtitle_text = subtitle_font.render("Video Settings", True, (255, 255, 255))
    subtitle_rect = subtitle_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))

    manager = pygame_gui.UIManager(surface.get_size(), "gui-themes/theme.json")

    # buttons
    fullscreen_btn = pygame_gui.elements.UIButton(pygame.Rect(surface.get_width() // 2 - 100, surface.get_height() // 2 + 40, 200, 50), "Fullscreen", manager)
    windowed_btn = pygame_gui.elements.UIButton(pygame.Rect(surface.get_width() // 2 - 100, surface.get_height() // 2 + 100, 200, 50), "Windowed", manager)
    back_btn = pygame_gui.elements.UIButton(pygame.Rect(surface.get_width() // 2 - 100, surface.get_height() // 2 + 160, 200, 50), "Back", manager)

    while True:
        time_delta = clock.tick(60) / 1000.0
        surface.blit(background, (0, 0))
        surface.blit(logo_image, logo_rect)
        surface.blit(title_text, title_rect)
        surface.blit(subtitle_text, subtitle_rect)

        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_btn:
                    return "back"
                elif event.ui_element == fullscreen_btn:
                    print('fullscreen')
                elif event.ui_element == windowed_btn:
                    print('windowed')

        manager.update(time_delta)
        manager.draw_ui(surface)
        pygame.display.flip()

# keyboard sebmenu
def skins_menu(surface):
    clock = pygame.time.Clock()

    background = pygame.image.load("sprites/background/space.jpg").convert()
    background = pygame.transform.scale(background, surface.get_size())

    logo_image = pygame.image.load("sprites/logo/logo.jpg").convert_alpha()
    logo_width = 300
    logo_height = int(logo_image.get_height() * (logo_width / logo_image.get_width()))
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    logo_rect = logo_image.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 200))

    title_font = pygame.font.Font(None, 80)
    title_text = title_font.render("Meteo Beats", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 70))

    subtitle_font = pygame.font.Font(None, 60)
    subtitle_text = subtitle_font.render("Skins Settings", True, (255, 255, 255))
    subtitle_rect = subtitle_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))

    manager = pygame_gui.UIManager(surface.get_size(), "gui-themes/theme.json")

    # buttons
    skin_redeye_btn = pygame_gui.elements.UIButton(pygame.Rect(surface.get_width() // 2 - 100, surface.get_height() // 2 + 40, 200, 50), "Red eye", manager)
    skin_pinky_btn = pygame_gui.elements.UIButton(pygame.Rect(surface.get_width() // 2 - 100, surface.get_height() // 2 + 100, 200, 50), "Pinky", manager)
    back_btn = pygame_gui.elements.UIButton(pygame.Rect(surface.get_width() // 2 - 100, surface.get_height() // 2 + 160, 200, 50), "Back", manager)

    while True:
        time_delta = clock.tick(60) / 1000.0
        surface.blit(background, (0, 0))
        surface.blit(logo_image, logo_rect)
        surface.blit(title_text, title_rect)
        surface.blit(subtitle_text, subtitle_rect)

        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_btn:
                    return "back"
                elif event.ui_element == skin_redeye_btn:
                    print('red eye')
                elif event.ui_element == skin_pinky_btn:
                    print('youre pink now')

        manager.update(time_delta)
        manager.draw_ui(surface)
        pygame.display.flip()

################################
# Game Over Menu
################################
def game_over_menu(elapsed_time):
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    # Load background
    background = pygame.image.load("sprites/background/space.jpg").convert()
    background = pygame.transform.scale(background, screen.get_size())

    # Load UI manager
    manager = pygame_gui.UIManager(screen.get_size(), "gui-themes/theme.json")

    # Logo
    logo_image = pygame.image.load("sprites/logo/logo.jpg").convert_alpha()
    logo_width = 300
    logo_height = int(logo_image.get_height() * (logo_width / logo_image.get_width()))
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    logo_rect = logo_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 200))

    # Game title
    title_font = pygame.font.Font(None, 80)
    title_text = title_font.render("Meteo Beats", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 70))

    # Game Over text
    game_over_font = pygame.font.Font(None, 60)
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    timer_font = pygame.font.Font(None, 50)
    timer_surface = timer_font.render(f"Time Survived: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
    timer_rect = timer_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 40))

    # Buttons
    restart_btn = pygame_gui.elements.UIButton(
        pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 60, 200, 50),
        "Restart",
        manager
    )
    main_menu_btn = pygame_gui.elements.UIButton(
        pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 120, 200, 50),
        "Main Menu",
        manager
    )
    quit_btn = pygame_gui.elements.UIButton(
        pygame.Rect(screen.get_width() // 2 - 100, screen.get_height() // 2 + 180, 200, 50),
        "Quit",
        manager
    )

    # Event loop
    while True:
        time_delta = clock.tick(60) / 1000.0
        screen.blit(background, (0, 0))
        screen.blit(logo_image, logo_rect)
        screen.blit(title_text, title_rect)
        screen.blit(game_over_text, game_over_rect)
        screen.blit(timer_surface, timer_rect)

        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == restart_btn:
                    return "restart"
                elif event.ui_element == main_menu_btn:
                    return "main_menu"
                elif event.ui_element == quit_btn:
                    return "quit"

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()


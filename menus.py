# menus.py
import pygame
import pygame_gui
import os

# ------------------------------
# Main Menu
# ------------------------------
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
    title_text = title_font.render("Asteroid Destroyers", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 70))

    manager = pygame_gui.UIManager(screen.get_size(), "gui-themes/theme.json")

    # Buttons
    start_btn = pygame_gui.elements.UIButton(pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2, 200, 50), "Start Game", manager)
    settings_btn = pygame_gui.elements.UIButton(pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2 + 60, 200, 50), "Settings", manager)
    quit_btn = pygame_gui.elements.UIButton(pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2 + 120, 200, 50), "Quit", manager)

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
                elif event.ui_element == quit_btn:
                    pygame.quit()
                    exit()

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

# ------------------------------
# Settings Menu
# ------------------------------
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
    title_text = title_font.render("Asteroid Destroyers", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 70))

    subtitle_font = pygame.font.Font(None, 60)
    subtitle_text = subtitle_font.render("Settings", True, (255, 255, 255))
    subtitle_rect = subtitle_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2))

    manager = pygame_gui.UIManager(screen.get_size(), "gui-themes/theme.json")

    video_btn = pygame_gui.elements.UIButton(pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2 + 40, 200, 50), "Video", manager)
    skins_btn = pygame_gui.elements.UIButton(pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2 + 100, 200, 50), "Skins", manager)
    back_btn = pygame_gui.elements.UIButton(pygame.Rect(screen.get_width()//2 - 100, screen.get_height()//2 + 160, 200, 50), "Back", manager)

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

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

def main_menu(screen):
    clock = pygame.time.Clock()

    # Load background and UI theme using the passed screen
    main_menu_background = pygame.image.load("sprites/background/space.jpg").convert()
    main_menu_background = pygame.transform.scale(main_menu_background, screen.get_size())
    manager = pygame_gui.UIManager(screen.get_size(), "gui-themes/theme.json")

    # Logo
    logo_image = pygame.image.load("sprites/logo/logo.jpg").convert_alpha()
    logo_width = 300
    logo_height = int(logo_image.get_height() * (logo_width / logo_image.get_width()))
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    logo_rect = logo_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 200))

    # Title
    title_font = pygame.font.Font(None, 80)
    title_text = title_font.render("Astroid Destroyers", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 70))

    # Buttons
    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (screen.get_width() // 2 - 100, screen.get_height() // 2),
            (200, 50)
        ),
        text="Start Game",
        manager=manager
    )

    settings_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (screen.get_width() // 2 - 100, screen.get_height() // 2 + 60),
            (200, 50)
        ),
        text="Settings",
        manager=manager
    )

    quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (screen.get_width() // 2 - 100, screen.get_height() // 2 + 120),
            (200, 50)
        ),
        text="Quit",
        manager=manager
    )

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        screen.blit(main_menu_background, (0, 0))
        screen.blit(logo_image, logo_rect)
        screen.blit(title_text, title_rect)

        for event in pygame.event.get():
            manager.process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    return
                elif event.ui_element == settings_button:
                    settings_menu(screen)
                elif event.ui_element == quit_button:
                    pygame.quit()
                    exit()

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
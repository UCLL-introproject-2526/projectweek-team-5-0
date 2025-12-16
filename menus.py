# menus.py
import pygame
import pygame_gui
import os

def main_menu():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    # Load background
    main_menu_background = pygame.image.load("sprites/background/space.jpg").convert()
    main_menu_background = pygame.transform.scale(main_menu_background, screen.get_size())

    # Load UI theme
    theme_path = os.path.join("gui-themes", "theme.json")
    manager = pygame_gui.UIManager(screen.get_size(), theme_path)

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
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    return
                elif event.ui_element == settings_button:
                    print("Settings button clicked!")
                elif event.ui_element == quit_button:
                    pygame.quit()
                    exit()

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
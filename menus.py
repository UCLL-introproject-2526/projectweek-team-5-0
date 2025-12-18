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
    title_text = title_font.render("Asteroid Destroyers", True, (255, 255, 255))
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
    title_text = title_font.render("Asteroid Destroyers", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 70))

    subtitle_font = pygame.font.Font(None, 60)
    subtitle_text = subtitle_font.render("Keyboard Settings", True, (255, 255, 255))
    subtitle_rect = subtitle_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))

    manager = pygame_gui.UIManager(surface.get_size(), "gui-themes/theme.json")

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

        manager.update(time_delta)
        manager.draw_ui(surface)
        pygame.display.flip()

def video_menu(surface):
    print("Video settings opened")
    return "back"

def skins_menu(surface):
    print("Skins settings opened")
    return "back"

################################
# Game Over Menu
################################
def game_over_menu():
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
    title_text = title_font.render("Asteroid Destroyers", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 70))

    # Game Over text
    game_over_font = pygame.font.Font(None, 60)
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

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


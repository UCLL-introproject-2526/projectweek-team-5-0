import pygame
import pygame_gui
import time
import os
from ui_elements import *
from metronome import Metronome
from asteroids import Asteroid
from player_state import PlayerState
from avatar import Avatar
from projectile import Projectile

pygame.init()

def main_menu():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    # Load background and scale to screen
    main_menu_background = pygame.image.load("sprites/background/space.jpg").convert()
    main_menu_background = pygame.transform.scale(main_menu_background, screen.get_size())

    # Load UI theme
    theme_path = os.path.join("gui-themes", "theme.json")
    manager = pygame_gui.UIManager(screen.get_size(), theme_path)

    # Load logo image
    logo_image = pygame.image.load("sprites/logo/logo.jpg").convert_alpha()
    logo_width = 300
    logo_height = int(logo_image.get_height() * (logo_width / logo_image.get_width()))
    logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
    logo_rect = logo_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 200))

    # Create game title text
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

    quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (screen.get_width() // 2 - 100, screen.get_height() // 2 + 70),
            (200, 50)
        ),
        text="Quit",
        manager=manager
    )

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        screen.blit(main_menu_background, (0, 0))

        # Draw logo and title
        screen.blit(logo_image, logo_rect)
        screen.blit(title_text, title_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    return
                if event.ui_element == quit_button:
                    pygame.quit()
                    exit()

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()

# =====================================================
# deze functie zitten alle dingen in die gerund worden.
# =====================================================

# closes game properly
def close_game():
    pygame.quit()

def main():
    surface = create_main_surface()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    start_time = time.time()
    player_state = PlayerState()
    metronome = Metronome(bpm=120)
    running = True # run game status
    game_over = False
    asteroids = []
    projectiles = []
    last_spawn_time = 0

    # Create a avatar instance
    avatar = Avatar(surface.get_width(), surface.get_height())

    def spawn_asteroid():
        asteroid = Asteroid(surface.get_width(), surface.get_height(), 10)
        asteroids.append(asteroid)

    def spawn_projectile(avatar_position):
        projectile = Projectile(avatar_position)
        projectiles.append(projectile)

    # show start screen firt
    main_menu()

    os.environ['SDL_VIDEO_CENTERED'] = '1'  # center the window
    info = pygame.display.Info()
    surface = pygame.display.set_mode(
        (info.current_w, info.current_h),
        pygame.RESIZABLE
    )

    while running:
        surface.fill((0, 0, 0))  # Clear screen with black

        metronome.update()
        player_state.update()

        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        # Draw everything
        if not game_over:
                        # Asteroid spawning logic
            if elapsed_time - last_spawn_time >= 2:  # Spawn every 2 seconds
                spawn_asteroid()
                last_spawn_time = elapsed_time

            #==========================
            #ENKEL DRAWS HIERONDER
            # =============================

            #draw alle ui elementen laatste en on top
            draw_earth_bar(surface)
            # Update and draw asteroids
            for asteroid in asteroids[:]:
                asteroid.update(projectiles)
                asteroid.draw(surface)
                if asteroid.health <= 0:
                    asteroids.remove(asteroid)
                if asteroid.rect.y > surface.get_height():
                    asteroids.remove(asteroid)
                    player_state.take_damage(10)
            # Update and draw projectiles
            for projectile in projectiles[:]:
                projectile.update(projectiles)
                projectile.draw(surface)
            # Update and draw avatar
            keys = pygame.key.get_pressed()
            avatar.update(keys, surface.get_width(), surface.get_height())
            avatar.draw(surface)
            draw_health(surface, font, player_state.health)
            draw_timer(surface, font, elapsed_time)
            draw_shoot_indicator(surface, metronome)

            # Check for game over
            if player_state.health <= 0:
                game_over = True
        else:
            # Display Game Over message
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            restart_text = font.render("Press ESC to quit", True, (255, 255, 255))

            surface.blit(game_over_text, ((surface.get_width() - game_over_text.get_width()) // 2,
                                         (surface.get_height() - game_over_text.get_height()) // 2 - 20))
            surface.blit(restart_text, ((surface.get_width() - restart_text.get_width()) // 2,
                                        (surface.get_height() - restart_text.get_height()) // 2 + 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # checks for escape and quits
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("closed game")
                    running = False

            #dummy schiet functie
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if metronome.can_shoot() == True:
                        spawn_projectile(avatar.get_avatar_position())
                        print("PEWPEW")
                    else:
                        print("FOUTE TIMING JIJ IDIOOT")

# dit is tijdelijk omdat we nog geen damage feature hebben. nu kan je
# de damage-logica triggeren met h
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    player_hit = player_state.take_damage(10)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    player_hit = player_state.paralyse()

        clock.tick(60)  # 60 FPS

    close_game() # cleanly close game

# no touchy, supposed to run
main()
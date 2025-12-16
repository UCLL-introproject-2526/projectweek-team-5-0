import pygame
# import pygame_gui
import time
from ui_elements import *
from metronome import Metronome
from asteroids import Asteroid
from player_state import PlayerState
from avatar import Avatar
from projectile import Projectile

pygame.init()

# =====================================================
# Start Screen with Smaller Rounded Button (Adjusted)
# =====================================================
def draw_rounded_button(surface, text, rect, color, font):
    # Draw the rounded rectangle
    pygame.draw.rect(surface, color, rect, border_radius=25)

    # Render text and position it in the center of the button
    text_surface = font.render(text, True, (255, 255, 255))  # White text for contrast
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def show_start_screen(surface):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 35)  # Slightly reduced font size for the start button

    # Set background color
    surface.fill((0, 0, 0))

    # Title text with smaller font size
    title_font = pygame.font.Font(None, 80)  # Smaller title font size
    title_text = title_font.render("ASTEROID SHOOTER", True, (255, 255, 255))  # White text
    surface.blit(title_text, (surface.get_width() // 2 - title_text.get_width() // 2, surface.get_height() // 5))

    # Start button position and size (centering the button)
    start_button_rect = pygame.Rect(
        (surface.get_width() // 2 - 100, surface.get_height() // 2 + 50),  # Adjusted position for better centering
        (200, 50)  # Adjusted button size to fit text
    )

    # Draw Start button (blue with rounded corners)
    draw_rounded_button(surface, "START GAME", start_button_rect, (0, 128, 255), font)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Check if the user clicked the button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    running = False  # Stop the loop and start the game

            # checks for escape and quits
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("closed menu")
                    pygame.quit()
                    quit()


            # If the screen is resized or fullscreened, re-draw the elements
            if event.type == pygame.VIDEORESIZE:
                surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)  # Dynamically resize surface
                # Re-call the start screen function to re-center UI
                show_start_screen(surface)

        pygame.display.flip()
        clock.tick(60)  # Ensure the screen updates at 60 FPS

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

    # show start screen first
    show_start_screen(surface)

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
            
            # ship collision
            player_state.update_ship_collision(avatar, asteroids)

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
                        if player_state.is_hit == False:
                            spawn_projectile(avatar.get_avatar_position())
                            print("PEWPEW")
                    else:
                        player_state.is_hit = True
                        print("FOUTE TIMING JIJ IDIOOT")

# dit is tijdelijk omdat we nog geen damage feature hebben. nu kan je
# de damage-logica triggeren met h
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    player_hit = player_state.take_damage(10)

        clock.tick(60)  # 60 FPS

    close_game() # cleanly close game

# no touchy, supposed to run
main()
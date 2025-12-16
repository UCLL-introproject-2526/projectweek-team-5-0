
import pygame
import time
from ui_elements import *
from asteroids import Asteroid

pygame.init()

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
    health = 100  # Starting health
    running = True # run game status
    game_over = False
    asteroids = []
    last_spawn_time = 0

    def spawn_asteroid():
        asteroid = Asteroid(surface.get_width(), surface.get_height())
        asteroids.append(asteroid)

    while running:
        surface.fill((0, 0, 0))  # Clear screen with black

        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        # Draw everything
        if not game_over:
            draw_circle(surface)
            draw_health(surface, font, health)
            draw_timer(surface, font, elapsed_time)
            draw_earth_bar(surface)


            # Asteroid spawning logic
            if elapsed_time - last_spawn_time >= 2:  # Spawn every 2 seconds
                spawn_asteroid()
                last_spawn_time = elapsed_time
            
            # Update and draw asteroids
            for asteroid in asteroids[:]:
                asteroid.update()
                asteroid.draw(surface)
                if asteroid.rect.y > surface.get_height():
                    asteroids.remove(asteroid)
                    health -= 10  # Decrease health by 10 if asteroid goes off screen

            # Check for game over
            if health <= 0:
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

        clock.tick(60)  # 60 FPS

    close_game() # cleanly close game

# no touchy, supposed to run
main()

import pygame
import time
from ui_elements import *
from asteroids import Asteroid

pygame.init()

# =====================================================
# deze functie zitten alle dingen in die gerund worden.
# =====================================================
def main():
    surface = create_main_surface()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    start_time = time.time()
    
    health = 100  # Starting health
    asteroids = []
    last_spawn_time = 0

    def spawn_asteroid():
        asteroid = Asteroid(surface.get_width(), surface.get_height())
        asteroids.append(asteroid)
    
    while True:
        surface.fill((0, 0, 0))  # Clear screen with black
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        # Draw everything
        draw_circle(surface)
        draw_health(surface, font, health)
        draw_timer(surface, font, elapsed_time)
        draw_earth_bar(surface)


        # Asteroid spawning logic
        if elapsed_time - last_spawn_time >= 2:  # Spawn every 2 seconds
            spawn_asteroid()
            last_spawn_time = elapsed_time
            
        for asteroid in asteroids[:]:
            asteroid.update()
            asteroid.draw(surface)
            if asteroid.rect.y > surface.get_height():
                asteroids.remove(asteroid)
                health -= 10  # Decrease health by 10 if asteroid goes off screen

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        clock.tick(60)  # 60 FPS


# no touchy, supposed to run
main()
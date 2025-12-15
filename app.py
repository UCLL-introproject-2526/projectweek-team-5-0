import pygame
import time
from ui_elements import *

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
    
    while True:
        surface.fill((0, 0, 0))  # Clear screen with black
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        # Draw everything
        draw_circle(surface)
        draw_health(surface, font, health)
        draw_timer(surface, font, elapsed_time)
        draw_earth_bar(surface)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        clock.tick(60)  # 60 FPS

# no touchy, supposed to run
main()
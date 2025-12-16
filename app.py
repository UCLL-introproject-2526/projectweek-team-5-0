import pygame
import time
from ui_elements import *
from metronome import Metronome

pygame.init()

# =====================================================
# deze functie zitten alle dingen in die gerund worden.
# =====================================================
def main():
    surface = create_main_surface()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    start_time = time.time()

    health = 100  
    metronome = Metronome(bpm=120)

    while True:
        surface.fill((0, 0, 0))  # Clear screen with black

        metronome.update()

        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        # Draw everything
        draw_health(surface, font, health)
        draw_timer(surface, font, elapsed_time)
        draw_earth_bar(surface)
        draw_shoot_indicator(surface, metronome)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # checks for escape and quits
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("closed game")
                    pygame.quit()

            #dummy schiet functie
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if metronome.can_shoot() == True:
                        print("PEWPEW")
                    else:
                        print("FOUTE TIMING JIJ IDIOOT")

        clock.tick(60)  # 60 FPS

# no touchy, supposed to run
main()
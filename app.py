import pygame
pygame.init()
# =====================================================
# deze functie zitten alle dingen in die gerund worden.
# =====================================================
def main():
    surface = create_main_surface()
    draw_circle(surface)
    pygame.display.flip()
    while True:
        pygame.event.pump()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

# ====================================
# hieronder komen alle helper functies
# ====================================
def create_main_surface():
    screen_size = (1024, 768)
    return pygame.display.set_mode(screen_size)

def draw_circle(surface):
    pygame.draw.circle(surface, (255, 0, 0), (512, 384), 50)

# no touchy, supposed to run
main()
import pygame
import random

class Asteroid:
    def __init__(self, screen_width, screen_height):
        # start at random x, above the screen
        self.x = random.randint(0, screen_width - 40)
        self.speed = random.randint(20, 30)
        self.rect = pygame.Rect(self.x, -40, 40, 40)

    def update(self):
        # move straight down
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
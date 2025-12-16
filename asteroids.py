import pygame
import random

class Asteroid:
    def __init__(self, screen_width, screen_height, health):
        # start at random x, above the screen
        self.x = random.randint(0, screen_width - 40)
        self.speed = random.randint(2, 3)
        self.rect = pygame.Rect(self.x, -40, 40, 40)
        self.health = health

    def update(self, projectiles):
        # move straight down
        self.rect.y += self.speed
        if pygame.Rect.collidelist(self.rect, projectiles) != -1:
            projectiles.remove(projectiles[pygame.Rect.collidelist(self.rect, projectiles)])
            self.damage(10)

    def damage(self, damage):
        self.health -= damage

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
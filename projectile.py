import pygame
import math

class Projectile:
    def __init__(self, player_position):
        # start at player position
        self.x = player_position[0]
        self.y = player_position[1]
        self.speed = -4
        self.rect = pygame.Rect(self.x, self.y, 20, 20)

    def update(self, projectiles):
        # move straight up
        if self.rect.y < 0:
            projectiles.remove(self)
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 100, 100), self.rect)
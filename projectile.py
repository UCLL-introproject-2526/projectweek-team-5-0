import pygame
import math

class Projectile:
    def __init__(self, player_position, angle):
        # start at player position (tip of the avatar ideally)
        self.rect = pygame.Rect(player_position[0], player_position[1], 10, 10)

        self.speed = 15
        rad = math.radians(angle + 90)

        # velocity based on angle
        self.vx = math.cos(rad) * self.speed
        self.vy = -math.sin(rad) * self.speed  # negative because pygame's y-axis grows downward

    def update(self, projectiles, screen_width, screen_height):
        # move in direction of vx, vy
        self.rect.x += self.vx
        self.rect.y += self.vy

        # remove if off screen
        if (self.rect.right < 0 or self.rect.left > screen_width or
            self.rect.bottom < 0 or self.rect.top > screen_height):
            projectiles.remove(self)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 100, 100), self.rect)
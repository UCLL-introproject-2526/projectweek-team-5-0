import pygame
import math
import os

class Projectile:

    projectile_sprite = None
    
    @classmethod
    def load_sprite(cls):
        if cls.projectile_sprite is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            sprite_path = os.path.join(script_dir, "sprites/projectile/projectile.png") 
            cls.projectile_sprite = pygame.image.load(sprite_path).convert_alpha()
            cls.projectile_sprite = pygame.transform.scale(cls.projectile_sprite, (50, 50))

    def __init__(self, player_position, angle):
        Projectile.load_sprite() 
        self.rect = pygame.Rect(player_position[0], player_position[1], 10, 10)
        self.angle = angle
        self.speed = 15
        rad = math.radians(angle + 90)

        # velocity based on angle
        self.vx = math.cos(rad) * self.speed
        self.vy = -math.sin(rad) * self.speed

    def update(self, projectiles, screen_width, screen_height):
        # move in direction of vx, vy
        self.rect.x += self.vx
        self.rect.y += self.vy

        # remove if off screen
        if (self.rect.right < 0 or self.rect.left > screen_width or
            self.rect.bottom < 0 or self.rect.top > screen_height):
            projectiles.remove(self)

    def draw(self, surface):
        rotated = pygame.transform.rotate(Projectile.projectile_sprite, self.angle-90)
        rect = rotated.get_rect(center=self.rect.center)
        surface.blit(rotated, rect)
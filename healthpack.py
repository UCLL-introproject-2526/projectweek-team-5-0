import pygame
import random
import os

class HealthPack:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width - 30)
        self.y = -30
        self.size = 30
        self.speed = 2  # Slower than asteroids
        
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sprite_path = os.path.join(script_dir, "sprites", "items", "MedPak3_Pixel.png")
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
    
    def update(self):
        # Move down
        self.rect.y += self.speed
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
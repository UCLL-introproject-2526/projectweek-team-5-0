import pygame
import random
import os

class Asteroid:
    def __init__(self, screen_width, screen_height, health):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sprite_folder = os.path.join(script_dir, "sprites", "asteroid")

        # Get all image files
        sprite_files = [f for f in os.listdir(sprite_folder) if f.endswith('.png')]
        
        # Pick random sprite and load it
        chosen_sprite = random.choice(sprite_files)
        sprite_path = os.path.join(sprite_folder, chosen_sprite)
        self.image = pygame.image.load(sprite_path).convert_alpha()
        
        # Scale to 40x40
        self.image = pygame.transform.scale(self.image, (40, 40))
        
        # NOW create rect from image (after image exists!)
        self.rect = self.image.get_rect()
        
        # Position
        self.x = random.randint(0, screen_width - 40)
        self.speed = random.randint(2, 3)
        self.rect.x = self.x
        self.rect.y = -40
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
        surface.blit(self.image, self.rect)
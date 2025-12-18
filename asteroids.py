import pygame
import random
import os

class Asteroid:
    def __init__(self, screen_width, screen_height, health, speed):
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
        self.speed = speed
        self.rect.x = self.x
        self.rect.y = -40

        self.health = health

    def update(self):
        # move straight down
        self.rect.y += self.speed


    def damage(self, damage):
        self.health -= damage

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_asteroid_position(self):
        position = [self.rect.x + 20, self.rect.y - 20]
        return position

class Splitter:
    def __init__(self, spawn_offset_x, spawn_offset_y, health, size, asteroid):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sprite_folder = os.path.join(script_dir, "sprites", "asteroid")

        # Get all image files
        sprite_files = [f for f in os.listdir(sprite_folder) if f.endswith('.png')]

        # Pick random sprite and load it
        chosen_sprite = random.choice(sprite_files)
        sprite_path = os.path.join(sprite_folder, chosen_sprite)
        self.image = pygame.image.load(sprite_path).convert_alpha()

        # Scale to size
        self.image = pygame.transform.scale(self.image, (size, size))

        # NOW create rect from image (after image exists!)
        self.rect = self.image.get_rect()

        # Position
        self.x = (asteroid.get_asteroid_position())[0]
        self.y = (asteroid.get_asteroid_position())[1]
        self.speed = asteroid.speed - 1
        self.rect.x = self.x + spawn_offset_x
        self.rect.y = self.y + spawn_offset_y

        self.health = health

    def update(self):
        # move straight down
        self.rect.y += self.speed

    def damage(self, damage):
        self.health -= damage

    def draw(self, surface):
        surface.blit(self.image, self.rect)
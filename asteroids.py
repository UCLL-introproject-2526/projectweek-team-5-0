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
        self.pos_y = -40.0                 # NEW: track float position
        self.rect.x = self.x
        self.rect.y = int(self.pos_y)

        self.health = health

    def update(self):
        # move straight down using float position
        self.pos_y += self.speed
        self.rect.y = int(self.pos_y)      # update rect from float

    def damage(self, damage):
        self.health -= damage

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_asteroid_position(self):
        # return center-ish position
        return [self.rect.x + 20, self.rect.y - 20]


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
        self.x = asteroid.get_asteroid_position()[0]
        self.y = asteroid.get_asteroid_position()[1]

        # --- CHANGE: clamp speed so it's never 0 ---
        # If asteroid.speed == 1, this gives 0.5 instead of 0
        self.speed = max(0.5, asteroid.speed - 0.5)

        # NEW: track float position for smooth movement
        self.pos_y = float(self.y + spawn_offset_y)
        self.rect.x = self.x + spawn_offset_x
        self.rect.y = int(self.pos_y)

        self.health = health

    def update(self):
        # move straight down using float position
        self.pos_y += self.speed
        self.rect.y = int(self.pos_y)

    def damage(self, damage):
        self.health -= damage

    def draw(self, surface):
        surface.blit(self.image, self.rect)
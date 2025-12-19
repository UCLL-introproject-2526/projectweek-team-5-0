import pygame
import random
import os

class Asteroid:
    destroy_sound = None
    
    @classmethod
    def load_sound(cls):
        """Load destroy sound once for all asteroids"""
        if cls.destroy_sound is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(script_dir, "sfx", "asteroidDies.wav")
            cls.destroy_sound = pygame.mixer.Sound(sound_path)
            cls.destroy_sound.set_volume(0.1)
            print("Asteroid destroy sound loaded")

    def __init__(self, screen_width, screen_height, health, speed, spawn_time):
        Asteroid.load_sound()
        self.spawn_time = spawn_time

        if self.spawn_time >= 180:
            self.damage_value = 100
        else:
            self.damage_value = 10
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
        max_spawn_x = int(screen_width * 0.92) - 40
        self.x = random.randint(0, max_spawn_x)
        self.speed = speed
        self.pos_y = -40.0 
        self.rect.x = self.x
        self.rect.y = int(self.pos_y)

        self.health = health

    def play_destroy_sound(self):
        if Asteroid.destroy_sound:
            Asteroid.destroy_sound.play()

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
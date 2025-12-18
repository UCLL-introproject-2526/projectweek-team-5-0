import pygame
import os
import random

class PowerUpItem:
    sprite = None
    pickup_sound = None

    @classmethod
    def load_assets(cls):
        if cls.sprite is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            try:
                img_path = os.path.join(script_dir, "sprites/upgrades/ShootGun.png")
                cls.sprite = pygame.image.load(img_path).convert_alpha()
            except:
                cls.sprite = pygame.Surface((30, 30))
                cls.sprite.fill((0, 255, 255)) # Cyan box fallback
            
            cls.sprite = pygame.transform.scale(cls.sprite, (30, 30))

        if cls.pickup_sound is None:
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                sound_path = os.path.join(script_dir, "sfx/powerup.wav")
                cls.pickup_sound = pygame.mixer.Sound(sound_path)
                cls.pickup_sound.set_volume(0.4)
            except:
                pass

    def __init__(self, screen_width, screen_height):
        PowerUpItem.load_assets()
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(random.randint(0, screen_width - self.width), -40, self.width, self.height)
        self.speed = 3
        self.float_y = float(self.rect.y)

    def update(self):
        self.float_y += self.speed
        self.rect.y = int(self.float_y)

    def draw(self, surface):
        surface.blit(PowerUpItem.sprite, self.rect)

    def play_sound(self):
        if PowerUpItem.pickup_sound:
            PowerUpItem.pickup_sound.play()
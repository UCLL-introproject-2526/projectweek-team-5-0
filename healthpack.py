import pygame
import random
import os

class HealthPack:

    pickup_sound = None
    
    @classmethod
    def load_sound(cls):
        if cls.pickup_sound is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(script_dir, "sfx", "healthpack.wav")
            cls.pickup_sound = pygame.mixer.Sound(sound_path)
            cls.pickup_sound.set_volume(0.5)
            
    def __init__(self, screen_width, screen_height):
        HealthPack.load_sound()
        self.x = random.randint(0, screen_width - 30)
        self.y = -30
        self.size = 30
        self.speed = 2  # Slower than asteroids
        
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sprite_path = os.path.join(script_dir, "sprites", "items", "MedPak3_Pixel.png")
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))

    def play_pickup_sound(self):
        if HealthPack.pickup_sound:
            HealthPack.pickup_sound.play()
    
    def update(self):
        # Move down
        self.rect.y += self.speed
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
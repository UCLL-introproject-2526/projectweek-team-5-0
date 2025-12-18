import pygame
import math
import os

class Projectile:

    projectile_sprite = None
    shoot_sound = None
    shotgun_sound = None
    
    @classmethod
    def load_sprite(cls):
        if cls.projectile_sprite is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            sprite_path = os.path.join(script_dir, "sprites/projectile/projectile.png") 
            cls.projectile_sprite = pygame.image.load(sprite_path).convert_alpha()
            cls.projectile_sprite = pygame.transform.scale(cls.projectile_sprite, (50, 50))

    @classmethod
    def load_sound(cls):  # ADD THIS METHOD
        if cls.shoot_sound is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(script_dir, "sfx/laserShoot.wav")
            cls.shoot_sound = pygame.mixer.Sound(sound_path)
            cls.shoot_sound.set_volume(0.3)

    @classmethod
    def load_shotgun_sound(cls):  # ADD THIS METHOD
        if cls.shotgun_sound is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(script_dir, "sfx/laserShoot2.wav")
            cls.shotgun_sound = pygame.mixer.Sound(sound_path)
            cls.shotgun_sound.set_volume(0.5)


    def __init__(self, player_position, angle, is_shotgun=False):
        Projectile.load_sprite()
        Projectile.load_sound() 
        Projectile.load_shotgun_sound() 
        self.rect = pygame.Rect(player_position[0], player_position[1], 10, 10)
        self.angle = angle
        self.speed = 15
        rad = math.radians(angle + 90)

        # velocity based on angle
        self.vx = math.cos(rad) * self.speed
        self.vy = -math.sin(rad) * self.speed

        #SFX
        if is_shotgun:
            if Projectile.shotgun_sound:
                Projectile.shotgun_sound.play()
        else:
            if Projectile.shoot_sound:
                Projectile.shoot_sound.play()

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
import pygame
from projectile import Projectile

class CombatModifier:
    def __init__(self):
        self.active = False
        self.start_time = 0
        self.duration = 15000  # 15 seconds

    def activate(self, metronome):
        self.active = True
        self.start_time = pygame.time.get_ticks()
        print("SHOTGUN MODE: Only shoot on beats 1, 3, 5, 7!")

    def update(self, metronome):
        if self.active:
            if pygame.time.get_ticks() - self.start_time >= self.duration:
                self.active = False
                print("SHOTGUN DEACTIVATED")

    def is_beat_forbidden(self, current_beat):
        # When active, can only shoot on ODD beats (1, 3, 5, 7)
        if self.active:
            return current_beat % 2 == 0  # Forbid even beats (0, 2, 4, 6)
        return False

    def create_shots(self, avatar, metronome):
        shots = []
        base_angle = avatar.angle
        gun_pos = avatar.get_gun_position()

        # Shotgun on all allowed beats when modifier is active
        if self.active:
            angles = [base_angle - 20, base_angle - 10, base_angle, base_angle + 10, base_angle + 20]
            for i, a in enumerate(angles):
                # Only play sound on first projectile
                shots.append(Projectile(gun_pos, a, is_shotgun=(i == 0)))
        else:
            shots.append(Projectile(gun_pos, base_angle, is_shotgun=False))
        
        return shots
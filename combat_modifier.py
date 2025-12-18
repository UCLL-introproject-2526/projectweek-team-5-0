import pygame
from projectile import Projectile

class CombatModifier:
    def __init__(self):
        self.active = False
        self.start_time = 0
        self.duration = 10000 

    def activate(self, metronome):
        # We don't change metronome rhythm anymore
        self.active = True
        self.start_time = pygame.time.get_ticks()
        print("MODIFIER ACTIVE: Beat 8 Disabled, Beat 7 Shotgun")

    def update(self, metronome):
        if self.active:
            if pygame.time.get_ticks() - self.start_time >= self.duration:
                self.active = False
                print("MODIFIER DEACTIVATED")

    def is_beat_forbidden(self, current_beat):
        # Prevent shooting on the 8th beat (index 7) when active
        return self.active and current_beat == 7

    def create_shots(self, avatar, metronome):
        shots = []
        base_angle = avatar.angle
        gun_pos = avatar.get_gun_position()

        # Trigger shotgun on beat 6 (The last allowed beat)
        is_shotgun_beat = metronome.current_beat == 6

        if self.active and is_shotgun_beat:
            angles = [base_angle - 20, base_angle - 10, base_angle, base_angle + 10, base_angle + 20]
            for a in angles:
                shots.append(Projectile(gun_pos, a))
        else:
            shots.append(Projectile(gun_pos, base_angle))
        
        return shots
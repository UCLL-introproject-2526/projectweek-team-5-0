# metronome.py
import pygame
import numpy as np
import os

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
script_dir = os.path.dirname(os.path.abspath(__file__))
accent_beat = pygame.mixer.Sound(os.path.join(script_dir, "sfx/dance_kick3-92807.wav")) 
regular_beat = pygame.mixer.Sound(os.path.join(script_dir, "sfx/dance_kick3-92807.wav"))

accent_beat.set_volume(1)
regular_beat.set_volume(1)

class Metronome:
    def __init__(self, bpm=120):
        self.bpm = bpm
        self.beat_interval = 60000 / bpm
        self.current_beat = 0

        current_time = pygame.time.get_ticks()

        # Pretend a beat just happened one interval ago
        # This makes the timing calculations work correctly from the start
        self.last_beat_time = current_time - self.beat_interval
        self.next_beat_time = current_time  # First beat will happen immediately

        self.shoot_tolerance = 100 

    def update(self, combat_mod=None):
        current_time = pygame.time.get_ticks()

        if current_time >= self.next_beat_time:
            # Check if this beat should be silent
            is_silent = False
            if combat_mod and combat_mod.is_beat_forbidden(self.current_beat):
                is_silent = True

            # Only play sound if NOT silent
            if not is_silent:
                if self.current_beat == 0 or self.current_beat == 4:
                    accent_beat.play()
                else:
                    regular_beat.play()

            # Update timing
            self.last_beat_time = current_time
            self.next_beat_time = current_time + self.beat_interval

            self.current_beat = (self.current_beat + 1) % 8

    def can_shoot(self):
        """Check if current time is within valid shooting window"""
        current_time = pygame.time.get_ticks()
        time_since_last = current_time - self.last_beat_time
        time_until_next = self.next_beat_time - current_time

        min_time = min(time_since_last, time_until_next)

        return min_time <= self.shoot_tolerance
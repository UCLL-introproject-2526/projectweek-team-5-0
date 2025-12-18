# metronome.py
import pygame
import numpy as np

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

def create_click_sound(frequency, duration=0.1):
    sample_rate = 22050
    n_samples = int(sample_rate * duration)

    t = np.linspace(0, duration, n_samples, False)
    wave = np.sin(frequency * t * 2 * np.pi)

    envelope = np.linspace(1, 0, n_samples)
    wave = wave * envelope

    wave = (wave * 32767).astype(np.int16)
    stereo_wave = np.column_stack((wave, wave))

    return pygame.sndarray.make_sound(stereo_wave)

# Create sounds
accent_beat = create_click_sound(300)
regular_beat = create_click_sound(300)

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
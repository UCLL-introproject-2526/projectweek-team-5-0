# dit file doet
# - de health decreasing logic
# een flag voor 'has been hit' met een timer voor paralyzation
# sound effect on getting hit
# player_state.py
# player_state.py
import pygame
import numpy as np
import os
from avatar import Avatar

class PlayerState:
    def __init__(self):
        """
        Manages player state including hit detection and health
        """
        self.is_hit = False  # Flag indicating if player was just hit
        self.hit_time = 0  # When the hit occurred
        self.hit_duration = 5000  # How long hit state lasts (ms)

        self.health = 100  # Starting health
        self.max_health = 100

        script_dir = os.path.dirname(os.path.abspath(__file__))
        sound_path = os.path.join(script_dir, "sfx/hitHurt.wav")
        # Try to load hit sound
        self.hit_sound = pygame.mixer.Sound(sound_path)
        self.hit_sound.set_volume(1)
        print("Hit sound loaded successfully from hit_sound.wav")

    def _create_fallback_sound(self):
        """Create a simple hit sound if WAV file is missing"""
        sample_rate = 22050
        duration = 0.2  # Increased from 0.15
        n_samples = int(sample_rate * duration)

        t = np.linspace(0, duration, n_samples, False)
        # Harsh downward sweep for hit sound
        freq_start = 800  # Higher frequency
        freq_end = 200
        frequency = np.linspace(freq_start, freq_end, n_samples)

        wave = np.sin(2 * np.pi * frequency * t)
        envelope = np.linspace(1, 0, n_samples)
        wave = wave * envelope

        # Increased volume from 0.3 to 0.8
        wave = (wave * 32767 * 0.8).astype(np.int16)
        stereo_wave = np.column_stack((wave, wave))

        sound = pygame.sndarray.make_sound(stereo_wave)
        sound.set_volume(1.0)  # Max volume
        return sound

    def take_damage(self, damage_amount=10):
        """
        Called when player (earth) takes damage
        
        damage_amount: How much health to subtract (default 10)
        Returns: True if player died, False otherwise
        """
        current_time = pygame.time.get_ticks()
        
        # Apply damage
        self.health -= damage_amount
        
        # Clamp health to 0 minimum
        if self.health < 0:
            self.health = 0
        
        # Play sound
        print(f"Attempting to play hit sound: {self.hit_sound}")
        if self.hit_sound:
            self.hit_sound.play()
            print("Hit sound played!")
        else:
            print("ERROR: No hit sound to play!")
        
        print(f"Earth hit! Health: {self.health}/{self.max_health}")
        
        # Return True if player died
        return self.health <= 0
    
    def paralyse(self):
        # Paralyzes the player(ship)

        # Prevent taking damage while already in hit state (invincibility frames)
        if self.is_hit:
            print("Can't take damage - still in hit state")
            return False
        
        # paralyze
        if self.is_hit == False:
            self.is_hit = True
            print(f"Ship paralysed! Keep your shots in scync capt\'n")
        
        # Play sound
        print(f"Attempting to play hit sound: {self.hit_sound}")
        if self.hit_sound:
            self.hit_sound.play()
            print("Hit sound played!")
        else:
            print("ERROR: No hit sound to play!")

        # Play sound
        print(f"Attempting to play hit sound: {self.hit_sound}")
        if self.hit_sound:
            self.hit_sound.play()
            print("Hit sound played!")
        else:
            print("ERROR: No hit sound to play!")

        print(f"Player hit! Health: {self.health}/{self.max_health}")

        # Return True if player died
        return self.health <= 0

    def update(self):
        """
        Call every frame to update hit state
        """
        if self.is_hit:
            current_time = pygame.time.get_ticks()

            # Check if hit duration has passed
            if current_time - self.hit_time >= self.hit_duration:
                self.is_hit = False
                print("Hit state ended - player vulnerable again")

    def update_ship_collision(self, avatar, astroidlist):
        if pygame.Rect.collidelist(avatar.rect, astroidlist) != -1:
            self.is_hit = True
            print("You've been hit")

    def is_alive(self):
        """Check if player is still alive"""
        return self.health > 0

    def heal(self, heal_amount):
        """Heal the player"""
        self.health = min(self.health + heal_amount, self.max_health)
        print(f"Player healed! Health: {self.health}/{self.max_health}")

    def reset(self):
        """Reset player state for new game"""
        self.health = self.max_health
        self.is_hit = False
        self.hit_time = 0
        print("Player state reset")
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

# paralisys 
    paralisys_sprites = None
    
    @classmethod
    def load_paralisys_sprites(cls):
        """Load all paralisys sprites from the sprites/paralisys folder"""
        if cls.paralisys_sprites is None:
            cls.paralisys_sprites = []
            script_dir = os.path.dirname(os.path.abspath(__file__))
            paralisys_folder = os.path.join(script_dir, "sprites", "paralyze")
            
            try:
                for filename in os.listdir(paralisys_folder):
                    if filename.endswith(('.png', '.jpg', '.jpeg')):
                        image_path = os.path.join(paralisys_folder, filename)
                        sprite = pygame.image.load(image_path).convert_alpha()
                        cls.paralisys_sprites.append(sprite)
                
                print(f"Loaded {len(cls.paralisys_sprites)} paralisys sprites")
            except FileNotFoundError:
                print(f"Warning: {paralisys_folder} not found - no paralisys effects")
                cls.paralisys_sprites = []

    def __init__(self):
        """
        Manages player state including hit detection and health
        """
        PlayerState.load_paralisys_sprites()

        self.is_hit = False  # Flag indicating if player was just hit
        self.hit_time = 0  # When the hit occurred
        self.hit_duration = 1000  # How long hit state lasts (ms)

        self.health = 100  # Starting health
        self.max_health = 100

        script_dir = os.path.dirname(os.path.abspath(__file__))
        sound_path = os.path.join(script_dir, "sfx/hitHurt.wav")
        # Try to load hit sound
        self.hit_sound = pygame.mixer.Sound(sound_path)
        self.hit_sound.set_volume(1)
        print("Hit sound loaded successfully from hit_sound.wav")

        #paralisys 
        self.paralisys_frame_count = 0
        self.current_paralisys = None  # Currently displayed paralisys sprite

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
    
    def trigger_paralisys(self):
        """Call this when the player gets paralysed"""
        if PlayerState.paralisys_sprites:
            self.current_paralisys = (PlayerState.paralisys_sprites)
            self.is_firing = True
            self.fire_frame_count = self.hit_duration  # How long hit state lasts (ms)
    
    def paralyse(self):
        # Paralyzes the player(ship)

        # Prevent taking damage while already in hit state (invincibility frames)
        if self.is_hit:
            print("Can't take damage - still in hit state")
            return False
        
        # paralyze
        if self.is_hit == False:
            self.trigger_paralisys
            self.hit_time = pygame.time.get_ticks()
            self.is_hit = True
            print(f"Ship paralysed! Keep your shots in scync capt\'n")
        
        # Play sound (change to a paralyze sound)
        print(f"Attempting to play hit sound: {self.hit_sound}")
        if self.hit_sound:
            self.hit_sound.play()
            print("Hit sound played!")
        else:
            print("ERROR: No hit sound to play!")

        # Draw flame sprite if firing
    def draw_paralisys(self, surface):
        if self.is_hit and self.current_paralisys:
            paralisys_width = 70
            paralisys_height = 70
            scaled_paralisys = pygame.transform.scale(self.current_paralisys, (paralisys_width, paralisys_height))

            surface.blit(scaled_paralisys)


    def update(self):
        """
        Call every frame to update hit state
        """
        if self.is_hit:
            current_time = pygame.time.get_ticks()
            # Check if hit duration has passed
            if current_time >= self.hit_time + self.hit_duration:
                self.is_hit = False
                print("Hit state ended - player vulnerable again")
        print(pygame.time.get_ticks())
        print(self.hit_time)

    def update_ship_collision(self, avatar, astroidlist):
        if self.is_hit:
            return  # invincibility frames active

        if pygame.Rect.collidelist(avatar.rect, astroidlist) != -1:
                self.paralyse()
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

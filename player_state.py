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

# paralyse
    paralyse_sprites = None

    @classmethod
    def load_paralyse_sprites(cls):
        """Load all paralyse sprites from the sprites/paralyze folder"""
        if cls.paralyse_sprites is None:
            cls.paralyse_sprites = []
            script_dir = os.path.dirname(os.path.abspath(__file__))
            paralyse_folder = os.path.join(script_dir, "sprites", "paralyze")

            try:
                frame_files = sorted([f for f in os.listdir(paralyse_folder) if f.endswith(('.png', '.jpg', '.jpeg'))])
                for filename in frame_files:
                    image_path = os.path.join(paralyse_folder, filename)
                    sprite = pygame.image.load(image_path).convert_alpha()
                    cls.paralyse_sprites.append(sprite)

                print(f"Loaded {len(cls.paralyse_sprites)} paralyse sprites")
            except FileNotFoundError:
                print(f"Warning: {paralyse_folder} not found - no paralyse effects")
                cls.paralyse_sprites = []

    def __init__(self):
        PlayerState.load_paralyse_sprites()

        self.is_hit = False  # Flag indicating if player was just hit
        self.hit_time = 0  # When the hit occurred
        self.hit_duration = 1000  # How long hit state lasts (ms)

        self.health = 100  # Starting health
        self.max_health = 100

        script_dir = os.path.dirname(os.path.abspath(__file__))

    # Sound for asteroid hitting earth
        sound_path = os.path.join(script_dir, "sfx/hitHurt.wav")
        self.hit_sound = pygame.mixer.Sound(sound_path)
        self.hit_sound.set_volume(0.5)
        paralyze_sound_path = os.path.join(script_dir, "sfx/paralyze.wav")
        self.paralyze_sound = pygame.mixer.Sound(paralyze_sound_path)
        self.paralyze_sound.set_volume(0.5)

        #paralyse
        self.current_paralyse_frame = 0
        self.paralyse_frame_speed = 3
        self.paralyse_frame_count = 0

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

    def trigger_paralyse(self):
        if PlayerState.paralyse_sprites:
            self.current_paralyse = (PlayerState.paralyse_sprites)
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
            self.trigger_paralyse
            self.hit_time = pygame.time.get_ticks()
            self.is_hit = True

        # Play sound (change to a paralyze sound)
        if self.paralyze_sound:
                self.paralyze_sound.play()


        # Draw flame sprite if firing
    def draw_paralyse(self, surface, avatar):
        if self.is_hit and PlayerState.paralyse_sprites:
            # Cycle through frames
            if self.current_paralyse_frame < len(PlayerState.paralyse_sprites):
                current_sprite = PlayerState.paralyse_sprites[self.current_paralyse_frame]

                # Scale and position over avatar
                paralyse_width = 70
                paralyse_height = 70
                scaled_paralyse = pygame.transform.scale(current_sprite, (paralyse_width, paralyse_height))

                # Center on avatar
                paralyse_x = avatar.rect.centerx - paralyse_width // 2
                paralyse_y = avatar.rect.centery - paralyse_height // 2

                surface.blit(scaled_paralyse, (paralyse_x, paralyse_y))


    def update(self):
        """
        Call every frame to update hit state
        """
        if self.is_hit:
            current_time = pygame.time.get_ticks()
            # Check if hit duration has passed

            self.paralyse_frame_count += 1
            if self.paralyse_frame_count >= self.paralyse_frame_speed:
                self.paralyse_frame_count = 0
                self.current_paralyse_frame += 1

                if self.current_paralyse_frame >= len(PlayerState.paralyse_sprites):
                    self.current_paralyse_frame = 0


            if current_time >= self.hit_time + self.hit_duration:
                self.is_hit = False
                print("Hit state ended - player vulnerable again")

    def update_ship_collision(self, avatar, astroid_list, splitter_list):
        if self.is_hit:
            return  # invincibility frames active

        if pygame.Rect.collidelist(avatar.rect, astroid_list) != -1 or pygame.Rect.collidelist(avatar.rect, splitter_list) != -1:
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

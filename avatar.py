import pygame
import math
import random
import os

class Avatar:

    flame_sprites = None
    
    @classmethod
    def load_flame_sprites(cls):
        """Load all flame sprites from the sprites/flames folder"""
        if cls.flame_sprites is None:
            cls.flame_sprites = []
            script_dir = os.path.dirname(os.path.abspath(__file__))
            flame_folder = os.path.join(script_dir, "sprites", "flames")
            
            try:
                for filename in os.listdir(flame_folder):
                    if filename.endswith(('.png', '.jpg', '.jpeg')):
                        image_path = os.path.join(flame_folder, filename)
                        sprite = pygame.image.load(image_path).convert_alpha()
                        cls.flame_sprites.append(sprite)
                
                print(f"Loaded {len(cls.flame_sprites)} flame sprites")
            except FileNotFoundError:
                print(f"Warning: {flame_folder} not found - no flame effects")
                cls.flame_sprites = []

    def __init__(self, screen_width, screen_height):
        Avatar.load_flame_sprites() #enkel bij eerste shoot nodig, init

        # start at center bottom
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect((screen_width - self.width) // 2, screen_height - self.height - 10, self.width, self.height)
        self.speed = 5

        self.vx = 0  # Velocity X
        self.vy = 0  # Velocity Y
        self.acceleration = 1.5
        self.friction = 0.9
        self.max_speed = 8

        self.base_image = pygame.image.load('sprites/player/player.png').convert_alpha()
        self.base_image = pygame.transform.scale(self.base_image, (self.width, self.height))
        self.image = self.base_image

        #VUUR 
        self.is_firing = False   #A FLAG
        self.fire_duration = 8  # How many frames the flame shows
        self.fire_frame_count = 0
        self.current_flame = None  # Currently displayed flame sprite

    def trigger_fire(self):
        """Call this when the avatar shoots"""
        if Avatar.flame_sprites:
            self.current_flame = random.choice(Avatar.flame_sprites)
            self.is_firing = True
            self.fire_frame_count = self.fire_duration

    def update(self, keys, screen_width, screen_height):
        
        if keys[pygame.K_LEFT]:
            self.vx -= self.acceleration
        if keys[pygame.K_RIGHT]:
            self.vx += self.acceleration
        if keys[pygame.K_UP]:
            self.vy -= self.acceleration
        if keys[pygame.K_DOWN]:
            self.vy += self.acceleration

        self.vx *= self.friction
        self.vy *= self.friction

        # Cap maximum speed
        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > self.max_speed:
            self.vx = (self.vx / speed) * self.max_speed
            self.vy = (self.vy / speed) * self.max_speed    

        # Stop completely if moving very slowly (prevents tiny drifting)
        if abs(self.vx) < 0.1:
            self.vx = 0
        if abs(self.vy) < 0.1:
            self.vy = 0
        
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Bouncy boi - actually bounces!
        if self.rect.left < 0:
            self.rect.left = 0
            self.vx = -self.vx * 0.3  # Reverse and dampen (70% energy retained)
        if self.rect.right > screen_width:
            self.rect.right = screen_width
            self.vx = -self.vx * 0.3
        if self.rect.top < 0:
            self.rect.top = 0
            self.vy = -self.vy * 0.3
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.vy = -self.vy * 0.3

        # Update fire animation
        if self.is_firing:
            self.fire_frame_count -= 1
            if self.fire_frame_count <= 0:
                self.is_firing = False

        #Rotatation toward mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        self.angle = math.degrees(math.atan2(-dy, dx)) - 90  

        #Rotate the image
        self.image = pygame.transform.rotate(self.base_image, self.angle)

        #Update rect to new image size and keep center
        self.rect = self.image.get_rect(center=self.rect.center) 
            
    def get_avatar_position(self):
        #gets avatar position and returns it
        avatar_position = [self.rect.x + (self.width/4), self.rect.y + (self.height/2)]
        #the division ensures the middle of the avatar is returned
        return avatar_position
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

        # Draw flame sprite if firing
        if self.is_firing and self.current_flame:
            # Scale flame to fit (adjust size as needed)
            flame_width = 30
            flame_height = 30
            scaled_flame = pygame.transform.scale(self.current_flame, (flame_width, flame_height))
            
            # Position flame above avatar, centered
            flame_x = self.rect.centerx - flame_width // 2
            flame_y = self.rect.top - flame_height + 10  # Overlap slightly with ship
            
            # Optional: fade out flame as animation ends
            if self.fire_frame_count < 4:
                # Make flame semi-transparent in last few frames
                scaled_flame.set_alpha(int(255 * (self.fire_frame_count / 4)))
            
            surface.blit(scaled_flame, (flame_x, flame_y))
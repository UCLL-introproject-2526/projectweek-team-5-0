import pygame
import random
import os

class HealthPack:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width - 30)
        self.y = -30
        self.size = 30
        self.speed = 2  # Slower than asteroids
        
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
        # Visual properties for green orb
        self.color = (50, 255, 50)  # Bright green
        self.glow_color = (100, 255, 100, 100)  # Light green glow
        
        # Animation
        self.pulse = 0
        self.pulse_speed = 0.1
    
    def update(self):
        # Move down
        self.rect.y += self.speed
        
        # Pulse animation
        self.pulse += self.pulse_speed
        if self.pulse > 1 or self.pulse < 0:
            self.pulse_speed = -self.pulse_speed
    
    def draw(self, surface):
        # Calculate pulsing size
        pulse_size = int(self.size * (0.9 + 0.1 * self.pulse))
        
        # Draw glow effect (outer circle)
        glow_radius = pulse_size + 5
        pygame.draw.circle(surface, (100, 255, 100), self.rect.center, glow_radius)
        
        # Draw main orb
        pygame.draw.circle(surface, self.color, self.rect.center, pulse_size // 2)
        
        # Draw inner highlight
        highlight_offset = pulse_size // 6
        highlight_pos = (self.rect.centerx - highlight_offset, self.rect.centery - highlight_offset)
        pygame.draw.circle(surface, (200, 255, 200), highlight_pos, pulse_size // 4)
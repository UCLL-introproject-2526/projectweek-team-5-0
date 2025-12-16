import pygame
import math

class Avatar:
    def __init__(self, screen_width, screen_height):
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
            
    def get_avatar_position(self):
        #gets avatar position and returns it
        avatar_position = [self.rect.x + (self.width/4), self.rect.y + (self.height/2)]
        #the division ensures the middle of the avatar is returned
        return avatar_position
    
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), self.rect)
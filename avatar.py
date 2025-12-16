import pygame
import math

class Avatar:
    def __init__(self, screen_width, screen_height):
        # start at center bottom
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect((screen_width - self.width) // 2, screen_height - self.height - 10, self.width, self.height)
        self.speed = 5

    def update(self, keys, screen_width, screen_height):
        #Move left or right with arrow keys

        #Horizontal movement
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed

        #Vertical movement
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < screen_height:
            self.rect.y += self.speed
            
    def get_avatar_position(self):
        #gets avatar position and returns it
        avatar_position = [self.rect.x + (self.width/4), self.rect.y + (self.height/2)]
        #the division ensures the middle of the avatar is returned
        return avatar_position
    
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), self.rect)
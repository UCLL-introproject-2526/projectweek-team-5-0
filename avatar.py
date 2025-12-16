import pygame

class Avatar:
    def __init__(self, screen_width, screen_height):
        # start at center bottom
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect((screen_width - self.width) // 2, screen_height - self.height - 10, self.width, self.height)
        self.speed = 5

    def update(self, keys, screen_width):
        #Move left or right with arrow keys
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
    
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), self.rect)
import pygame
import math

class Avatar:
    def __init__(self, screen_width, screen_height):
        # start at center bottom
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect((screen_width - self.width) // 2, screen_height - self.height - 10, self.width, self.height)
        self.speed = 5

        #Load PNG as the base image
        self.base_image = pygame.image.load("player.png").convert_alpha()

        #Fit to desired size
        self.base_image = pygame.transform.scale(self.base_image, (self.width, self.height))

        #Current image to be drawn
        self.image = self.base_image

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

        #Rotation toward mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))

        #Rotate the image
        self.image = pygame.transform.rotate(self.base_image, angle - 90)
        
        #Update rect to image size and keep center
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_avatar_position(self):
        #gets avatar position and returns it
        avatar_position = [self.rect.x + (self.width/4), self.rect.y + (self.height/2)]
        #the division ensures the middle of the avatar is returned
        return avatar_position
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    

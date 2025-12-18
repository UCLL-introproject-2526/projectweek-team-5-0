import os
import pygame

class Explosion:

    def __init__(self, x, y):
        self.frames = []
        #path met os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(script_dir, "sprites", "boom")
        #put image on self location
        frame_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')])
        for filename in frame_files:
                frame_path = os.path.join(folder_path, filename)
                frame = pygame.image.load(frame_path).convert_alpha()
                frame = pygame.transform.scale(frame, (80, 80))  # Size of explosion
                self.frames.append(frame)


        self.rect = self.frames[0].get_rect()
        self.rect.center = (x, y)

        self.current_frame = 0
        self.frame_speed = 5
        self.frame_count = 0

    def update(self):
        self.frame_count += 1
        if self.frame_count >= self.frame_speed:
            self.frame_count = 0
            self.current_frame += 1

    def is_finished(self):
        return self.frame_count >= len(self.frames)
    
    def draw(self, surface):
        if self.current_frame < len(self.frames):
            surface.blit(self.frames[self.current_frame], self.rect)
    

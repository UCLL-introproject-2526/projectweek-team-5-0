import pygame

def create_main_surface():
    window_size = [600, 600]
    return pygame.display.set_mode(window_size, pygame.RESIZABLE)

def draw_circle(surface):
    pygame.draw.circle(surface, (255, 0, 0), (512, 384), 50)

def draw_health(surface, font, health):
    health_text = font.render(f"Health: {health}", True, (255, 255, 255))
    surface.blit(health_text, (20, 20))

def draw_timer(surface, font, elapsed_time):
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    timer_text = font.render(f"{minutes:02d}:{seconds:02d}", True, (255, 255, 255))
    timer_rect = timer_text.get_rect()
    timer_rect.topright = (1004, 20)  # 20px from top and right edge
    surface.blit(timer_text, timer_rect)

def draw_earth_bar(surface):
    bar_height = 60
    bar_y = 768 - bar_height  # At the bottom
    
    # Blue section (water)
    pygame.draw.rect(surface, (30, 144, 255), (0, bar_y, 512, bar_height))
    
    # Green section (land)
    pygame.draw.rect(surface, (34, 139, 34), (512, bar_y, 512, bar_height))
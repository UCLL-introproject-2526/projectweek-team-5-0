import pygame

def create_main_surface():
    # Create a resizable 600x600 window
    window_size = [600, 600]
    return pygame.display.set_mode(window_size, pygame.RESIZABLE)

def draw_circle(surface):
    # Draw circle centered in the window
    center_x = surface.get_width() // 2
    center_y = surface.get_height() // 2
    pygame.draw.circle(surface, (255, 0, 0), (center_x, center_y), 50)

def draw_health(surface, font, health):
    # Draw health text at top-left
    health_text = font.render(f"Health: {health}", True, (255, 255, 255))
    surface.blit(health_text, (20, 20))

def draw_timer(surface, font, elapsed_time):
    # Draw timer at top-right, relative to window width
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    timer_text = font.render(f"{minutes:02d}:{seconds:02d}", True, (255, 255, 255))
    timer_rect = timer_text.get_rect()
    timer_rect.topright = (surface.get_width() - 20, 20)  # 20px from right edge
    surface.blit(timer_text, timer_rect)

def draw_earth_bar(surface):
    # Draw bar at bottom of window
    bar_height = 60
    bar_y = surface.get_height() - bar_height
    
    # Blue section (water) = left half
    pygame.draw.rect(surface, (30, 144, 255), (0, bar_y, surface.get_width()//2, bar_height))
    
    # Green section (land) = right half
    pygame.draw.rect(surface, (34, 139, 34), (surface.get_width()//2, bar_y, surface.get_width()//2, bar_height))
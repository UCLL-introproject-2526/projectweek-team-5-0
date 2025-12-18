import pygame
import os

_earth_image = None

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

def load_earth_image():
    global _earth_image
    
    if _earth_image is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            _earth_image = pygame.image.load(os.path.join(script_dir, "sprites", "earth-transparrent.png")).convert_alpha()
            print("Earth image loaded successfully")
        except:
            _earth_image = False  # Mark as failed to avoid retrying
            print("Warning: sprites/earth.png not found - using colored bar")
    
    return _earth_image if _earth_image else None

def draw_earth_image(surface):
    bar_height = 120  # Height for earth display
    bar_y = surface.get_height() - bar_height
    bar_width = surface.get_width()
    
    earth_image = load_earth_image()
    
    if earth_image:
        earth_stretched = pygame.transform.scale(earth_image, (bar_width, bar_height))
        surface.blit(earth_stretched, (0, bar_y))
    else:
        half_width = bar_width // 2
        pygame.draw.rect(surface, (30, 144, 255), (0, bar_y, half_width, bar_height))
        pygame.draw.rect(surface, (34, 139, 34), (half_width, bar_y, half_width, bar_height))

def draw_shoot_indicator(surface, metronome):
    """
    Draws a vertical bar on the right side that lights up when you can shoot

    surface: The pygame surface to draw on
    metronome: The Metronome object to check timing
    """
    # Get window dimensions
    screen_width, screen_height = surface.get_size()

    # Bar dimensions as percentage of screen
    bar_width = screen_width * 0.015  # 3% of screen width
    bar_height = screen_height * 0.5  # 50% of screen height

    # Position on right side, vertically centered
    bar_x = screen_width - bar_width - (screen_width * 0.02)  # 2% margin from right
    bar_y = (screen_height - bar_height) / 2  # Centered vertically

    # Check if player can shoot
    can_shoot = metronome.can_shoot()

    # Choose color based on shoot window
    if can_shoot:
        bar_color = (74, 222, 128)  # Bright green - GO!
        glow_color = (74, 222, 128, 100)  # Semi-transparent green glow
    else:
        bar_color = (71, 85, 105)  # Dark gray - NOT YET
        glow_color = None

    # Draw glow effect when active
    if glow_color:
        glow_width = bar_width * 1.5
        glow_x = bar_x - (glow_width - bar_width) / 2
        pygame.draw.rect(surface, glow_color[:3],
                        (glow_x, bar_y, glow_width, bar_height))

    # Draw main bar
    pygame.draw.rect(surface, bar_color, (bar_x, bar_y, bar_width, bar_height))

    # Draw border
    pygame.draw.rect(surface, (255, 255, 255),
                    (bar_x, bar_y, bar_width, bar_height), 2)

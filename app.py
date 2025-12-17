import pygame
import pygame_gui
import time
import os
import random
from ui_elements import *
from menus import *
from metronome import Metronome
from asteroids import Asteroid
from asteroids import Splitter
from player_state import PlayerState
from avatar import Avatar
from projectile import Projectile

pygame.init()

# =====================================================
# deze functie zitten alle dingen in die gerund worden.
# =====================================================

# closes game properly
def close_game():
    pygame.quit()

def main(skip_menu=False):
    # create window once
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    info = pygame.display.Info()
    surface = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
    pygame.display.set_caption("Asteroid Destroyers")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    start_time = time.time()
    player_state = PlayerState()
    metronome = Metronome(bpm=120)
    running = True # run game status
    game_over = False

    # Only show main menu if skip_menu is False
    if not skip_menu:
        while running:
            action = main_menu(surface)  # Returns "start", "settings", or quits

            if action == "settings":
                settings_menu(surface)
                continue  # Show main menu again after settings
            elif action == "start":
                break  # Exit menu loop and start game

    asteroids = []
    splitters = []
    projectiles = []
    last_spawn_time = 0
    shoot_pressed = False

    # Create a avatar instance
    avatar = Avatar(surface.get_width(), surface.get_height())

    def spawn_asteroid():
        asteroid = Asteroid(surface.get_width(), surface.get_height(), 10)
        asteroids.append(asteroid)

    def spawn_projectile(avatar_position, angle):
        projectile = Projectile(avatar_position, angle)
        projectiles.append(projectile)

    try:
        game_background = pygame.image.load("sprites/earth_space.png").convert()
        game_background = pygame.transform.scale(game_background, (surface.get_width(), surface.get_height()))
    except pygame.error:
        print("Failed to load background image.")
        running = False

    while running:
        surface.fill((0, 0, 0)) 
        surface.blit(game_background, (0, 0))

        metronome.update()
        player_state.update()
        elapsed_time = time.time() - start_time

        if not game_over:
            if elapsed_time - last_spawn_time >= 2:
                spawn_asteroid()
                last_spawn_time = elapsed_time

            # 1. DRAW BACKGROUND LAYER FIRST (Earth Bar)
            draw_earth_image(surface)

            # 2. UPDATE & COLLISION LOGIC
            
            # Projectiles Update
            for projectile in projectiles[:]:
                projectile.update(projectiles, surface.get_width(), surface.get_height())
                projectile.draw(surface)

            # Asteroid Update + Collision
            for asteroid in asteroids[:]:
                asteroid.update() # CHANGE: No longer passing projectiles
                
                # NEW COLLISION BLOCK: Handles deletion on impact
                for projectile in projectiles[:]:
                    if asteroid.rect.colliderect(projectile.rect):
                        asteroid.damage(10)
                        if projectile in projectiles:
                            projectiles.remove(projectile) 

                asteroid.draw(surface)

                if asteroid.health <= 0:
                    if random.random() > 0.5:
                        splitters.append(Splitter(30, 0, 10, 20, asteroid))
                        splitters.append(Splitter(-30, 0, 10, 20, asteroid))
                    asteroids.remove(asteroid)
                
                if asteroid.rect.y > surface.get_height():
                    asteroids.remove(asteroid)
                    player_state.take_damage(10)

            # Splitter Update + Collision
            for splitter in splitters[:]:
                splitter.update() # CHANGE: No longer passing projectiles
                
                # NEW COLLISION BLOCK for Splitters
                for projectile in projectiles[:]:
                    if splitter.rect.colliderect(projectile.rect):
                        splitter.damage(10)
                        if projectile in projectiles:
                            projectiles.remove(projectile)

                splitter.draw(surface)
                if splitter.health <= 0:
                    splitters.remove(splitter)
                if splitter.rect.y > surface.get_height():
                    splitters.remove(splitter)
                    player_state.take_damage(5)

            # 3. DRAW PLAYER LAYER (On top of asteroids)
            keys = pygame.key.get_pressed()
            avatar.update(keys, surface.get_width(), surface.get_height())
            avatar.draw(surface)

            # 4. DRAW UI LAYER (On very top)
            draw_health(surface, font, player_state.health)
            draw_timer(surface, font, elapsed_time)
            draw_shoot_indicator(surface, metronome)

            player_state.update_ship_collision(avatar, asteroids)

            if player_state.health <= 0:
                game_over = True
        else:
            action = game_over_menu()

            if action == "restart":
                # Restart the game and skip the main menu
                return main(skip_menu=True)
            elif action == "main_menu":
                # go to main menu
                return main(skip_menu=False)
            elif action == "quit":
                running = False

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # checks for escape and quits
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("closed game")
                    running = False

            # SPATIE CHECK
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_pressed = True

            # klik check
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    shoot_pressed = True

            #schiet functie
            if shoot_pressed:
                if metronome.can_shoot() == True:
                    if player_state.is_hit == False:
                        spawn_projectile(avatar.get_gun_position(), avatar.angle)
                        avatar.trigger_fire()
                        print("PEWPEW")
                else:
                    player_state.is_hit = True
                    print("FOUTE TIMING JIJ IDIOOT")
                shoot_pressed=False

# dit is tijdelijk omdat we nog geen damage feature hebben. nu kan je
# de damage-logica triggeren met h
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    player_hit = player_state.take_damage(10)

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_j:
            #         player_state.self.health += 10

        clock.tick(60)  # 60 FPS

    close_game() # cleanly close game

# no touchy, supposed to run
main()
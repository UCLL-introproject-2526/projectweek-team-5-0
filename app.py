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

def main():
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

    # show main menu
    main_menu(surface)

    asteroids = []
    splitters = []
    projectiles = []
    last_spawn_time = 0

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
        surface.fill((0, 0, 0))  # Clear screen with black
        surface.blit(game_background, (0, 0))  # Set bg

        metronome.update()
        player_state.update()

        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        # Draw everything
        if not game_over:
                        # Asteroid spawning logic
            if elapsed_time - last_spawn_time >= 2:  # Spawn every 2 seconds
                spawn_asteroid()
                last_spawn_time = elapsed_time

            #==========================
            #ENKEL DRAWS HIERONDER
            # =============================

            #draw alle ui elementen laatste en on top
            draw_earth_bar(surface)
            # Update and draw asteroids
            for asteroid in asteroids[:]:
                asteroid.update(projectiles)
                asteroid.draw(surface)
                if asteroid.health <= 0:
                    if  random.randint(0, 1)>0.5:
                            splitter = Splitter(30, 0, 10, 20, asteroid)
                            splitters.append(splitter)

                            splitter = Splitter(-30, 0, 10, 20, asteroid)
                            splitters.append(splitter)

                    asteroids.remove(asteroid)
                if asteroid.rect.y > surface.get_height():
                    asteroids.remove(asteroid)
                    player_state.take_damage(10)
            # Update and draw splitters
            for splitter in splitters[:]:
                splitter.update(projectiles)
                splitter.draw(surface)
                if splitter.health <= 0:
                    splitters.remove(splitter)
                if splitter.rect.y > surface.get_height():
                    splitters.remove(splitter)
                    player_state.take_damage(5)
            # Update and draw projectiles
            for projectile in projectiles[:]:
                projectile.update(projectiles, surface.get_width(), surface.get_height())
                projectile.draw(surface)
            # Update and draw avatar
            keys = pygame.key.get_pressed()
            avatar.update(keys, surface.get_width(), surface.get_height())
            avatar.draw(surface)
            draw_health(surface, font, player_state.health)
            draw_timer(surface, font, elapsed_time)
            draw_shoot_indicator(surface, metronome)

            # ship collision
            player_state.update_ship_collision(avatar, asteroids)

            # Check for game over
            if player_state.health <= 0:
                game_over = True
        else:
            action = game_over_menu()

            if action == "restart":
                return main()  # clean restart
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

            #schiet functie
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if metronome.can_shoot() == True:
                        if player_state.is_hit == False:
                            spawn_projectile(avatar.get_gun_position(), avatar.angle)
                            avatar.trigger_fire()
                            print("PEWPEW")
                    else:
                        player_state.is_hit = True
                        print("FOUTE TIMING JIJ IDIOOT")

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
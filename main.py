# we hebben ai enkel gebruikt in een ondersteunende functie. Voor tijdelijk
# feature testen hebben we AI-code overgenomen maar al deze functies
# zijn door mensen herschreven. Onze game is dus niet gevibe-coded.

import pygame
import pygame_gui
import time
import os
from random import random, randint
from ui_elements import *
from menus import *
from metronome import Metronome
from asteroids import Asteroid
from asteroids import Splitter
from player_state import PlayerState
from avatar import Avatar
from projectile import Projectile
from healthpack import HealthPack
from explosion import Explosion
from powerup_item import PowerUpItem
from combat_modifier import CombatModifier

pygame.init()

# =====================================================
# deze functie zitten alle dingen in die gerund worden.
# =====================================================

# Settings menu's
SETTINGS_MENUS = {
    "keyboard": keyboard_menu,
    "video": video_menu,
    "skins": skins_menu,
}

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
    player_state = PlayerState()
    metronome = Metronome(bpm=120)
    running = True # run game status
    game_over = False
    combat_mod = CombatModifier()
    powerup_items = []
    last_powerup_spawn = 0

    # Only show main menu if skip_menu is False
    if not skip_menu:
        while running:
            action = main_menu(surface)  # Returns "start", "settings", or quits

            if action == "settings":
                while True:
                    settings_action = settings_menu(surface)

                    if settings_action == "back":
                        break  # back to main menu

                    submenu = SETTINGS_MENUS.get(settings_action)
                    if submenu:
                        submenu(surface)

                continue

            elif action == "start":
                break  # Exit menu loop and start game
            elif action == "quit":
                close_game()
                return

    start_time = time.time()

    asteroids = []
    splitters = []
    projectiles = []
    last_spawn_time = 0
    shoot_pressed = False
    healthpacks = []
    last_healthpack_spawn = 0
    explosions = []

    # Create a avatar instance
    avatar = Avatar(surface.get_width(), surface.get_height(), player_state)

    def spawn_asteroid():
        asteroid = Asteroid(surface.get_width(), surface.get_height(), 10, stage_speed, spawn_time=elapsed_time)
        asteroids.append(asteroid)

    def spawn_healthpack():
        healthpack = HealthPack(surface.get_width(), surface.get_height())
        healthpacks.append(healthpack)

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

        metronome.update(combat_mod)
        player_state.update()
        elapsed_time = time.time() - start_time

        if not game_over:
            if elapsed_time <= 60:
                stage_speed = randint(1, 2)
                stage_split_chance = 0.7
                asteroid_damage = 10
            elif 120 >= elapsed_time > 60:
                stage_split_chance = 0.5
            elif 180 >= elapsed_time > 120:
                stage_speed= randint(2, 3)
            else:
                stage_split_chance = 1.0
                asteroid_damage = 100

            if elapsed_time - last_spawn_time >= 2:
                spawn_asteroid()
                last_spawn_time = elapsed_time

            # HP ORB SPAWN
            if elapsed_time - last_healthpack_spawn >= 15:  # Spawn every 15 seconds
                spawn_healthpack()
                last_healthpack_spawn = elapsed_time

            # SPAWN LOGIC FOR SHOTGUN POWERUP
            if elapsed_time - last_powerup_spawn >= 25 and not combat_mod.active: # Spawn every 25s
                powerup_items.append(PowerUpItem(surface.get_width(), surface.get_height()))
                last_powerup_spawn = elapsed_time

            # UPDATE COMBAT MODIFIER
            combat_mod.update(metronome)

            # DRAW & UPDATE POWERUPS
            for p_item in powerup_items[:]:
                p_item.update()
                p_item.draw(surface)

                # Collision with Player
                if p_item.rect.colliderect(avatar.rect):
                    combat_mod.activate(metronome)
                    p_item.play_sound()
                    powerup_items.remove(p_item)

            # 1. DRAW BACKGROUND LAYER FIRST (Earth Bar)
            draw_earth_image(surface, player_state.health)

            # 2. UPDATE & COLLISION LOGIC

            # Projectiles Update
            for projectile in projectiles[:]:
                projectile.update(projectiles, surface.get_width(), surface.get_height())
                projectile.draw(surface)

            # Asteroid Update + Collision
            for asteroid in asteroids[:]:
                asteroid.update() # CHANGE: No longer passing projectiles
                # Only enable doomsday if time > 180 seconds
                if asteroid.spawn_time >= 180: #Stage 4 condition
                    explosion = Explosion(asteroid.rect.centerx, asteroid.rect.centery)
                    explosions.append(explosion)


                # NEW COLLISION BLOCK: Handles deletion on impact
                for projectile in projectiles[:]:
                    if asteroid.rect.colliderect(projectile.rect):
                        asteroid.damage(10)
                        if projectile in projectiles:
                            projectiles.remove(projectile)

                asteroid.draw(surface)

                if asteroid.health <= 0:
                    #black white exploseion
                    explosion = Explosion(asteroid.rect.centerx, asteroid.rect.centery,scale=1, grayscale=True)  # Half size
                    explosions.append(explosion)

                    asteroid.play_destroy_sound()
                    if random() > stage_split_chance:
                        splitters.append(Splitter(30, 0, 10, 20, asteroid))
                        splitters.append(Splitter(-30, 0, 10, 20, asteroid))
                    asteroids.remove(asteroid)
                if asteroid.rect.y > surface.get_height()-75:

                    #BOOM
                    explosion = Explosion(asteroid.rect.centerx, surface.get_height() - 60, scale=1.0, grayscale=False)
                    explosions.append(explosion)

                    asteroids.remove(asteroid)
                    player_state.take_damage(asteroid.damage_value)

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
                    explosion = Explosion(splitter.rect.centerx, splitter.rect.centery, scale=0.5, grayscale=True)  # Quarter size
                    explosions.append(explosion)
                    splitters.remove(splitter)
                if splitter.rect.y > surface.get_height()-75:

                    #BOOM
                    explosion = Explosion(splitter.rect.centerx, surface.get_height() - 60)
                    explosions.append(explosion)

                    splitters.remove(splitter)
                    player_state.take_damage(2)

            #THIS DRAWS ALL HP OBS/PACKS
            for healthpack in healthpacks[:]:
                healthpack.update()

                # Check collision with player
                if healthpack.rect.colliderect(avatar.rect):
                    player_state.heal(50)
                    healthpacks.remove(healthpack)
                    healthpack.play_pickup_sound()
                    continue

                healthpack.draw(surface)
            #NO MORE HP

            #EXPLOSION REMOVAL
            for explosion in explosions[:]:
                explosion.update()
                if explosion.is_finished():
                    explosions.remove(explosion)
                else:
                    explosion.draw(surface)

            # 3. DRAW PLAYER LAYER (On top of asteroids)
            keys = pygame.key.get_pressed()
            avatar.update(keys, surface.get_width(), surface.get_height())
            avatar.draw(surface)
            player_state.draw_paralisys(surface, avatar)

            # 4. DRAW UI LAYER (On very top)
            draw_health(surface, font, player_state.health)
            draw_timer(surface, font, elapsed_time)
            draw_shoot_indicator(surface, metronome, combat_mod)

            player_state.update_ship_collision(avatar, asteroids)

            if player_state.health <= 0:
                game_over = True
        else:

            # you can use "main_menu, restart and quit" in other functions to trigger this
            action = game_over_menu(elapsed_time)

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    print("restarted game")
                    return main(skip_menu=False)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print("restarted game")
                    return main(skip_menu=True)

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
                        if combat_mod.is_beat_forbidden(metronome.current_beat):
                            print("GUN JAMMED - EMPTY BEAT")
                        else:
                            new_shots = combat_mod.create_shots(avatar, metronome)
                            projectiles.extend(new_shots)
                            avatar.trigger_fire()
                            print("PEWPEW")
                else:
                    player_state.paralyse()
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
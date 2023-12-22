import pygame
import game_sdl
from constants import *
from game_structs import Character, CharacterBehavior, CharacterBehaviors


def update_character(character: Character, events: dict):
    if character.stop:
        return

    # Sleep
    if character.sleep:
        character.sleep = max(0, character.sleep - 1)
    # Movement
    else:
        if character.right:
            character.x += VEL_X
        elif character.left:
            character.x -= VEL_X

        if character.has_coll_enemy:
            character.vy = -VY_COLLIDE
            character.has_coll_enemy = False
        elif character.land and character.jump:
            character.vy = -VEL_Y
            character.land = False

    character.y += character.vy

def update_player(player: Character, events: dict):
    if pygame.K_RIGHT in events:
        if not player.right:
            player.direction = True
        player.right = events[pygame.K_RIGHT]

    if pygame.K_LEFT in events:
        if not player.left:
            player.direction = False
        player.left = events[pygame.K_LEFT]

    if pygame.K_UP in events:
        player.jump = events[pygame.K_UP]

    if pygame.K_SPACE in events:
        player.stop = events[pygame.K_SPACE]

    update_character(player, events)

def on_land(character: Character):
    character.land = True
    character.vy = 0

def on_peak(character: Character):
    if character.vy < 0:
        character.vy = 0

def on_air(character: Character):
    character.land = False
    character.vy = min(character.vy + GRAVITY, MAX_VY)  

def on_left(character: Character):
    pass

def on_right(character: Character):
    pass

def on_start(character: Character):
    pass

# Controlled character
def on_left_move(character: Character):
    character.direction = True
    character.right = True
    character.left = False

def on_right_move(character: Character):
    character.direction = False        
    character.right = False
    character.left = True

def on_start_move(character: Character):
    character.direction = True
    character.right = True

def on_start_jump(character: Character):
    character.direction = True
    character.right = True
    character.jump = True

def on_collide(character: Character, top: bool):
    if top:
        character.has_coll_enemy = True
    else:
        character.sleep = SLEEP

character_behaviors = {
    CharacterBehaviors.PLAYER: CharacterBehavior(update_player, on_land, on_peak, on_air, on_left, on_right, on_start, on_collide),
    CharacterBehaviors.JUMPING_AI: CharacterBehavior(update_character, on_land, on_peak, on_air, on_left_move, on_right_move, on_start_jump, on_collide),
    CharacterBehaviors.BASIC_AI: CharacterBehavior(update_character, on_land, on_peak, on_air, on_left_move, on_right_move, on_start_move, on_collide),
}

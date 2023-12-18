import pygame
import game
from constants import *
from game_structs import Character, CharacterBehavior


def update_character(character: Character, events: dict):
    if character.stop:
        return
            
    # X movement
    if character.right:
        character.x += VEL_X
    if character.left:
        character.x -= VEL_X
    
    # Y movement
    if character.land and character.jump:
        character.vy = -VEL_Y
        character.land = False
        
    character.y += character.vy

def update_player(player: Character, events: dict):
    if pygame.K_RIGHT in events:
        if not player.right:
            player.direction = True
            player.frame = 0
        player.right = events[pygame.K_RIGHT]
        
    if pygame.K_LEFT in events:
        if not player.left:
            player.direction = False
            player.frame = 0
        player.left = events[pygame.K_LEFT]
        
    if pygame.K_UP in events:
        player.jump = events[pygame.K_UP]
        player.frame = 0

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


player_behavior = CharacterBehavior(update_player, on_land, on_peak, on_air, on_left, on_right, on_start)

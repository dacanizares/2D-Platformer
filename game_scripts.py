import pygame
from game_structs import *
from constants import *
from collision_scripts import *
from tilemap_structs import Tilemap


def spawn_characters(tilemap: Tilemap, sprites_player, sprites_computer) -> tuple[list[Character], Character]:
    characters: list[Character] = []
    player: Character = None
    for to_spawn in tilemap.characters_to_spawn:
        if to_spawn.characterBehavior == CharacterBehaviors.PLAYER:
            sprites = sprites_player
        else:
            sprites = sprites_computer
        character = Character(to_spawn.x, to_spawn.y, CHARACTER_COLL_W, CHARACTER_COLL_H, CharacterAnim(sprites), to_spawn.characterBehavior)
        characters.append(character)
        if to_spawn.characterBehavior == CharacterBehaviors.PLAYER:
            player = character
    return (characters, player)

def update_camera(camera: Camera, focus_location: tuple):
    if camera.always_centered:
        camera.x = int(focus_location.x - DISP_W / 2)
        camera.y = int(focus_location.y - DISP_H * 3 / 4)
    else:
        limit_x = int(camera.offset_x * DISP_W)

        if focus_location.x < camera.x + limit_x:
            camera.x -= (camera.x + limit_x) - focus_location.x 
        elif focus_location.x > (camera.x + DISP_W) - limit_x:
            camera.x += focus_location.x - ((camera.x + DISP_W) - limit_x)

        limit_y = int(camera.offset_y * DISP_H)
        if focus_location.y < camera.y + limit_y:
            camera.y -= (camera.y + limit_y) - focus_location.y 
        elif focus_location.y > (camera.y + DISP_H) - limit_y:
            camera.y += focus_location.y - ((camera.y + DISP_H) - limit_y)


def start_characters(characters: list[Character], behaviors: dict):   
    for character in characters:
        update_character_collider(character, 0)
        behaviors[character.behavior_type].on_start(character)

def update_character_collider(character: Character, coll_dy: int):
    character.collider = pygame.Rect(character.x, character.y, character.w, character.h)
    character.coll_dy = coll_dy

# Updates entities and colliding events
# events: pygame events to send to entities
def update_characters(characters: list[Character], behaviors: dict, events: dict, tilemap: Tilemap):
    # Static collisions (against map)
    for character in characters:
        behavior = behaviors[character.behavior_type]
        behavior.update(character, events)
    
        # Collider to compare with
        coll = character.collider

        # UPDATE X --------------------------------------
        left, right, top, bot = project_collider_to_tilemap(character, tilemap)

        # Search for limits
        (min_x, coll_dy) = search_collisions(tilemap, left, top, bot, -1 , 0)
        (max_x, coll_dy) = search_collisions(tilemap, right, top, bot,  1 , 0) 

        # Limit X
        limit = min_x * tilemap.tilew + tilemap.tilew + coll.w / 2
        if character.x <= limit:
            character.x = limit
            behavior.on_left(character)
        limit = max_x * tilemap.tilew - coll.w / 2        
        if character.x >= limit:
            character.x = limit      
            behavior.on_right(character)
        # Update collider (just X axis)
        coll.x = character.x

        # UPDATE Y ------------------------------------
        left, right, top, bot = project_collider_to_tilemap(character, tilemap)

        # Search for limits
        (min_y, coll_dy) = search_collisions(tilemap, top, left, right, 0, -1)
        (max_y, coll_dy) = search_collisions(tilemap, bot, left, right, 0, 1, character.vy > 0 or character.land)

        # Limit Y
        limit = max_y * tilemap.tileh + coll_dy
        if character.y >= limit:
            character.y = limit
            behavior.on_land(character)
        else:
            behavior.on_air(character)

            limit = min_y * tilemap.tileh + tilemap.tileh + coll.h
            if character.y <= limit:
                character.y = limit
                behavior.on_peak(character)
        update_character_collider(character, coll_dy)        

    # Dynamic collisions
    for character_a_idx in range(0, len(characters) - 1):
        character_a = characters[character_a_idx]
        for character_b_idx in range(character_a_idx + 1, len(characters)):
            character_b = characters[character_b_idx]
            
            if character_a.collider.colliderect(character_b.collider):
                if character_a.collider.top < character_b.collider.top:
                    is_top_a = True
                else:
                    is_top_a = False

                behavior_a = behaviors[character_a.behavior_type]
                behavior_b = behaviors[character_b.behavior_type]
                behavior_a.on_collide(character_a, is_top_a)
                behavior_b.on_collide(character_b, not is_top_a)

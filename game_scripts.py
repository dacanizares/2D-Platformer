import pygame
from game_structs import *
from constants import *
from collision_scripts import *
from tilemap_structs import Tilemap


def update_camera(camera: Camera, focus_location: tuple):
    if camera.always_centered:
        camera.x = focus_location.x - DISP_W / 2
        camera.y = focus_location.y - DISP_H * 3 / 4
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
        behaviors[character.behavior_type].on_start(character)

def update_character_collider(character: Character):
    character.collider = pygame.Rect(character.x, character.y, character.collider.w, character.collider.h)

# Updates entities and colliding events
# events: pygame events to send to entities
def update_characters(characters: list[Character], behaviors: dict, events: dict, tilemap: Tilemap):
    # Static collisions (against map)
    for character in characters:
        behavior = behaviors[character.behavior_type]
        behavior.update(character, events)
    
        # Collider to compare with
        update_character_collider(character)
        coll = character.collider

        # UPDATE X --------------------------------------
        left, right, top, bot = project_collider_to_tilemap(coll, tilemap)

        # Search for limits
        min_x = search_collisions(tilemap, character, left, top, bot, -1 , 0)
        max_x = search_collisions(tilemap, character, right, top, bot,  1 , 0) 

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
        left, right, top, bot = project_collider_to_tilemap(coll, tilemap)

        # Search for limits
        min_y = search_collisions(tilemap, character, top, left, right, 0, -1)
        max_y = search_collisions(tilemap, character, bot, left, right, 0, 1, character.vy > 0 or character.land)

        # Limit Y
        limit = max_y * tilemap.tileh
        if character.y >= limit:
            character.y = limit
            behavior.on_land(character)
        else:
            behavior.on_air(character)

            limit = min_y * tilemap.tileh + tilemap.tileh + coll.h
            if character.y <= limit:
                character.y = limit
                behavior.on_peak(character)
        update_character_collider(character)        

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



import pygame
from constants import DISP_H, DISP_W
from game_structs import Camera, CharacterConfig
from tilemap_structs import Tilemap


def update_camera(camera: Camera, focus_location: tuple):
    if not camera.always_centered:
        camera.x = focus_location.x - DISP_W / 2
        camera.y = focus_location.y - DISP_H * 3 / 4
    else:
        limit_x = int(camera.offset * DISP_W)

        if focus_location.x < camera.x + limit_x:
            camera.x -= (camera.x + limit_x) - focus_location.x 
        elif focus_location.x > (camera.x + DISP_W) - limit_x:
            camera.x += focus_location.x - ((camera.x + DISP_W) - limit_x)

        limit_y = int(focus_location.offset * DISP_H)
        if focus_location.y < camera.y + limit_y:
            camera.y -= (camera.y + limit_y) - focus_location.y 
        elif focus_location.y > (camera.y + DISP_H) - limit_y:
            camera.y += focus_location.y - ((camera.y + DISP_H) - limit_y)


def start_characters(characters_config: list[CharacterConfig]):   
    for character_config in characters_config:
        character = character_config.character
        character_config.behavior.on_start(character)


# Get collider limits.
# col: pygame.Rect
# tileset_idx: where to get dimensions from, by default idx=0
#
# Returns left, right, top and bot rows or cols limiting with.
# The collider center point is at middle bottom.
def _get_limits(tilemap: Tilemap, col: pygame.Rect, tileset_idx: int=0):
    left = (col.x - col.w / 2 + 1) / tilemap.tilesets[tileset_idx].tilew
    right = (col.x + col.w / 2 - 1) / tilemap.tilesets[tileset_idx].tilew
    top = (col.y - col.h + 1) / tilemap.tilesets[tileset_idx].tileh
    bot = (col.y - 1) / tilemap.tilesets[tileset_idx].tileh
    return left, right, top, bot

# Updates entities and colliding events
# events: pygame events to send to entities
def update_characters(characters_config: list[CharacterConfig], events: dict, tilemap: Tilemap):
    for character_config in characters_config:
        character = character_config.character
        character_config.behavior.update(character_config.character, events)
    
        # Collider to compare with
        col = character.collider

        # UPDATE X --------------------------------------
        left, right, top, bot = _get_limits(tilemap, col)

        # Search for limits
        min_x = _search_collisions(tilemap, left, top, bot, -1 , 0)
        max_x = _search_collisions(tilemap, right, top, bot,  1 , 0) 

        # Limit X
        limit = min_x * tilemap.tilew + tilemap.tilew + col.w / 2
        if character.x <= limit:
            character.x = limit
            character_config.behavior.on_left(character)
        limit = max_x * tilemap.tilew - col.w / 2        
        if character.x >= limit:
            character.x = limit      
            character_config.behavior.on_right(character)
        # Update collider (just X axis)
        col.x = character.x

        # UPDATE Y ------------------------------------
        left, right, top, bot = _get_limits(tilemap, col)

        # Search for limits
        min_y = _search_collisions(tilemap, top, left, right, 0, -1)
        max_y = _search_collisions(tilemap, bot, left, right, 0, 1)

        # Limit Y
        limit = min_y * tilemap.tileh + tilemap.tileh + col.h
        if character.y <= limit:
            character.y = limit
            character_config.behavior.on_peak(character)
        limit = max_y * tilemap.tileh

        if character.y >= limit:
            character.y = limit
            character_config.behavior.on_land(character)
        else:
            character_config.behavior.on_air(character)

        # Update Collider
        character.collider = pygame.Rect(character.x, character.y, character.collider.w, character.collider.h)


#if DEBUG:
#    game.debug_txt('LEFT: '+str(min_x), (0,0), RED)
#    game.debug_txt('RIGHT: '+str(max_x), (0,10), RED)
#    game.debug_txt('TOP: '+str(min_y), (0,20), RED)
#    game.debug_txt('BOT: '+str(max_y), (0,30), RED)   
#    
#    game.debug_txt('LEFT: '+str(left), (100,0), RED)
#    game.debug_txt('RIGHT: '+str(right), (100,10), RED)
#    game.debug_txt('TOP: '+str(top), (100,20), RED)
#    game.debug_txt('BOT: '+str(bot), (100,30), RED)                      


# Search for static objects to collide with
# start: starting point
# a: lower bound
# b: upper bound (a < b)
# dx, dy: moving direction
#
# Returns: None if no colliders found. Otherwise a value with the ROW or COLUMN of the collider.
#
# Example: 
#  to trace from x = 1, to the left, from tiles y = 2 to y = 3
#  search(1, 2, 5, 1, 0)
#
# Result:
#    0 1 2 3 4 5 ... MAX_DIST_COL
#  0 . . . . . .
#  1 . . . . . .
#  2 . X X X X X 
#  3 . X X X X X 
#  4 . . . . . . 
#
#  It will search on the position marked with X

def _search_collisions(tilemap: Tilemap, start, a, b, dx, dy):
    # Grant that these vars are int
    start = int(start)
    a = int(a)
    b = int(b)

    # Validate that we arent searching on diagonals
    if dx != 0 and dy != 0:
        raise Exception('collision search', 'unable to lock on diagonals.')

    if a < 0:
        return -1

    # Set limits, by default 0, width or height according to dx and dy
    limit = -1
    if dx > 0:
        limit = tilemap.current_width
    elif dy > 0:
        limit = tilemap.current_height
            
    # Search for static objects!
    while True:
        # If we reached the limit
        if start == limit:
            return start

        # Scan!
        for i in range(a, b + 1):
            # x changing
            if dx != 0 and tilemap.current_map[i][start] not in tilemap.no_collision:                    
                return start
            # y changing
            elif dy != 0 and tilemap.current_map[start][i] not in tilemap.no_collision:
                return start
        # Advance!
        start += (dx + dy)

import pygame
from game_structs import *
from constants import *
from tilemap_scripts import get_coll_dy
from tilemap_structs import Tilemap

# Project character collider to tilemap.
# character: Character
# tileset_idx: where to get dimensions from, by default idx=0
#
# Returns left, right, top and bot rows or cols limiting with.
# The collider center point is at middle bottom.
def project_collider_to_tilemap(character: Character, tilemap: Tilemap, tileset_idx: int=0):
    coll = character.collider
    tile_w = tilemap.tilesets[tileset_idx].tilew
    tile_h = tilemap.tilesets[tileset_idx].tileh
    left = (coll.x - coll.w / 2 + 1) / tile_w
    right = (coll.x + coll.w / 2 - 1) / tile_w
    top = (coll.y - coll.h + 1 - character.coll_dy) / tile_h
    bot = (coll.y - 1 - character.coll_dy) / tile_h
    return int(left), int(right), int(top), int(bot)


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
def search_collisions(tilemap: Tilemap, start, a, b, dx, dy, ignore_no_peak=False) -> tuple[int, float]:
    # Grant that these vars are int
    start = int(start)
    a = int(a)
    b = int(b)

    # Validate that we arent searching on diagonals
    if dx != 0 and dy != 0:
        raise Exception('collision search', 'unable to lock on diagonals.')

    if a < 0:
        return (-1, 0)

    # Set limits, by default 0, width or height according to dx and dy
    limit = -1
    if dx > 0:
        limit = tilemap.current_width
    elif dy > 0:
        limit = tilemap.current_height
            
    # Search for static objects!
    while True:
        # Advance!
        start += (dx + dy)
        
        # If we reached the limit
        if start == limit or start < 0:
            return (start, 0)

        # Scan!
        for i in range(a, b + 1):
            # x changing
            if dx != 0:
                tile_id = tilemap.current_map[i][start]
                if tile_id not in tilemap.no_collision and tile_id not in tilemap.no_peak:   
                    return (start, 0)
            # y changing
            elif dy != 0:

                if dy > 0 and DEBUG_COLL_BOT:
                    tilemap.debug_rects.append((start, i))

                tile_id = tilemap.current_map[start][i]
                if tile_id not in tilemap.no_collision:                    
                    if ignore_no_peak or tile_id not in tilemap.no_peak: 
                        return (start, get_coll_dy(tilemap, tile_id))
        

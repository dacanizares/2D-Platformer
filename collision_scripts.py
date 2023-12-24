import pygame
from game_structs import *
from constants import *
from tilemap_structs import Tilemap

# Project collider to tilemap.
# col: pygame.Rect
# tileset_idx: where to get dimensions from, by default idx=0
#
# Returns left, right, top and bot rows or cols limiting with.
# The collider center point is at middle bottom.
def project_collider_to_tilemap(col: pygame.Rect, tilemap: Tilemap, tileset_idx: int=0):
    tile_w = tilemap.tilesets[tileset_idx].tilew
    tile_h = tilemap.tilesets[tileset_idx].tileh
    left = (col.x - col.w / 2 + 1) / tile_w
    right = (col.x + col.w / 2 - 1) / tile_w
    top = (col.y - col.h + 1) / tile_h
    bot = (col.y - 1) / tile_h
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
def search_collisions(tilemap: Tilemap, character: Character, start, a, b, dx, dy, ignore_no_peak=False):
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
        # Advance!
        start += (dx + dy)
        
        # If we reached the limit
        if start == limit or start < 0:
            return start

        # Scan!
        for i in range(a, b + 1):
            # x changing
            if dx != 0:
                if tilemap.current_map[i][start] not in tilemap.no_collision and tilemap.current_map[i][start] not in tilemap.no_peak:   
                    return start
            # y changing
            elif dy != 0:
                if dy > 0 and DEBUG_COLL_BOT:
                    tilemap.debug_rects.append((start, i))
                if tilemap.current_map[start][i] not in tilemap.no_collision:                    
                    if ignore_no_peak or tilemap.current_map[start][i] not in tilemap.no_peak: 
                        return start
        

import game
import pygame
from pygame.locals import *
from constants import *

class Gamelogic:
    def __init__(self, player, tilemap):        
        self.player = player
        self.tilemap = tilemap

    # Get collider limits.
    # col: pygame.Rect
    #
    # Returns left, right, top and bot rows or cols limiting with.
    # The collider center point is at middle bottom.

    def get_limits(self, col):
        left = (col.x - col.w / 2 + 1) / self.tilemap.tilew
        right = (col.x + col.w / 2 - 1) / self.tilemap.tilew
        top = (col.y - col.h + 1) / self.tilemap.tileh
        bot = (col.y - 1) / self.tilemap.tileh

        return left, right, top, bot
        

    # Updates entities and colliding events
    # events: pygame events to send to entities

    def update(self, events):
        self.player.update_events(events)
        self.player.update()
        
        # Collider to compare with
        col = self.player.collider

        # UPDATE X --------------------------------------
        left, right, top, bot = self.get_limits(col)

        # Search for limits
        min_x = self.search(left, top, bot, -1 , 0)
        max_x = self.search(right, top, bot,  1 , 0) 

        # Limit X
        limit = min_x * self.tilemap.tilew + self.tilemap.tilew + col.w / 2
        if self.player.x <= limit:
            self.player.x = limit
        limit = max_x * self.tilemap.tilew - col.w / 2        
        if self.player.x >= limit:
            self.player.x = limit      

        # Update collider (just X axis)
        col.x = self.player.x



        # UPDATE Y ------------------------------------
        left, right, top, bot = self.get_limits(col)

        # Search for limits
        min_y = self.search(top, left, right, 0, -1)
        max_y = self.search(bot, left, right, 0, 1)

        # Limit Y
        limit = min_y * self.tilemap.tileh + self.tilemap.tileh + col.h
        if self.player.y <= limit:
            self.player.y = limit
            self.player.on_peak()
        limit = max_y * self.tilemap.tileh

        if self.player.y >= limit:
            self.player.y = limit
            self.player.on_land()
        else:
            self.player.on_air()

        # Update Collider
        self.player.collider = pygame.Rect(self.player.x, self.player.y, self.player.collider.w, self.player.collider.h)


        if DEBUG:
            game.debug_txt('LEFT: '+str(min_x), (0,0), RED)
            game.debug_txt('RIGHT: '+str(max_x), (0,10), RED)
            game.debug_txt('TOP: '+str(min_y), (0,20), RED)
            game.debug_txt('BOT: '+str(max_y), (0,30), RED)   
            
            game.debug_txt('LEFT: '+str(left), (100,0), RED)
            game.debug_txt('RIGHT: '+str(right), (100,10), RED)
            game.debug_txt('TOP: '+str(top), (100,20), RED)
            game.debug_txt('BOT: '+str(bot), (100,30), RED)                      
    

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

    def search(self, start, a, b, dx, dy):        
        # Validate that we arent searching on diagonals
        if dx != 0 and dy != 0:
            raise Exception('collision search', 'unable to lock on diagonals.')

        if a < 0:
            return -1

        # Set limits, by default 0, width or height according to dx and dy
        limit = -1
        if dx > 0:
            limit = self.tilemap.current_width
        elif dy > 0:
            limit = self.tilemap.current_height
                
        # Search for static objects!
        while True:
            # If we reached the limit
            if start == limit:
                return start

            # Scan!
            for i in range(a, b + 1):
                # x changing
                if dx != 0 and self.tilemap.current_map[i][start] not in self.tilemap.no_collision:                    
                    return start
                # y changing
                elif dy != 0 and self.tilemap.current_map[start][i] not in self.tilemap.no_collision:
                    return start
            # Advance!
            start += (dx + dy)
           
        
        
        
    

    

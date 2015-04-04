import game
import pygame
from pygame.locals import *
from constants import *

class Gamelogic:
    def __init__(self, player, tilemap):        
        self.player = player
        self.tilemap = tilemap.current_map        
        
    def update(self, eventos):
        self.player.update_events(eventos)
        self.player.update()
        
        col = self.player.static_col

        # Update X
        left = (col.x - col.w / 2 + 1) / WTILE
        right = (col.x + col.w / 2 - 1) / WTILE
        top = (col.y - col.h + 1) / HTILE
        bot = (col.y - 1) / HTILE
        top = max(0,min(top, len(self.tilemap)-1))
        bot = max(0,min(bot,len(self.tilemap)-1))
        left = max(0,min(left,len(self.tilemap[0])-1))
        right = max(0,min(right,len(self.tilemap[0])-1))

        min_x = self.search_left(left, top, bot)
        max_x = self.search_right(right, top, bot)
        min_x = min_x + WTILE + col.w/2
        max_x = max_x - col.w/2
        
        if self.player.x >= max_x:
            self.player.x = max_x
        if self.player.x <= min_x:
            self.player.x = min_x

        # Update Y
        

        min_y = self.search_top(top, left, right)
        max_y = self.search_bot(bot, left, right)        
        min_y = min_y + HTILE + col.h
        max_y = max_y

        if self.player.y >= max_y:
            self.player.y = max_y
            self.player.on_land()
        else:
            self.player.on_air()
            
        if self.player.y <= min_y:
            self.player.y = min_y
            self.player.on_peak()

        if DEBUG:
            game.debug_txt('LEFT: '+str(left), (0,0),RED)
            game.debug_txt('RIGHT: '+str(right), (0,10),RED)
            game.debug_txt('TOP: '+str(top), (0,20),RED)
            game.debug_txt('BOT: '+str(bot), (0,30),RED)           
        

        self.player.static_col = pygame.Rect(self.player.x, self.player.y, self.player.static_col.w, self.player.static_col.h)
        
    #def search(self, start, a, b, dx, dy):
    #   while True:
            
        
    
            
    #PEDING FIX THIS CODE
    def search_top(self, top, left, right):
        for i in range(0, MAX_DIST_COL):
            for j in range(left, right+1):
                if top - i < 0:
                    continue
                if self.tilemap[top-i][j] not in IDS_COLISION_TOP:
                    if DEBUG:
                        game.debug_txt('COL->TOP: '+str(top-i),(400,0),RED)
                    return (top-i)*HTILE
        return MIN_Y

    def search_bot(self, bot, left, right):
        for i in range(0, MAX_DIST_COL):
            for j in range(left, right+1):
                if bot + i >= len(self.tilemap):
                    continue
                if self.tilemap[bot+i][j] not in IDS_COLISION_BOT:
                    if DEBUG:
                        game.debug_txt('COL->BOT: '+str(bot+i),(400,10),RED)
                    return (bot+i)*HTILE
        return MAX_Y

    def search_left(self, left, top, bot):
        for i in range(0, MAX_DIST_COL):
            for j in range(top, bot+1):
                if left - i < 0:
                    continue
                if self.tilemap[j][left-i] not in IDS_COLISION_LEFT:
                    if DEBUG:
                        game.debug_txt('COL->LEFT: '+str(left-i),(400,20),RED)
                    return (left-i)*WTILE
        return MIN_X

    def search_right(self, right, top, bot):
        for i in range(0, MAX_DIST_COL):
            for j in range(top, bot+1):
                if right + i >= len(self.tilemap[0]):
                    continue
                if self.tilemap[j][right+i] not in IDS_COLISION_RIGHT:
                    if DEBUG:
                        game.debug_txt('COL->RIGHT: '+str(right+i),(400,30),RED)
                    return (right+i)*WTILE
        return MAX_X

           
        
        
        
    

    

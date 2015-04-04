import game
import pygame
from pygame.locals import *
from constants import *

class Camera:
    def __init__(self, x, y, focus, tilemap):        
        self.x = x
        self.y = y
        self.focus = focus
        self.tilemap = tilemap

    def update(self):
        self.x = self.focus.x - DISP_W / 2
        self.y = self.focus.y - DISP_H * 3 / 4        

    def draw(self):
        x = 0
        y = 0
        for row in self.tilemap.current_map:
            for tile_id in row:
                if tile_id != 0:
                    tile = self.tilemap.gindex[tile_id]
                    tile.draw(x * tile.tileset.tilew - self.x,
                              y * tile.tileset.tileh - self.y)            
                x += 1
                if x >= self.tilemap.current_width:
                    x = 0
                    y += 1
        self.focus.draw(self.focus.x - self.x, self.focus.y - self.y)       
    

    

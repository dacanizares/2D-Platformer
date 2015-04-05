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
        starting_x = (self.x - 1) / self.tilemap.tilew
        starting_y = (self.y - 1) / self.tilemap.tileh

        ending_x = (self.x + DISP_W + 1) / self.tilemap.tilew
        ending_y = (self.y + DISP_H + 1) / self.tilemap.tileh

        for i in range(starting_y, ending_y+1):
            if i < 0 or i >= self.tilemap.current_height:
                continue
            for j in range(starting_x, ending_x+1):
                if j < 0 or j >= self.tilemap.current_width:
                    continue

                tile_id = self.tilemap.current_map[i][j]
                if tile_id != 0:
                    tile = self.tilemap.gindex[tile_id]
                    tile.draw(j * tile.tileset.tilew - self.x,
                              i * tile.tileset.tileh - self.y)
                    if DEBUG:
                        game.debug_txt(str(i)+','+str(j), 
                                       (j * tile.tileset.tilew - self.x,
                                        i * tile.tileset.tileh - self.y), RED)           
                
        self.focus.draw(self.focus.x - self.x, self.focus.y - self.y)
    

    

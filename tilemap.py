import game
import pygame
from tile import *
from pygame.locals import *
from constants import *

class Tilemap:
    def __init__(self, tiles, resources):
        result = []
        for y in range(0,len(tiles)):
            row = []
            for x in range(0,len(tiles[y])):
                if tiles[y][x] != -1:
                    row.append(Tile(WTILE*x,HTILE*y,[resources[tiles[y][x]]]))
                else:
                    row.append(None)
                
            result.append(row)
        self.tilemap = tiles
        self.tiles = result
        self.resources = resources
        
    def draw(self, xcam, ycam, width, height):
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                tile = self.tiles[i][j]
                if tile != None:
                    tile.draw(tile.x-xcam,tile.y-ycam)
                if DEBUG:
                    game.debug_txt(str(j)+','+str(i), (j*HTILE-xcam,i*WTILE-ycam),YELLOW)
        
    

    

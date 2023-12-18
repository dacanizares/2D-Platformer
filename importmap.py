import json
import game
from constants import *
import pygame
from pygame.locals import *

class Tile:
    def __init__(self, x, y, tileset):
        self.x = x
        self.y = y
        self.tileset = tileset

    def draw(self, x, y):
        game.draw_tile( self.tileset.sheet, (x, y), 
                        pygame.Rect(self.x, 
                                    self.y,
                                    self.tileset.tilew, 
                                    self.tileset.tileh), 
                        game.to_rgb(self.tileset.alpha_color))

class Tileset:
    def __init__(self, path, w, h, tilew, tileh, margin, spacing, firstgid, alpha_color):
        self.path = path
        self.w = w
        self.h = h
        self.tilew = tilew
        self.tileh = tileh
        self.margin = margin
        self.spacing = spacing
        self.firstgid = firstgid
        self.alpha_color = alpha_color
        self.sheet = game.load_image(self.path)

class Tilemap:
    def __init__(self):
        self.gindex = {}  
        self.tilesets = []
        self.current_map = None
        self.current_width = 0
        self.current_height = 0        

    def load_tilesets(self, path):
        json_data = open(path)
        data = json.load(json_data)        

        for t in data['tilesets']:
            tileset = Tileset(t['image'], t['imagewidth'], t['imageheight'],
                              t['tilewidth'], t['tileheight'], 
                              t['margin'], t['spacing'],
                              t['firstgid'], t['transparentcolor'])
            self.tilesets.append(tileset)

        self.index_gid()
        json_data.close()
         
    def index_gid(self):
        for tileset in self.tilesets:
            gid = tileset.firstgid

            for i in range(0, tileset.h/(tileset.tileh + tileset.spacing)):
                for j in range(0, tileset.w/(tileset.tilew + tileset.spacing)):
                    x = j * (tileset.tilew + tileset.spacing) + tileset.margin
                    y = i * (tileset.tileh + tileset.spacing) + tileset.margin 
                    self.gindex[gid] = Tile(x, y, tileset)
                    gid += 1

    def load_map(self, path):
        json_data = open(path)
        data = json.load(json_data)
        self.current_height = data['height']
        self.current_width = data['width']
        
        self.current_map = []
        map_data = data['layers'][0]['data']
        for i in range(self.current_height):
            row = []
            for j in range(self.current_width):
                row.append(map_data[i * self.current_width + j])    
            self.current_map.append(row)

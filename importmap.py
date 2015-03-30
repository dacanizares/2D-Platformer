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

class Tilemap:
    def __init__(self):
        self.gindex = {}  
        self.tilesets = []

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
        height = data['height']
        width = data['width']
        tilewidth = data['tilewidth']
        return [data['layers'][0]['data'],width,height,tilewidth]

t = Tilemap()
t.load_tilesets('map-sm.json')
map = t.load_map('map-sm.json')


game.start(DISP_W, DISP_H)
clock = game.clock()

pygame.mixer.init()
pygame.mixer.music.load("sound/hyperfun.mp3")
pygame.mixer.music.play()

# Gameloop
while True:
    events = game.get_events()
    if 'QUIT' in events:
        game.quit_game()
        break
    
    game.clear()

    x = 0
    y = 0
    for d in map[0]:
        if d != 0:
            tile = t.gindex[d]
            # Killing fps
            game.draw(game.load_sprite(game.load_image(tile.tileset.path),pygame.Rect(tile.x,tile.y,tile.tileset.tilew,tile.tileset.tileh),
                                       (0,0,0)), (x*tile.tileset.tilew,y*tile.tileset.tileh))
        x+=1
        if x >= map[1]:
            x=0
            y+=1
    
    clock.tick(30)
    game.debug_txt('FPS: '+str(clock.get_fps()), (750,580),RED) 
    
    game.update()
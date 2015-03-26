import game
import pygame
from constants import *
from resources import *
from player import *
from tile import *
from tilemap import *
from camera import *
from gamelogic import *


# Game starts!
game.start(DISP_W, DISP_H)

resources = Resources()

player = Player(128, 64, pygame.Rect(0,0,30,70), resources.player)
tiles = [[1,-1,-1,-1,-1,-1,-1,-1],
         [1,-1,-1, 1, 1,-1,-1,-1],
         [1,-1,-1,-1,-1,-1, 0, 0],
         [1,-1,-1,-1,-1,-1,-1, 1],
         [1, 0, 0,-1,-1, 0, 1, 1],
         [1, 1, 1, 0, 0, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1]]
camera = Camera(0, 0, player, Tilemap(tiles, resources.tiles))
gamelogic = Gamelogic(player, tiles)

clock = game.clock()

# Gameloop
while True:
    events = game.get_events()
    if 'QUIT' in events:
        game.quit_game()
        break
    
    game.clear()

    gamelogic.update(events)
    camera.update()
    camera.draw()
    
    game.update()
    
    clock.tick(30)

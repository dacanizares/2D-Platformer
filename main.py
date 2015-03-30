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

player = Player(128, 64, pygame.Rect(128,64,30,70), resources.player)
tiles = [[1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [1,-1,-1, 1, 1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 0, 0,-1],
         [1,-1,-1,-1,-1,-1, 0, 0, 0, 0, 0, 0, 0, 0,-1,-1,-1, 0, 0,-1,-1],
         [1,-1,-1,-1,-1,-1,-1, 1, 1, 1, 1, 1, 1, 1, 0,-1,-1,-1,-1,-1,-1],
         [1, 0, 0,-1,-1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,-1,-1,-1,-1, 0],
         [1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
camera = Camera(0, 0, player, Tilemap(tiles, resources.tiles))
gamelogic = Gamelogic(player, tiles)

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

    gamelogic.update(events)
    camera.update()
    camera.draw()

    clock.tick(30)
    game.debug_txt('FPS: '+str(clock.get_fps()), (750,580),RED) 
    
    game.update()
    
    

import game
import pygame
from constants import *
from resources import *
from player import *
from tile import *
from tilemap import *
from tileset import *
from camera import *
from gamelogic import *


# Game starts!
game.start(DISP_W, DISP_H)

resources = Resources()

player = Player(0, 0, pygame.Rect(128,64,30,70), resources.player)
tilemap = Tilemap()
tilemap.load_tilesets('map-sm.json')
tilemap.load_map('mapa-sm2.json')
camera = Camera(0, 0, player, tilemap)
gamelogic = Gamelogic(player, tilemap)

clock = game.clock()

pygame.mixer.init()
pygame.mixer.music.load("sound/hyperfun.mp3")
pygame.mixer.music.play(100)

sheet = game.load_image('graphics/blocks1.png')


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
    
    

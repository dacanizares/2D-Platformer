from camera import render
from character import *
import game
import pygame
from constants import *
from game_scripts import start_characters, update_camera, update_characters
from game_structs import Camera, Character, CharacterBehavior, CharacterConfig
from resources import *

from controlled_character import *
from tilemap_scripts import load_map


# Game starts!
game.start(DISP_W, DISP_H)

resources = Resources()

player = Character(40, 40, pygame.Rect(0,0,20,25), resources.player[0], resources.player[1], resources.player[2])
player_behavior = CharacterBehavior(update_player, on_land, on_peak, on_air, on_left, on_right, on_start)
player_config = CharacterConfig(player, player_behavior)
#ai = ControlledCharacter(100, 40, pygame.Rect(0,0,20,25), resources.player)
tilemap = load_map('map1.json')
camera = Camera(0, 0, offset=0.5, always_centered=False)

characters = [player]
characters_config = [player_config]#, ai]

clock = game.clock()

pygame.mixer.init()
pygame.mixer.music.load("sound/hyperfun.mp3")
pygame.mixer.music.play(100)

sheet = game.load_image('graphics/blocks1.png')


# Gameloop
start_characters(characters_config)
while True:
    
    events = game.get_events()
    if 'QUIT' in events:
        game.quit_game()
        break
    
    game.clear()

    update_characters(characters_config, events, tilemap)
    update_camera(camera, player)
    render(camera, characters, tilemap)    
    game.debug_txt('FPS: '+str(clock.get_fps())[:4], (540,380),RED)    
    game.update()
    clock.tick(60)
    
    

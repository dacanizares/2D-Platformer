﻿import pygame
import game_sdl
from constants import *
from characters import *
from camera import render
from game_structs import Camera, Character, CharacterBehavior, CharacterBehaviors
from game_scripts import start_characters, update_camera, update_characters
from sprites import load_sprites
from tilemap_scripts import load_map


# Game starts!
game_sdl.start(DISP_W, DISP_H)
spr_idle, spr_walk, spr_jump = load_sprites()

player = Character(40, 40, pygame.Rect(0,0,20,25), spr_idle, spr_walk, spr_jump, CharacterBehaviors.PLAYER)
jumping_ai = Character(60, 40, pygame.Rect(0,0,20,25), spr_idle, spr_walk, spr_jump, CharacterBehaviors.JUMPING_AI)
basic_ai = Character(100, 40, pygame.Rect(0,0,20,25), spr_idle, spr_walk, spr_jump, CharacterBehaviors.BASIC_AI)

tilemap = load_map('maps/map1.json')
camera = Camera(0, 0, offset=0.3, always_centered=False)

characters = [player, jumping_ai, basic_ai]

clock = game_sdl.clock()

pygame.mixer.init()
pygame.mixer.music.load("sound/hyperfun.mp3")
pygame.mixer.music.play(100)

sheet = game_sdl.load_image('graphics/blocks1.png')

# Gameloop
start_characters(characters, character_behaviors)
while True:    
    events = game_sdl.get_events()
    if 'QUIT' in events:
        game_sdl.quit_game()
        break
    
    game_sdl.clear()
    update_characters(characters, character_behaviors, events, tilemap)
    update_camera(camera, player)
    render(camera, characters, tilemap)
    game_sdl.debug_txt('FPS: '+str(clock.get_fps())[:4], (540,380),RED)  
    game_sdl.update()
    clock.tick(60)

﻿import pygame
import game_sdl
from constants import *
from characters import *
from game_render import *
from game_structs import *
from game_scripts import *
from sprites import load_sprites
from tilemap_scripts import load_map


# Game starts!
game_sdl.start(DISP_W, DISP_H)
sprites_player = load_sprites(True)
sprites_computer = load_sprites(False)

# Map
tilemap = load_map('maps/map1.json')
process_tilemap(tilemap)
(characters, player) = spawn_characters(tilemap, sprites_player, sprites_computer)
camera = Camera(0, 0, always_centered=False)

# Music
pygame.mixer.init()
pygame.mixer.music.load("sound/hyperfun.mp3")
pygame.mixer.music.play(100)

# Gameloop
start_characters(characters, character_behaviors)
clock = game_sdl.clock()
while True:    
    events = game_sdl.get_events()
    if 'QUIT' in events:
        game_sdl.quit_game()
        break
    
    game_sdl.clear()
    update_characters(characters, character_behaviors, events, tilemap)
    update_camera(camera, player)
    render(camera, characters, tilemap)
    if DEBUG_FPS:
        game_sdl.debug_txt('FPS: '+str(clock.get_fps())[:4], (540,380),RED)  
    game_sdl.update()
    clock.tick(FPS)

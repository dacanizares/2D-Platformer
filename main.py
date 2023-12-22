import pygame
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
sprites = load_sprites()

# Characters
player = Character(40, 40, pygame.Rect(0,0,20,25), CharacterAnim(sprites), CharacterBehaviors.PLAYER)
jumping_ai = Character(60, 40, pygame.Rect(0,0,20,25), CharacterAnim(sprites), CharacterBehaviors.JUMPING_AI)
basic_ai = Character(100, 40, pygame.Rect(0,0,20,25), CharacterAnim(sprites), CharacterBehaviors.BASIC_AI)
characters = [player, jumping_ai, basic_ai]

# Map
tilemap = load_map('maps/map1.json')
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
    game_sdl.debug_txt('FPS: '+str(clock.get_fps())[:4], (540,380),RED)  
    game_sdl.update()
    clock.tick(FPS)

from camera import render
from character import *
import game
import pygame
from constants import *
from game_scripts import start_characters, update_camera, update_characters
from game_structs import Camera, Character, CharacterBehavior, CharacterBehaviors
from sprites import load_sprites
from tilemap_scripts import load_map


# Game starts!
game.start(DISP_W, DISP_H)
spr_idle, spr_walk, spr_jump = load_sprites()

player = Character(40, 40, pygame.Rect(0,0,20,25), spr_idle, spr_walk, spr_jump, CharacterBehaviors.PLAYER)
jumping_ai = Character(60, 40, pygame.Rect(0,0,20,25), spr_idle, spr_walk, spr_jump, CharacterBehaviors.JUMPING_AI)
basic_ai = Character(100, 40, pygame.Rect(0,0,20,25), spr_idle, spr_walk, spr_jump, CharacterBehaviors.BASIC_AI)

tilemap = load_map('maps/map1.json')
camera = Camera(0, 0, offset=0.3, always_centered=False)

characters = [player, jumping_ai, basic_ai]

clock = game.clock()

pygame.mixer.init()
pygame.mixer.music.load("sound/hyperfun.mp3")
pygame.mixer.music.play(100)

sheet = game.load_image('graphics/blocks1.png')

# Gameloop
start_characters(characters, character_behaviors)
while True:    
    events = game.get_events()
    if 'QUIT' in events:
        game.quit_game()
        break
    
    game.clear()
    update_characters(characters, character_behaviors, events, tilemap)
    update_camera(camera, player)
    render(camera, characters, tilemap)
    game.debug_txt('FPS: '+str(clock.get_fps())[:4], (540,380),RED)  
    game.update()
    clock.tick(60)

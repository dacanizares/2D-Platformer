import game_sdl
import pygame
from pygame.locals import *
from game_structs import CharacterAnims

def get_walk_rects(player: bool) -> list[pygame.Rect]:
    if player:
        return [pygame.Rect(112,2,26,40),
                pygame.Rect(4,4,30,38)]
    else:
        return [pygame.Rect(276,128,30,40),
                pygame.Rect(308,128,32,40)]

def get_jump_rects(player: bool) -> list[pygame.Rect]:
    if player:
        return [pygame.Rect(4,4,30,38),
                pygame.Rect(38,4,30,36)]
    else:
        return [pygame.Rect(308,128,32,40),
                pygame.Rect(344,128,30,40)]

def get_idle_rects(player: bool) -> list[pygame.Rect]:
    if player:
        return [pygame.Rect(76,2,26,40),
                pygame.Rect(112,2,24,40)]
    else:
        return [pygame.Rect(548,128,30,40),
                pygame.Rect(583,128,30,40)]


def load_sprites(player: bool) -> dict[CharacterAnims, list[list[pygame.Surface]]]:
    sheet = game_sdl.load_image('graphics/arc2.png')
    walk_right = game_sdl.load_sprites(sheet, get_walk_rects(player), (0,0,0))
    walk_left = game_sdl.flip_sprites(walk_right)

    idle_right = game_sdl.load_sprites(sheet, get_idle_rects(player), (0,0,0))
    idle_left = game_sdl.flip_sprites(idle_right)

    jump_right = game_sdl.load_sprites(sheet, get_jump_rects(player), (0,0,0))
    jump_left = game_sdl.flip_sprites(jump_right)
    return {
        CharacterAnims.IDLE: [idle_right, idle_left],
        CharacterAnims.WALK: [walk_right, walk_left],
        CharacterAnims.JUMP: [jump_right, jump_left],
        CharacterAnims.SLEEP: [idle_right, idle_left],
    }

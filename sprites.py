import game_sdl
import pygame
from pygame.locals import *
from game_structs import CharacterAnim, CharacterAnims

def load_sprites() -> dict[CharacterAnims, list[list[pygame.Surface]]]:
    sheet = game_sdl.load_image('graphics/arc2.png')
    #rects = [#pygame.Rect(514,8,24,34),
    #        pygame.Rect(550,8,30,34),
    #         pygame.Rect(582,8,28,34),
    #         pygame.Rect(550,8,30,34)]
    rects = [pygame.Rect(112,2,26,40),
            pygame.Rect(112,2,26,40),
            pygame.Rect(112,2,26,40),
            pygame.Rect(4,4,30,38),
            pygame.Rect(4,4,30,38),
            pygame.Rect(4,4,30,38)]
            
    walk_right = game_sdl.load_sprites(sheet, rects, (0,0,0))
    walk_left = game_sdl.flip_sprites(walk_right)

    rects = [pygame.Rect(76,2,26,40),
            pygame.Rect(112,2,24,40)]
    idle_right = game_sdl.load_sprites(sheet, rects, (0,0,0))
    idle_left = game_sdl.flip_sprites(idle_right)

    rects = [pygame.Rect(4,4,30,38),
            pygame.Rect(38,4,30,36)]
    jump_right = game_sdl.load_sprites(sheet, rects, (0,0,0))
    jump_left = game_sdl.flip_sprites(jump_right)
    return {
        CharacterAnims.IDLE: [idle_right, idle_left],
        CharacterAnims.WALK: [walk_right, walk_left],
        CharacterAnims.JUMP: [jump_right, jump_left],
        CharacterAnims.SLEEP: [idle_right, idle_left],
    }

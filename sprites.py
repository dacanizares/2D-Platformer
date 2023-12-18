import game
import pygame
from pygame.locals import *

def load_sprites():
    sheet = game.load_image('graphics/arc2.png')
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
            
    walk_right = game.load_sprites(sheet, rects, (0,0,0))
    walk_left = game.flip_sprites(walk_right)

    rects = [pygame.Rect(76,2,26,40),
            pygame.Rect(112,2,24,40)]
    idle_right = game.load_sprites(sheet, rects, (0,0,0))
    idle_left = game.flip_sprites(idle_right)

    rects = [pygame.Rect(4,4,30,38),
            pygame.Rect(38,4,30,36)]
    jump_right = game.load_sprites(sheet, rects, (0,0,0))
    jump_left = game.flip_sprites(jump_right)
    return ([idle_right, idle_left],
            [walk_right,walk_left],            
            [jump_right, jump_left])

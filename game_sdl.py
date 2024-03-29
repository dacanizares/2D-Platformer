﻿import pygame
from pygame import *
from tilemap_structs import Tile, Tileset

def start(w,h):
    print('One second, we are awakening the character.')
    pygame.init()
    flags = DOUBLEBUF
    pygame.display.set_mode((w * 2, h * 2), flags)
    print('Lets go!')

def apply_alpha(image, colorkey):
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

def load_image(path: str, colorkey = None):    
    image = pygame.image.load(path.strip('../')).convert()
    apply_alpha(image, colorkey)
    return image

def load_sprite(sheet, rectangle, colorkey = (0, 0, 0)):    
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size).convert()
    image.blit(sheet, (0, 0), rect)
    apply_alpha(image, colorkey)
    return image
     
def load_sprites(sheet, rects, colorkey = (0, 0, 0)):
    return [load_sprite(sheet, rect, colorkey) for rect in rects]

def flip_sprites(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]
    
def clear():
    screen = pygame.display.get_surface()
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0, 0))

def draw(image: Surface, xy: tuple):
    screen = pygame.display.get_surface()
    screen.blit(image, xy)

def draw_from_tileset(tileset: Tileset, xy: tuple, rect: pygame.Rect, colorkey=None, surface: pygame.Surface = None):   
    if (surface is None):
        surface = pygame.display.get_surface()
    image = pygame.Surface(rect.size)
    image.blit(tileset.sheet, (0, 0), rect)
    apply_alpha(image, colorkey)
    surface.blit(image, xy)

def draw_tile(tileset: Tileset, tile: Tile, xy: tuple, surface: pygame.Surface = None):
    draw_from_tileset(tileset, xy,
                      pygame.Rect(tile.x, tile.y, tileset.tilew, tileset.tileh),
                      to_rgb(tileset.alpha_color),
                      surface)

def draw_rect(rect: pygame.Rect, color = (255, 0, 0)):
    screen = pygame.display.get_surface()
    pygame.draw.rect(screen, color, rect)

def draw_rect_borders(rect: pygame.Rect, border_size=1, color = (255, 0, 0)):
    draw_rect(pygame.Rect(rect.x, rect.y, rect.w, border_size), color)
    draw_rect(pygame.Rect(rect.x, rect.y, border_size, rect.h), color)
    draw_rect(pygame.Rect(rect.x, rect.y + rect.h, rect.w, border_size), color)
    draw_rect(pygame.Rect(rect.x + rect.w, rect.y, border_size, rect.h), color)

def debug_txt(txt, xy, color):
    font = pygame.font.Font(None, 12)
    text = font.render(txt, 1, color)
    screen = pygame.display.get_surface()
    screen.blit(text, xy)


def update():
    screen = pygame.display.get_surface()
    screen.blit(pygame.transform.scale2x(screen), (0, 0))
    pygame.display.flip()

def get_events():
    events = {}
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            events[event.key] = True
        if event.type == KEYUP:
            events[event.key] = False
        elif event.type == QUIT:
            events['QUIT'] = True
    return events     

def quit_game():
    pygame.quit()

def clock():
    return pygame.time.Clock()

def to_rgb(color: str):
    hex_value = color.lstrip('#')
    return tuple(int(hex_value[i : i + 2], 16) for i in (0, 2, 4))

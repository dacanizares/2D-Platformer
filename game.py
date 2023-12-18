import pygame
from pygame import *
from tilemap_structs import Tile, Tileset

def start(w,h):
    print('One second, we are awakening the character.')
    pygame.init()
    pygame.display.set_mode((w, h))
    print('Lets go!')

def apply_alpha(image, colorkey):
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)

def load_image(path, colorkey = None):
    image = pygame.image.load(path).convert()
    apply_alpha(image, colorkey)
    return image

def load_sprite(sheet, rectangle, colorkey = (0,0,0)):    
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size).convert()
    image.blit(sheet, (0, 0), rect)
    apply_alpha(image, colorkey)
    return image
     
def load_sprites(sheet, rects, colorkey = (0,0,0)):
    return [load_sprite(sheet, rect, colorkey) for rect in rects]

def flip_sprites(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]
    
def clear():
    screen = pygame.display.get_surface()
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    screen.blit(background, (0,0))

def draw(image: Surface, xy: tuple):
    screen = pygame.display.get_surface()
    screen.blit(image, xy)


def draw_from_tileset(tileset: Tileset, xy: tuple, rect: pygame.Rect, colorkey=None):   
    screen = pygame.display.get_surface()
    image = pygame.Surface(rect.size)
    image.blit(tileset.sheet, (0, 0), rect)
    apply_alpha(image, colorkey)
    screen.blit(image, xy)

def draw_tile(tileset: Tileset, tile: Tile, xy: tuple):
    draw_from_tileset(tileset, xy,
                      pygame.Rect(tile.x, tile.y, tileset.tilew, tileset.tileh),
                      to_rgb(tileset.alpha_color))

def draw_rect(rect):
    screen = pygame.display.get_surface()
    pygame.draw.rect(screen, (255,0,0), rect)

def debug_txt(txt,xy,color):
    font = pygame.font.Font(None, 12)
    text = font.render(txt, 1, color)
    screen = pygame.display.get_surface()
    screen.blit(text, xy)


def update():
    screen = pygame.display.get_surface()
    #screen.blit(pygame.transform.scale2x(screen), (0,0))
    screen.blit(screen, (0,0))
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


def new_rect(x, y, size):
    return pygame.Rect(x, y, size[0], size[1])

def to_rgb(color: str):
    hex_value = color.lstrip('#')
    return tuple(int(hex_value[i:i+2], 16) for i in (0, 2, 4))

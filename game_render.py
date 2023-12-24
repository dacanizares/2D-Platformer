import math
import pygame
import game_sdl
from constants import *
from game_structs import Camera, Character, CharacterAnims, CharacterBehaviors
from tilemap_structs import Tilemap


chunks: list[list[pygame.Surface]]
chunk_size: int = 8
chunk_dim: tuple[int, int]

def process_chunk(x: int, y: int, tilemap: Tilemap) -> pygame.Surface:
    global chunk_dim
    surface = pygame.Surface(chunk_dim)
    x *= chunk_size
    y *= chunk_size 
    for chunk_y in range(0, chunk_size):
        for chunk_x in range(0, chunk_size):
            if y + chunk_y >= tilemap.current_height or x + chunk_x >= tilemap.current_width:
                continue
            tile_id = tilemap.current_map[y + chunk_y][x + chunk_x]
            if tile_id != 0:
                tile = tilemap.gindex[tile_id]
                tileset = tilemap.tilesets[tile.tileset_idx]
                game_sdl.draw_tile(tileset, tile, (chunk_x * tilemap.tilew, chunk_y * tilemap.tileh), surface)
    return surface

def process_tilemap(tilemap: Tilemap):
    global chunk_dim, chunks
    chunks = []
    chunk_dim = (tilemap.tilew * chunk_size, tilemap.tileh * chunk_size)
    for y in range(0, math.ceil(tilemap.current_height / chunk_size)):
        chunks.append([])
        for x in range(0, math.ceil(tilemap.current_width / chunk_size)):
            chunks[y].append(process_chunk(x, y, tilemap))

def get_chunk(x: int, y: int) -> tuple[int, int]:
    return (int(x / chunk_size), int(y / chunk_size))

def render(camera: Camera, characters: list[Character], tilemap: Tilemap):
    starting_x = int((camera.x - 1) / tilemap.tilew)
    starting_y = int((camera.y - 1) / tilemap.tileh)

    ending_x = int((camera.x + DISP_W + 1) / tilemap.tilew)
    ending_y = int((camera.y + DISP_H + 1) / tilemap.tileh)

    # Render Tilemap
    if not RENDER_CHUNKS:
        for i in range(starting_y, ending_y+1):
            if i < 0 or i >= tilemap.current_height:
                continue
            for j in range(starting_x, ending_x+1):
                if j < 0 or j >= tilemap.current_width:
                    continue

                tile_id = tilemap.current_map[i][j]
                if tile_id != 0:
                    tile = tilemap.gindex[tile_id]
                    tileset = tilemap.tilesets[tile.tileset_idx]
                    x = j * tileset.tilew - camera.x
                    y = i * tileset.tileh - camera.y
                    game_sdl.draw_tile(tileset, tile, (x, y))
                    if DEBUG:
                        game_sdl.debug_txt(str(i)+','+str(j), (x,y), RED)
    else:
        chunks_to_draw: list[tuple[int, int]] = []
        for i in range(starting_y, ending_y + 1):
            if i < 0 or i >= tilemap.current_height:
                continue
            for j in range(starting_x, ending_x + 1):
                if j < 0 or j >= tilemap.current_width:
                    continue
                chunk_coord = get_chunk(j, i)
                if chunk_coord not in chunks_to_draw:
                    chunks_to_draw.append(chunk_coord)
        
        screen = pygame.display.get_surface()
        for chunk_coord in chunks_to_draw:
            if chunk_coord[1] >= len(chunks) or chunk_coord[0] >= len(chunks[chunk_coord[1]]):
                continue
            chunk = chunks[chunk_coord[1]][chunk_coord[0]]
            chunk_x = chunk_coord[0] * chunk_dim[0]
            chunk_y = chunk_coord[1] * chunk_dim[1]
            screen.blit(chunk, (chunk_x - camera.x, chunk_y - camera.y))
    
    # Render Characters
    for character in characters:
        draw_character(character, character.x - camera.x, character.y - camera.y)
    if DEBUG_COLL_BOT:
        for debug_rect in tilemap.debug_rects:
            tile_x = debug_rect[1] * tilemap.tilew
            tile_y = debug_rect[0] * tilemap.tileh
            game_sdl.draw_rect(pygame.Rect(tile_x - camera.x, tile_y - camera.y, tilemap.tilew, tilemap.tileh), RED)
        tilemap.debug_rects = []


def get_next_frame_update(state: CharacterAnims):
    if state == CharacterAnims.IDLE:
        return IDLE_ANIM_X_FRAMES
    else:
        return ANIM_EVERY_X_FRAMES

def draw_character(character: Character, xcam: float, ycam: float):
    # Set direction data
    if character.direction:
        anim_index = 0
    else:
        anim_index = 1

    # Anim states
    last_anim_state = character.anim.state

    # Set current anim state and frame
    if not character.land and not character.sleep:
        character.anim.state = CharacterAnims.JUMP
        if character.vy < 0:            
            character.anim.frame = 0
        else:
            character.anim.frame = 1
    else:
        if character.sleep:
            character.anim.state = CharacterAnims.SLEEP
        elif character.left or character.right:
            character.anim.state = CharacterAnims.WALK
        else:
            character.anim.state = CharacterAnims.IDLE
        
        # Changed anim?
        if character.anim.state != last_anim_state:
            character.anim.frame = 0
            character.anim.next_update = get_next_frame_update(character.anim.state)
        else:
            # Update frame and loop
            character.anim.next_update -= 1
            if character.anim.next_update == 0:
                character.anim.frame = (character.anim.frame + 1) % len(character.anim.sets[character.anim.state][anim_index])
                character.anim.next_update = get_next_frame_update(character.anim.state)
    
    sprite = character.anim.sets[character.anim.state][anim_index][character.anim.frame]

    # Center image
    xoffset = -sprite.get_width() / 2
    yoffset = -sprite.get_height()
    game_sdl.draw(sprite, (xcam + xoffset, ycam + yoffset))
    if DEBUG:
        game_sdl.draw_rect(pygame.Rect(xcam - character.collider.w/2, ycam - character.collider.h, character.collider.w, character.collider.h))

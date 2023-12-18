import pygame
import game_sdl
from constants import *
from game_structs import Camera, Character
from tilemap_structs import Tilemap


def render(camera: Camera, characters: list[Character], tilemap: Tilemap):
    starting_x = int((camera.x - 1) / tilemap.tilew)
    starting_y = int((camera.y - 1) / tilemap.tileh)

    ending_x = int((camera.x + DISP_W + 1) / tilemap.tilew)
    ending_y = int((camera.y + DISP_H + 1) / tilemap.tileh)

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
    for character in characters:
        draw_character(character, character.x - camera.x, character.y - camera.y)


def draw_character(character: Character, xcam, ycam):
    if character.direction:
        anim_index = 0
    else:
        anim_index = 1
        
    if not character.land:
        if character.vy < 0:
            sprite = character.jumping[anim_index][1]
        else:
            sprite = character.jumping[anim_index][0]
    else:
        if character.right or character.left:
            sprite = character.walking[anim_index][character.frame]
            character.frame = (character.frame + 1) % len(character.walking[anim_index])                
        else:
            character.delta_frames = (character.delta_frames + 1) % 120                
            if character.delta_frames < 90:
                sprite = character.idle[anim_index][0]
            else:
                sprite = character.idle[anim_index][1]

    # Center image
    xoffset = -sprite.get_width()/2
    yoffset = -sprite.get_height()
    game_sdl.draw(sprite, (xcam + xoffset, ycam + yoffset))
    if DEBUG:
        game_sdldraw_rect(pygame.Rect(xcam - character.collider.w/2, ycam - character.collider.h, character.collider.w, character.collider.h))

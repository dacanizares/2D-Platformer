import pygame
import game_sdl
from constants import *
from game_structs import Camera, Character, CharacterAnims, CharacterBehaviors
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

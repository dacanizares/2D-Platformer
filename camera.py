import game
from constants import *


def render(camera, actors, tilemap):
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
                game.draw_tile(tileset, tile, (x, y))
                if DEBUG:
                    game.debug_txt(str(i)+','+str(j), (x,y), RED)
    for actor in actors:
        actor.draw(actor.x - camera.x, actor.y - camera.y)

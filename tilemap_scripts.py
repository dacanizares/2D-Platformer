import game_sdl
import json
from game_structs import CharacterBehaviors
from tilemap_structs import Tile, Tilemap, TilemapCharacters, Tileset

def load_map(path):
    json_data = open(path)
    data = json.load(json_data)

    tilemap = Tilemap()
    tilemap.tilew = data['tilewidth']
    tilemap.tileh = data['tileheight']

    for t in data['tilesets']:
        tileset = Tileset(t['image'], t['imagewidth'], t['imageheight'],
                            t['tilewidth'], t['tileheight'], 
                            t['margin'], t['spacing'],
                            t['firstgid'], t['transparentcolor'],
                            game_sdl.load_image(t['image']))
        tilemap.tilesets.append(tileset)

        if 'tiles' in t:
            for tile_meta in t['tiles']:
                tile_id = tile_meta['id']
                tile_props = tile_meta['properties']
                for tile_prop in tile_props:
                    if tile_prop['name'] == 'NoCollide' and tile_prop['value'] == '1':
                        tilemap.no_collision[int(tile_id) + tileset.firstgid] = True
                    if tile_prop['name'] == 'NoPeak' and tile_prop['value'] == '1':
                        tilemap.no_peak[int(tile_id) + tileset.firstgid] = True
                    if tile_prop['name'] == 'CollDy':
                        tilemap.coll_dy[int(tile_id) + tileset.firstgid] = int(tile_prop['value'])

    # Index GUIDs
    for tileset_idx in range(0, len(tilemap.tilesets)):
        tileset = tilemap.tilesets[tileset_idx]
        gid = tileset.firstgid

        for i in range(0, int(tileset.h/(tileset.tileh + tileset.spacing))):
            for j in range(0, int(tileset.w/(tileset.tilew + tileset.spacing))):
                x = j * (tileset.tilew + tileset.spacing) + tileset.margin
                y = i * (tileset.tileh + tileset.spacing) + tileset.margin 
                tilemap.gindex[gid] = Tile(x, y, tileset_idx)
                gid += 1

    # Load map itself
    tilemap.current_height = data['height']
    tilemap.current_width = data['width']
    
    tilemap.current_map = []

    layer_terrain = 0
    layer_characters = 1
    map_data = data['layers'][layer_terrain]['data']
    for i in range(tilemap.current_height):
        row = []
        for j in range(tilemap.current_width):
            row.append(map_data[i * tilemap.current_width + j])    
        tilemap.current_map.append(row)

    char_data = data['layers'][layer_characters]['objects']
    for char in char_data:
        char_type = char['type'].upper()
        char_x = int(char['x'])
        char_y = int(char['y'])
        if char_type == 'PLAYER':
            char_type = CharacterBehaviors.PLAYER
        elif char_type == 'JUMPINGAI':
            char_type = CharacterBehaviors.JUMPING_AI
        else:
            char_type = CharacterBehaviors.BASIC_AI
        tilemap.characters_to_spawn.append(TilemapCharacters(char_type, char_x, char_y))
    
    json_data.close()

    return tilemap

def get_coll_dy(tilemap: Tilemap, tile_id: int) -> int:
    if tile_id not in tilemap.coll_dy:
        return 0
    else:
        return tilemap.coll_dy[tile_id]

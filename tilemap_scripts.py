import game
import json
from tilemap_structs import Tile, Tilemap, Tileset

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
                            game.load_image(t['image']))
        tilemap.tilesets.append(tileset)

        if 'tiles' in t:
            for tile_meta in t['tiles']:
                tile_id = tile_meta['id']
                tile_props = tile_meta['properties']
                for tile_prop in tile_props:
                    if tile_prop['name'] == 'NoCollide' and tile_prop['value'] == '1':
                        tilemap.no_collision[int(tile_id) + tileset.firstgid] = True

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
    map_data = data['layers'][0]['data']#CHANGE THIS!
    for i in range(tilemap.current_height):
        row = []
        for j in range(tilemap.current_width):
            row.append(map_data[i * tilemap.current_width + j])    
        tilemap.current_map.append(row)

    json_data.close()

    return tilemap


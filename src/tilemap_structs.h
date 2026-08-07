#ifndef PLATFORMER_TILEMAP_STRUCTS_H
#define PLATFORMER_TILEMAP_STRUCTS_H

#include <stdbool.h>
#include "raylib.h"
#include "game_structs.h"

typedef struct TilemapCharacter {
    CharacterBehaviorType behavior_type;
    int x;
    int y;
} TilemapCharacter;

/* Tile coordinates in the tileset image. */
typedef struct Tile {
    int x;
    int y;
    int tileset_idx;
} Tile;

/* Tileset metadata and its loaded image. */
typedef struct Tileset {
    char path[256];
    int w;
    int h;
    int tilew;
    int tileh;
    int margin;
    int spacing;
    int firstgid;
    Color alpha_color;
    Texture2D sheet;
} Tileset;

typedef struct Tilemap {
    Tile *gindex;
    int gindex_count;
    Tileset *tilesets;
    int tileset_count;
    int *current_map;
    int current_width;
    int current_height;
    int tilew;
    int tileh;
    TilemapCharacter *characters_to_spawn;
    int spawn_count;
    bool *no_collision;
    bool *no_peak;
    int *coll_dy;
} Tilemap;

#endif

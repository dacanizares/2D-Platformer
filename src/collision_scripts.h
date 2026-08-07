#ifndef PLATFORMER_COLLISION_SCRIPTS_H
#define PLATFORMER_COLLISION_SCRIPTS_H

#include <stdbool.h>
#include "game_structs.h"
#include "tilemap_structs.h"

typedef struct TileProjection {
    int left;
    int right;
    int top;
    int bottom;
} TileProjection;

typedef struct CollisionSearch {
    int position;
    int coll_dy;
} CollisionSearch;

TileProjection project_collider_to_tilemap(const Character *character, const Tilemap *tilemap);
CollisionSearch search_collisions(const Tilemap *tilemap, int start, int a, int b,
                                  int dx, int dy, bool ignore_no_peak);

#endif

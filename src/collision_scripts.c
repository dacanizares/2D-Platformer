#include "collision_scripts.h"
#include "constants.h"
#include "tilemap_scripts.h"

TileProjection project_collider_to_tilemap(const Character *character, const Tilemap *tilemap) {
    /* Project the character collider to the tilemap. The collider's center
       point is at the character's middle-bottom position. */
    const Rectangle coll = character->collider;
    return (TileProjection){
        .left = (int)((coll.x - coll.width / 2.0f + 1.0f) / (float)tilemap->tilew),
        .right = (int)((coll.x + coll.width / 2.0f - 1.0f) / (float)tilemap->tilew),
        .top = (int)((coll.y - coll.height + 1.0f - (float)character->coll_dy) / (float)tilemap->tileh),
        .bottom = (int)((coll.y - 1.0f - (float)character->coll_dy) / (float)tilemap->tileh)
    };
}

CollisionSearch search_collisions(const Tilemap *map, int start, int a, int b,
                                  int dx, int dy, bool ignore_no_peak) {
    /* Search for static objects to collide with.
       start: starting point
       a: lower bound
       b: upper bound (a < b)
       dx, dy: moving direction

       Returns no collision when none is found; otherwise returns the row or
       column containing the collider.

       Example: to trace from x = 1, to the left, from tiles y = 2 to y = 3:
           search(1, 2, 5, 1, 0)

       Result:
         0 1 2 3 4 5 ... MAX_DIST_COL
       0 . . . . . .
       1 . . . . . .
       2 . X X X X X
       3 . X X X X X
       4 . . . . . .

       The search scans the positions marked with X. */
    /* Validate that the search is locked to one axis. */
    if ((dx != 0 && dy != 0) || (dx == 0 && dy == 0) || a < 0) return (CollisionSearch){-1, 0};
    int limit = -1;
    if (dx > 0) limit = map->current_width;
    else if (dy > 0) limit = map->current_height;

    /* Set the limits according to the direction of travel, then scan. */
    for (int distance = 1; distance < MAX_DIST_COL; ++distance) {
        start += dx + dy;
        /* Stop when the map boundary or maximum search distance is reached. */
        if (start == limit || start < 0) return (CollisionSearch){start, 0};
        for (int i = a; i <= b; ++i) {
            int row = dx != 0 ? i : start;
            int col = dx != 0 ? start : i;
            int tile_id = 0;
            if (row >= 0 && row < map->current_height && col >= 0 && col < map->current_width) {
                tile_id = map->current_map[row * map->current_width + col];
            }
            bool valid = tile_id >= 0 && tile_id < map->gindex_count;
            bool collides = valid && !map->no_collision[tile_id];
            if (dx != 0) {
                if (collides && !map->no_peak[tile_id]) return (CollisionSearch){start, 0};
            } else if (collides && (ignore_no_peak || !map->no_peak[tile_id])) {
                return (CollisionSearch){start, get_coll_dy(map, tile_id)};
            }
        }
    }
    return (CollisionSearch){start, 0};
}

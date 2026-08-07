#ifndef PLATFORMER_TILEMAP_SCRIPTS_H
#define PLATFORMER_TILEMAP_SCRIPTS_H

#include <stdbool.h>
#include "tilemap_structs.h"

bool load_map(Tilemap *tilemap, const char *path);
void unload_map(Tilemap *tilemap);
int get_coll_dy(const Tilemap *tilemap, int tile_id);

#endif

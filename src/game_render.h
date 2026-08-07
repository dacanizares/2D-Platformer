#ifndef PLATFORMER_GAME_RENDER_H
#define PLATFORMER_GAME_RENDER_H

#include "game_structs.h"
#include "tilemap_structs.h"

void process_tilemap(Tilemap *tilemap);
void render(const GameCamera *camera, Character *characters, int character_count,
            const Tilemap *tilemap);

#endif

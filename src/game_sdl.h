#ifndef PLATFORMER_GAME_SDL_H
#define PLATFORMER_GAME_SDL_H

#include <stdbool.h>
#include "raylib.h"
#include "game_structs.h"
#include "tilemap_structs.h"

bool start(int width, int height);
void quit_game(void);
InputState get_events(void);
void clear(RenderTexture2D target);
void update(RenderTexture2D target);
void draw_tile(const Tileset *tileset, const Tile *tile, float x, float y);

#endif

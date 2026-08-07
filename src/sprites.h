#ifndef PLATFORMER_SPRITES_H
#define PLATFORMER_SPRITES_H

#include <stdbool.h>
#include "game_structs.h"

bool load_sprites(CharacterSprites *sprites, bool player);
void unload_sprites(CharacterSprites *sprites);

#endif

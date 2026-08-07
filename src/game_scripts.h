#ifndef PLATFORMER_GAME_SCRIPTS_H
#define PLATFORMER_GAME_SCRIPTS_H

#include <stdbool.h>
#include "game_structs.h"
#include "tilemap_structs.h"

bool spawn_characters(const Tilemap *tilemap, CharacterSprites *player_sprites,
                      CharacterSprites *computer_sprites, Character **characters,
                      int *character_count, Character **player);
void start_characters(Character *characters, int character_count);
void update_characters(Character *characters, int character_count,
                       const InputState *input, const Tilemap *tilemap);
void update_camera(GameCamera *camera, const Character *focus);

#endif

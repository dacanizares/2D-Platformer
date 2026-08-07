#ifndef PLATFORMER_CHARACTERS_H
#define PLATFORMER_CHARACTERS_H

#include "game_structs.h"

extern const CharacterBehavior character_behaviors[3];

void update_character(Character *character, const InputState *input);
void update_player(Character *player, const InputState *input);

#endif

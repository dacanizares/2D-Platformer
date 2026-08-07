#include "game_scripts.h"

#include <stdlib.h>
#include "characters.h"
#include "collision_scripts.h"

static void update_character_collider(Character *character, int coll_dy) {
    character->collider = (Rectangle){
        character->x,
        character->y,
        character->w,
        character->h
    };
    character->coll_dy = coll_dy;
}

bool spawn_characters(const Tilemap *tilemap, CharacterSprites *player_sprites,
                      CharacterSprites *computer_sprites, Character **characters,
                      int *character_count, Character **player) {
    *character_count = tilemap->spawn_count;
    *characters = calloc((size_t)*character_count, sizeof(**characters));
    *player = NULL;
    if (!*characters) return false;
    for (int i = 0; i < *character_count; ++i) {
        const TilemapCharacter *spawn = &tilemap->characters_to_spawn[i];
        Character *character = &(*characters)[i];
        character->x = (float)spawn->x;
        character->y = (float)spawn->y;
        character->w = CHARACTER_COLL_W;
        character->h = CHARACTER_COLL_H;
        character->behavior_type = spawn->behavior_type;
        character->direction = true;
        character->anim.sprites = spawn->behavior_type == CHARACTER_PLAYER ? player_sprites : computer_sprites;
        character->anim.state = CHARACTER_IDLE;
        if (spawn->behavior_type == CHARACTER_PLAYER) *player = character;
    }
    return *player != NULL;
}

void start_characters(Character *characters, int count) {
    for (int i = 0; i < count; ++i) {
        update_character_collider(&characters[i], 0);
        character_behaviors[characters[i].behavior_type].on_start(&characters[i]);
    }
}

void update_characters(Character *characters, int count, const InputState *input, const Tilemap *map) {
    /* Update entities and their collision events. */
    for (int i = 0; i < count; ++i) {
        Character *character = &characters[i];
        const CharacterBehavior *behavior = &character_behaviors[character->behavior_type];
        const float previous_x = character->x;
        const float previous_y = character->y;
        behavior->update(character, input);

        /* Preserve the original two-phase pygame collision order: X projects
           the previous collider, then only collider.x is refreshed for Y. */
        /* Static collisions against the map. */
        TileProjection projection = project_collider_to_tilemap(character, map);
        /* UPDATE X: search for horizontal limits. */
        CollisionSearch min_x = search_collisions(map, projection.left, projection.top, projection.bottom, -1, 0, false);
        CollisionSearch max_x = search_collisions(map, projection.right, projection.top, projection.bottom, 1, 0, false);
        float limit = (float)(min_x.position * map->tilew + map->tilew) + character->w / 2.0f;
        if (character->x <= limit) {
            character->x = limit;
            behavior->on_left(character);
        }
        limit = (float)(max_x.position * map->tilew) - character->w / 2.0f;
        if (character->x >= limit) {
            character->x = limit;
            behavior->on_right(character);
        }
        character->collider.x = character->x;

        /* Limit X and update the collider (just X axis). */
        projection = project_collider_to_tilemap(character, map);
        CollisionSearch min_y = search_collisions(map, projection.top, projection.left, projection.right, 0, -1, false);
        CollisionSearch max_y = search_collisions(map, projection.bottom, projection.left, projection.right, 0, 1,
                                                  character->vy > 0 || character->land);
        /* UPDATE Y: search for vertical limits. */
        limit = (float)(max_y.position * map->tileh + max_y.coll_dy);
        if (character->y >= limit) {
            character->y = limit;
            behavior->on_land(character);
        } else {
            behavior->on_air(character);
            limit = (float)(min_y.position * map->tileh + map->tileh) + character->h;
            if (character->y <= limit) {
                character->y = limit;
                behavior->on_peak(character);
            }
        }
        update_character_collider(character, max_y.coll_dy);
        character->previous_x = previous_x;
        character->previous_y = previous_y;
        character->frame_dx = character->x - previous_x;
        character->frame_dy = character->y - previous_y;
    }

    /* Dynamic collisions between characters. */
    for (int a = 0; a < count - 1; ++a) {
        for (int b = a + 1; b < count; ++b) {
            Character *first = &characters[a];
            Character *second = &characters[b];
            if (CheckCollisionRecs(first->collider, second->collider)) {
                bool first_on_top = first->collider.y < second->collider.y;
                character_behaviors[first->behavior_type].on_collide(first, first_on_top);
                character_behaviors[second->behavior_type].on_collide(second, !first_on_top);
            }
        }
    }
}

void update_camera(GameCamera *camera, const Character *focus) {
    if (camera->always_centered) {
        camera->x = focus->x - DISP_W / 2.0f;
        camera->y = focus->y - DISP_H * 0.75f;
        return;
    }
    float limit_x = camera->offset_x * DISP_W;
    if (focus->x < camera->x + limit_x) camera->x = focus->x - limit_x;
    else if (focus->x > camera->x + DISP_W - limit_x) camera->x = focus->x - (DISP_W - limit_x);
    float limit_y = camera->offset_y * DISP_H;
    if (focus->y < camera->y + limit_y) camera->y = focus->y - limit_y;
    else if (focus->y > camera->y + DISP_H - limit_y) camera->y = focus->y - (DISP_H - limit_y);
}

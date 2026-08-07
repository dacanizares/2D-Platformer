#include "game_render.h"

#include "constants.h"
#include "game_sdl.h"

void process_tilemap(const Tilemap *tilemap) {
    (void)tilemap;
    /* Render tilemap chunks. raylib batches visible tiles on the GPU, so no
       software chunk cache is needed. */
}

static int get_next_frame_update(CharacterAnimState state) {
    return state == CHARACTER_IDLE ? IDLE_ANIM_X_FRAMES : ANIM_EVERY_X_FRAMES;
}

static void draw_character(Character *character, float x, float y) {
    /* Set direction data. */
    CharacterAnimState previous = character->anim.state;
    /* Animation states. */
    if (!character->land && character->sleep == 0) {
        character->anim.state = CHARACTER_JUMP;
        character->anim.frame = character->vy < 0 ? 0 : 1;
    } else {
        if (character->sleep > 0) character->anim.state = CHARACTER_SLEEP;
        else if (character->left || character->right) character->anim.state = CHARACTER_WALK;
        else character->anim.state = CHARACTER_IDLE;

        /* Changed animation? */
        if (previous != character->anim.state) {
            character->anim.frame = 0;
            character->anim.next_update = get_next_frame_update(character->anim.state);
        } else {
            --character->anim.next_update;
            if (character->anim.next_update <= 0) {
                character->anim.frame = (character->anim.frame + 1) % 2;
                character->anim.next_update = get_next_frame_update(character->anim.state);
            }
        }
    }

    /* Center image. */
    Rectangle source = character->anim.sprites->frames[character->anim.state][character->anim.frame];
    float frame_width = source.width;
    if (!character->direction) {
        source.width = -source.width;
    }
    Rectangle destination = {x - frame_width / 2.0f, y - source.height, frame_width, source.height};
    DrawTexturePro(character->anim.sprites->sheet, source, destination, (Vector2){0}, 0, WHITE);
    if (DEBUG_DRAW) {
        DrawRectangleLines((int)(x - character->collider.width / 2.0f),
                           (int)(y - character->collider.height),
                           (int)character->collider.width, (int)character->collider.height, RED);
    }
}

void render(const GameCamera *camera, Character *characters, int count, const Tilemap *map) {
    int start_x = (int)((camera->x - 1.0f) / (float)map->tilew);
    int start_y = (int)((camera->y - 1.0f) / (float)map->tileh);
    int end_x = (int)((camera->x + (float)DISP_W + 1.0f) / (float)map->tilew);
    int end_y = (int)((camera->y + (float)DISP_H + 1.0f) / (float)map->tileh);
    if (start_x < 0) start_x = 0;
    if (start_y < 0) start_y = 0;
    if (end_x >= map->current_width) end_x = map->current_width - 1;
    if (end_y >= map->current_height) end_y = map->current_height - 1;

    for (int row = start_y; row <= end_y; ++row) {
        for (int col = start_x; col <= end_x; ++col) {
            int tile_id = map->current_map[row * map->current_width + col];
            if (tile_id <= 0 || tile_id >= map->gindex_count) continue;
            const Tile *tile = &map->gindex[tile_id];
            const Tileset *set = &map->tilesets[tile->tileset_idx];
            draw_tile(set, tile, (float)(col * map->tilew) - camera->x,
                      (float)(row * map->tileh) - camera->y);
        }
    }
    for (int i = 0; i < count; ++i) {
        draw_character(&characters[i], characters[i].x - camera->x, characters[i].y - camera->y);
    }
    if (DEBUG_FPS) DrawText(TextFormat("FPS: %d", GetFPS()), DISP_W - 65, DISP_H - 18, 10, RED);
}

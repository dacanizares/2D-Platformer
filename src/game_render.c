#include "game_render.h"

#include <stdlib.h>

#include "constants.h"
#include "game_sdl.h"

#if RENDER_CHUNKS && RENDER_BACKEND == RENDER_BACKEND_GPU
static void draw_tile_at(const Tilemap *map, int tile_id, int x, int y) {
    if (tile_id <= 0 || tile_id >= map->gindex_count) return;
    const Tile *tile = &map->gindex[tile_id];
    const Tileset *set = &map->tilesets[tile->tileset_idx];
    Rectangle source = {(float)tile->x, (float)tile->y,
                       (float)set->tilew, (float)set->tileh};
    DrawTextureRec(set->sheet, source, (Vector2){(float)x, (float)y}, WHITE);
}
#endif

void process_tilemap(Tilemap *tilemap) {
#if RENDER_CHUNKS
    tilemap->chunk_count = ((tilemap->current_width + CHUNK_SIZE - 1) / CHUNK_SIZE) *
                           ((tilemap->current_height + CHUNK_SIZE - 1) / CHUNK_SIZE);
    tilemap->chunks = calloc((size_t)tilemap->chunk_count, sizeof(*tilemap->chunks));
    if (!tilemap->chunks) return;

    int index = 0;
    for (int cy = 0; cy < tilemap->current_height; cy += CHUNK_SIZE) {
        for (int cx = 0; cx < tilemap->current_width; cx += CHUNK_SIZE) {
            TilemapChunk *chunk = &tilemap->chunks[index++];
            chunk->x = cx;
            chunk->y = cy;
            chunk->width = (tilemap->current_width - cx < CHUNK_SIZE ?
                            tilemap->current_width - cx : CHUNK_SIZE) * tilemap->tilew;
            chunk->height = (tilemap->current_height - cy < CHUNK_SIZE ?
                             tilemap->current_height - cy : CHUNK_SIZE) * tilemap->tileh;

#if RENDER_BACKEND == RENDER_BACKEND_SOFTWARE
            Image image = GenImageColor(chunk->width, chunk->height, BLANK);
            if (!IsImageValid(image)) continue;
            for (int row = cy; row < cy + chunk->height / tilemap->tileh; ++row) {
                for (int col = cx; col < cx + chunk->width / tilemap->tilew; ++col) {
                    int tile_id = tilemap->current_map[row * tilemap->current_width + col];
                    if (tile_id <= 0 || tile_id >= tilemap->gindex_count) continue;
                    const Tile *tile = &tilemap->gindex[tile_id];
                    const Tileset *set = &tilemap->tilesets[tile->tileset_idx];
                    ImageDraw(&image, set->image,
                              (Rectangle){(float)tile->x, (float)tile->y,
                                          (float)set->tilew, (float)set->tileh},
                              (Rectangle){(float)((col - cx) * tilemap->tilew),
                                          (float)((row - cy) * tilemap->tileh),
                                          (float)set->tilew, (float)set->tileh}, WHITE);
                }
            }
            chunk->texture = LoadTextureFromImage(image);
            UnloadImage(image);
#else
            RenderTexture2D target = LoadRenderTexture(chunk->width, chunk->height);
            if (!IsRenderTextureValid(target)) continue;
            BeginTextureMode(target);
            ClearBackground(BLANK);
            for (int row = cy; row < cy + chunk->height / tilemap->tileh; ++row)
                for (int col = cx; col < cx + chunk->width / tilemap->tilew; ++col)
                    draw_tile_at(tilemap, tilemap->current_map[row * tilemap->current_width + col],
                                 (col - cx) * tilemap->tilew, (row - cy) * tilemap->tileh);
            EndTextureMode();
            chunk->target = target;
            chunk->texture = target.texture;
#endif
        }
    }
#else
    (void)tilemap;
#endif
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
#if RENDER_CHUNKS
    for (int i = 0; i < map->chunk_count; ++i) {
        const TilemapChunk *chunk = &map->chunks[i];
        if (!IsTextureValid(chunk->texture)) continue;
        Rectangle source = {0, 0, (float)chunk->texture.width, (float)chunk->texture.height};
#if RENDER_BACKEND == RENDER_BACKEND_GPU
        source.height = -source.height;
#endif
        DrawTexturePro(chunk->texture, source,
                       (Rectangle){(float)(chunk->x * map->tilew) - camera->x,
                                   (float)(chunk->y * map->tileh) - camera->y,
                                   (float)chunk->width, (float)chunk->height},
                       (Vector2){0}, 0, WHITE);
    }
#else
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
#endif
    for (int i = 0; i < count; ++i) {
        draw_character(&characters[i], characters[i].x - camera->x, characters[i].y - camera->y);
    }
#if DEBUG_VELOCITY
    for (int i = 0; i < count; ++i) {
        const Character *character = &characters[i];
        if (character->behavior_type != CHARACTER_PLAYER) continue;
        DrawRectangle(5, 5, 245, 52, Fade(BLACK, 0.75f));
        DrawText(TextFormat("PLAYER pos: %.1f, %.1f", character->x, character->y),
                 10, 10, 10, LIME);
        DrawText(TextFormat("prev: %.1f, %.1f  d/frame: %.1f, %.1f",
                            character->previous_x, character->previous_y,
                            character->frame_dx, character->frame_dy),
                 10, 25, 10, LIME);
        DrawText(TextFormat("velocity: vx %.1f  vy %.1f px/frame",
                            character->frame_dx, character->frame_dy),
                 10, 40, 10, LIME);
        break;
    }
#endif
    if (DEBUG_FPS) DrawText(TextFormat("FPS: %d", GetFPS()), DISP_W - 65, DISP_H - 18, 10, RED);
}

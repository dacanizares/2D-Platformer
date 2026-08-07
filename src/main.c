#include <stdio.h>
#include <stdlib.h>

#include "raylib.h"
#include "constants.h"
#include "game_render.h"
#include "game_scripts.h"
#include "game_sdl.h"
#include "sprites.h"
#include "tilemap_scripts.h"

int main(void) {
    /* Game starts! */
    if (!start(DISP_W, DISP_H)) {
        fprintf(stderr, "Could not initialize raylib.\n");
        return 1;
    }

    int result = 1;
    RenderTexture2D canvas = LoadRenderTexture(DISP_W, DISP_H);
    SetTextureFilter(canvas.texture, TEXTURE_FILTER_POINT);
    CharacterSprites player_sprites = {0};
    CharacterSprites computer_sprites = {0};
    Tilemap tilemap = {0};
    Character *characters = NULL;
    Character *player = NULL;
    int character_count = 0;
    Music music = {0};

    /* Map and sprites. */
    if (!IsRenderTextureValid(canvas) || !load_sprites(&player_sprites, true) ||
        !load_sprites(&computer_sprites, false) || !load_map(&tilemap, "maps/map1.json")) {
        fprintf(stderr, "Could not load the game graphics or map. Run from the project root.\n");
        goto cleanup;
    }
    process_tilemap(&tilemap);
    if (!spawn_characters(&tilemap, &player_sprites, &computer_sprites,
                          &characters, &character_count, &player)) {
        fprintf(stderr, "Could not spawn a player.\n");
        goto cleanup;
    }

    /* Music. */
    if (IsAudioDeviceReady()) {
        music = LoadMusicStream("sound/hyperfun.mp3");
        if (IsMusicValid(music)) {
            music.looping = true;
            PlayMusicStream(music);
        }
    }
    GameCamera camera = {0, 0, CAMERA_OFFSET_X, CAMERA_OFFSET_Y, false};
    start_characters(characters, character_count);

    /* Game loop. */
    while (!WindowShouldClose()) {
        if (IsMusicValid(music)) UpdateMusicStream(music);
        InputState input = get_events();
        update_characters(characters, character_count, &input, &tilemap);
        update_camera(&camera, player);
        clear(canvas);
        render(&camera, characters, character_count, &tilemap);
        update(canvas);
    }
    result = 0;

cleanup:
    if (IsMusicValid(music)) UnloadMusicStream(music);
    free(characters);
    unload_map(&tilemap);
    unload_sprites(&computer_sprites);
    unload_sprites(&player_sprites);
    if (IsRenderTextureValid(canvas)) UnloadRenderTexture(canvas);
    quit_game();
    return result;
}

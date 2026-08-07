#include "game_sdl.h"
#include "constants.h"

bool start(int width, int height) {
    SetConfigFlags(FLAG_WINDOW_RESIZABLE | FLAG_VSYNC_HINT);
    InitWindow(width * 2, height * 2, "2D Platformer - C + raylib");
    if (!IsWindowReady()) return false;
    InitAudioDevice();
    SetTargetFPS(FPS);
    return true;
}

void quit_game(void) {
    if (IsAudioDeviceReady()) CloseAudioDevice();
    CloseWindow();
}

InputState get_events(void) {
    return (InputState){
        .right = IsKeyDown(KEY_RIGHT),
        .left = IsKeyDown(KEY_LEFT),
        .up = IsKeyDown(KEY_UP),
        .down = IsKeyDown(KEY_DOWN),
        .jump = IsKeyDown(KEY_LEFT_CONTROL) || IsKeyDown(KEY_RIGHT_CONTROL),
        .stop = IsKeyDown(KEY_SPACE)
    };
}

void clear(RenderTexture2D target) {
    BeginTextureMode(target);
    ClearBackground(BLACK);
}

void update(RenderTexture2D target) {
    EndTextureMode();
    BeginDrawing();
    ClearBackground(BLACK);
    Rectangle src = {0, 0, (float)target.texture.width, -(float)target.texture.height};
    Rectangle dst = {0, 0, (float)GetScreenWidth(), (float)GetScreenHeight()};
    DrawTexturePro(target.texture, src, dst, (Vector2){0}, 0, WHITE);
    EndDrawing();
}

void draw_tile(const Tileset *tileset, const Tile *tile, float x, float y) {
    Rectangle source = {(float)tile->x, (float)tile->y, (float)tileset->tilew, (float)tileset->tileh};
    DrawTextureRec(tileset->sheet, source, (Vector2){x, y}, WHITE);
}

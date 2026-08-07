#include "sprites.h"

static void get_walk_rects(bool player, Rectangle frames[2]) {
    /* Walk animation frames for the player or computer character. */
    if (player) {
        frames[0] = (Rectangle){112, 2, 26, 40};
        frames[1] = (Rectangle){4, 4, 30, 38};
    } else {
        frames[0] = (Rectangle){276, 128, 30, 40};
        frames[1] = (Rectangle){308, 128, 32, 40};
    }
}

static void get_jump_rects(bool player, Rectangle frames[2]) {
    /* Jump animation frames for the player or computer character. */
    if (player) {
        frames[0] = (Rectangle){4, 4, 30, 38};
        frames[1] = (Rectangle){38, 4, 30, 36};
    } else {
        frames[0] = (Rectangle){308, 128, 32, 40};
        frames[1] = (Rectangle){344, 128, 30, 40};
    }
}

static void get_idle_rects(bool player, Rectangle frames[2]) {
    /* Idle animation frames for the player or computer character. */
    if (player) {
        frames[0] = (Rectangle){76, 2, 26, 40};
        frames[1] = (Rectangle){112, 2, 24, 40};
    } else {
        frames[0] = (Rectangle){548, 128, 30, 40};
        frames[1] = (Rectangle){583, 128, 30, 40};
    }
}

bool load_sprites(CharacterSprites *sprites, bool player) {
    Image image = LoadImage("graphics/arc2.png");
    if (!IsImageValid(image)) return false;
    ImageFormat(&image, PIXELFORMAT_UNCOMPRESSED_R8G8B8A8);
    ImageColorReplace(&image, BLACK, BLANK);
    sprites->sheet = LoadTextureFromImage(image);
    UnloadImage(image);
    if (!IsTextureValid(sprites->sheet)) return false;

    get_idle_rects(player, sprites->frames[CHARACTER_IDLE]);
    get_walk_rects(player, sprites->frames[CHARACTER_WALK]);
    get_jump_rects(player, sprites->frames[CHARACTER_JUMP]);
    sprites->frames[CHARACTER_SLEEP][0] = sprites->frames[CHARACTER_IDLE][0];
    sprites->frames[CHARACTER_SLEEP][1] = sprites->frames[CHARACTER_IDLE][1];
    return true;
}

void unload_sprites(CharacterSprites *sprites) {
    if (IsTextureValid(sprites->sheet)) UnloadTexture(sprites->sheet);
    sprites->sheet = (Texture2D){0};
}

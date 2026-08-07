#include "characters.h"

static void on_land(Character *character) {
    character->land = true;
    character->vy = 0;
}

static void on_peak(Character *character) {
    if (character->vy < 0) character->vy = 0;
}

static void on_air(Character *character) {
    character->land = false;
    character->vy += GRAVITY;
    if (character->vy > MAX_VY) character->vy = MAX_VY;
}

static void on_left(Character *character) {
    (void)character;
}

static void on_right(Character *character) {
    (void)character;
}

static void on_start(Character *character) {
    (void)character;
}

static void on_left_move(Character *character) {
    character->direction = true;
    character->right = true;
    character->left = false;
}

static void on_right_move(Character *character) {
    character->direction = false;
    character->right = false;
    character->left = true;
}

static void on_start_move(Character *character) {
    character->direction = true;
    character->right = true;
}

static void on_start_jump(Character *character) {
    on_start_move(character);
    character->jump = true;
}

static void on_collide(Character *character, bool top) {
    if (top) character->has_coll_enemy = true;
    else character->sleep = CHARACTER_SLEEP_FRAMES;
}

void update_character(Character *character, const InputState *input) {
    (void)input;
    if (character->stop) return;
    /* Sleep. */
    if (character->sleep > 0) {
        --character->sleep;
    } else {
        /* Movement. */
        if (character->right) character->x += VEL_X;
        else if (character->left) character->x -= VEL_X;
        if (character->has_coll_enemy) {
            character->vy = -VY_COLLIDE;
            character->has_coll_enemy = false;
        } else if (character->land && character->jump) {
            character->vy = -VEL_Y;
            character->land = false;
        }
    }
    /* pygame.Rect and the original Python code both worked on truncated pixels. */
    character->y = (float)(int)(character->y + character->vy);
}

void update_player(Character *player, const InputState *input) {
    if (input->right && !player->right) player->direction = true;
    if (input->left && !player->left) player->direction = false;
    player->right = input->right;
    player->left = input->left;
    player->jump = input->jump;
    player->stop = input->stop;
    update_character(player, input);
}

const CharacterBehavior character_behaviors[3] = {
    {update_player, on_land, on_peak, on_air, on_left, on_right, on_start, on_collide},
    {update_character, on_land, on_peak, on_air, on_left_move, on_right_move, on_start_jump, on_collide},
    {update_character, on_land, on_peak, on_air, on_left_move, on_right_move, on_start_move, on_collide}
};

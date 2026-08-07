#ifndef PLATFORMER_GAME_STRUCTS_H
#define PLATFORMER_GAME_STRUCTS_H

#include <stdbool.h>
#include "raylib.h"
#include "constants.h"

typedef struct GameCamera {
    float x;
    float y;
    float offset_x;
    float offset_y;
    bool always_centered;
} GameCamera;

/* Character behavior types. */
typedef enum CharacterBehaviorType {
    CHARACTER_PLAYER = 0,
    CHARACTER_JUMPING_AI,
    CHARACTER_BASIC_AI
} CharacterBehaviorType;

/* Character animation states. */
typedef enum CharacterAnimState {
    CHARACTER_IDLE = 0,
    CHARACTER_WALK,
    CHARACTER_JUMP,
    CHARACTER_SLEEP,
    CHARACTER_ANIM_COUNT
} CharacterAnimState;

typedef struct CharacterSprites {
    Texture2D sheet;
    Rectangle frames[CHARACTER_ANIM_COUNT][2];
} CharacterSprites;

typedef struct CharacterAnim {
    CharacterSprites *sprites;
    CharacterAnimState state;
    int frame;
    int next_update;
} CharacterAnim;

typedef struct Character {
    float x;
    float y;
    float w;
    float h;
    CharacterAnim anim;
    CharacterBehaviorType behavior_type;
    /* Default state. */
    Rectangle collider;
    int coll_dy;
    int sleep;
    bool has_coll_enemy;
    float vy;
    bool direction;
    bool land;
    bool right;
    bool left;
    bool jump;
    bool stop;
} Character;

typedef struct InputState {
    bool right;
    bool left;
    bool jump;
    bool stop;
} InputState;

typedef struct CharacterBehavior {
    /* Events. */
    void (*update)(Character *, const InputState *);
    void (*on_land)(Character *);
    void (*on_peak)(Character *);
    void (*on_air)(Character *);
    void (*on_left)(Character *);
    void (*on_right)(Character *);
    void (*on_start)(Character *);
    void (*on_collide)(Character *, bool);
} CharacterBehavior;

#endif

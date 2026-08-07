#ifndef PLATFORMER_CONSTANTS_H
#define PLATFORMER_CONSTANTS_H

/* Graphics. */
#define DISP_W 600
#define DISP_H 400
#define FPS 60

/* Debug and rendering options. */
#ifndef RENDER_CHUNKS
#define RENDER_CHUNKS 1
#endif
#define RENDER_BACKEND_GPU 0
#define RENDER_BACKEND_SOFTWARE 1
#ifndef RENDER_BACKEND
#define RENDER_BACKEND RENDER_BACKEND_SOFTWARE
#endif
#define DEBUG_DRAW 0
#define DEBUG_COLL_BOT 0
#define DEBUG_CHUNKS 0
#define DEBUG_FPS 0

/* Camera. */
#define CAMERA_OFFSET_X 0.40f
#define CAMERA_OFFSET_Y 0.35f

/* Characters. */
#define CHARACTER_COLL_W 20
#define CHARACTER_COLL_H 40
#define ANIM_EVERY_X_FRAMES 6
#define IDLE_ANIM_X_FRAMES 120
#define CHARACTER_SLEEP_FRAMES 60
#define VY_COLLIDE 10.0f
#define MAX_VY 13.0f
#define VEL_X 3.0f
#define VEL_Y 12.0f
#define GRAVITY 0.6f

/* Static collisions. */
#define MAX_DIST_COL 500
#define CHUNK_SIZE 8

#endif

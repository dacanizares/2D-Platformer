#include "tilemap_scripts.h"

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *skip_space(const char *p, const char *end) {
    while (p < end && isspace((unsigned char)*p)) ++p;
    return p;
}

static const char *find_key(const char *begin, const char *end, const char *key) {
    char needle[96];
    snprintf(needle, sizeof(needle), "\"%s\"", key);
    const char *p = begin;
    while ((p = strstr(p, needle)) != NULL && p < end) {
        p += strlen(needle);
        p = skip_space(p, end);
        if (p < end && *p == ':') return skip_space(p + 1, end);
    }
    return NULL;
}

static const char *match_scope(const char *open, const char *end) {
    if (!open || open >= end || (*open != '{' && *open != '[')) return NULL;
    const char close = *open == '{' ? '}' : ']';
    int depth = 0;
    bool in_string = false;
    bool escaped = false;
    for (const char *p = open; p < end; ++p) {
        if (in_string) {
            if (escaped) escaped = false;
            else if (*p == '\\') escaped = true;
            else if (*p == '"') in_string = false;
            continue;
        }
        if (*p == '"') in_string = true;
        else if (*p == *open) ++depth;
        else if (*p == close && --depth == 0) return p;
    }
    return NULL;
}

static int read_int(const char *begin, const char *end, const char *key, int fallback) {
    const char *p = find_key(begin, end, key);
    return p ? (int)strtol(p, NULL, 10) : fallback;
}

static bool read_string(const char *begin, const char *end, const char *key, char *out, size_t cap) {
    const char *p = find_key(begin, end, key);
    if (!p || p >= end || *p != '"' || cap == 0) return false;
    ++p;
    size_t n = 0;
    while (p < end && *p != '"') {
        char c = *p++;
        if (c == '\\' && p < end) {
            char escaped = *p++;
            c = escaped == 'n' ? '\n' : escaped == 't' ? '\t' : escaped;
        }
        if (n + 1 < cap) out[n++] = c;
    }
    out[n] = '\0';
    return true;
}

static Color read_color(const char *text) {
    unsigned int rgb = 0;
    if (text && text[0] == '#') (void)sscanf(text + 1, "%x", &rgb);
    return (Color){(unsigned char)(rgb >> 16), (unsigned char)(rgb >> 8), (unsigned char)rgb, 255};
}

static int count_objects(const char *array, const char *array_end) {
    int count = 0;
    const char *p = array + 1;
    while (p < array_end) {
        p = skip_space(p, array_end);
        if (*p == ',') { ++p; continue; }
        if (*p != '{') break;
        const char *close = match_scope(p, array_end + 1);
        if (!close) break;
        ++count;
        p = close + 1;
    }
    return count;
}

static bool build_asset_path(const char *map_path, const char *image, char *out, size_t cap) {
    const char *slash = strrchr(map_path, '/');
    if (!slash) return snprintf(out, cap, "%s", image) > 0;
    int directory_len = (int)(slash - map_path);
    return snprintf(out, cap, "%.*s/%s", directory_len, map_path, image) > 0;
}

static void parse_tile_properties(Tilemap *map, const char *tiles_begin, const char *tiles_end, int firstgid) {
    /* Read collision metadata attached to each tile. */
    const char *p = tiles_begin + 1;
    while (p < tiles_end) {
        p = skip_space(p, tiles_end);
        if (*p == ',') { ++p; continue; }
        if (*p != '{') break;
        const char *tile_end = match_scope(p, tiles_end + 1);
        if (!tile_end) break;
        int gid = firstgid + read_int(p, tile_end, "id", 0);
        const char *props = find_key(p, tile_end, "properties");
        if (props && *props == '[' && gid >= 0 && gid < map->gindex_count) {
            const char *props_end = match_scope(props, tile_end + 1);
            const char *q = props + 1;
            while (props_end && q < props_end) {
                q = skip_space(q, props_end);
                if (*q == ',') { ++q; continue; }
                if (*q != '{') break;
                const char *prop_end = match_scope(q, props_end + 1);
                if (!prop_end) break;
                char name[32] = {0};
                char value[32] = {0};
                read_string(q, prop_end, "name", name, sizeof(name));
                read_string(q, prop_end, "value", value, sizeof(value));
                if (strcmp(name, "NoCollide") == 0 && strcmp(value, "1") == 0) map->no_collision[gid] = true;
                else if (strcmp(name, "NoPeak") == 0 && strcmp(value, "1") == 0) map->no_peak[gid] = true;
                else if (strcmp(name, "CollDy") == 0) map->coll_dy[gid] = atoi(value);
                q = prop_end + 1;
            }
        }
        p = tile_end + 1;
    }
}

static bool load_tilesets(Tilemap *map, const char *json, const char *end, const char *map_path) {
    const char *array = find_key(json, end, "tilesets");
    const char *array_end = match_scope(array, end);
    if (!array || !array_end) return false;
    map->tileset_count = count_objects(array, array_end);
    map->tilesets = calloc((size_t)map->tileset_count, sizeof(*map->tilesets));
    if (!map->tilesets) return false;

    int max_gid = 1;
    const char *p = array + 1;
    for (int i = 0; i < map->tileset_count; ++i) {
        p = skip_space(p, array_end);
        if (*p == ',') p = skip_space(p + 1, array_end);
        const char *object_end = match_scope(p, array_end + 1);
        if (!object_end) return false;
        Tileset *set = &map->tilesets[i];
        char image[256] = {0};
        char alpha[16] = {0};
        set->firstgid = read_int(p, object_end, "firstgid", 1);
        set->w = read_int(p, object_end, "imagewidth", 0);
        set->h = read_int(p, object_end, "imageheight", 0);
        set->tilew = read_int(p, object_end, "tilewidth", map->tilew);
        set->tileh = read_int(p, object_end, "tileheight", map->tileh);
        set->margin = read_int(p, object_end, "margin", 0);
        set->spacing = read_int(p, object_end, "spacing", 0);
        read_string(p, object_end, "image", image, sizeof(image));
        read_string(p, object_end, "transparentcolor", alpha, sizeof(alpha));
        set->alpha_color = read_color(alpha);
        build_asset_path(map_path, image, set->path, sizeof(set->path));
        int columns = set->w / (set->tilew + set->spacing);
        int rows = set->h / (set->tileh + set->spacing);
        int after = set->firstgid + columns * rows;
        if (after > max_gid) max_gid = after;
        p = object_end + 1;
    }

    map->gindex_count = max_gid;
    map->gindex = calloc((size_t)max_gid, sizeof(*map->gindex));
    map->no_collision = calloc((size_t)max_gid, sizeof(*map->no_collision));
    map->no_peak = calloc((size_t)max_gid, sizeof(*map->no_peak));
    map->coll_dy = calloc((size_t)max_gid, sizeof(*map->coll_dy));
    if (!map->gindex || !map->no_collision || !map->no_peak || !map->coll_dy) return false;
    map->no_collision[0] = true;

    /* Index tileset image coordinates by global tile ID. */
    p = array + 1;
    for (int i = 0; i < map->tileset_count; ++i) {
        p = skip_space(p, array_end);
        if (*p == ',') p = skip_space(p + 1, array_end);
        const char *object_end = match_scope(p, array_end + 1);
        Tileset *set = &map->tilesets[i];
        int gid = set->firstgid;
        for (int y = set->margin; y + set->tileh <= set->h; y += set->tileh + set->spacing) {
            for (int x = set->margin; x + set->tilew <= set->w; x += set->tilew + set->spacing) {
                if (gid < max_gid) map->gindex[gid] = (Tile){x, y, i};
                ++gid;
            }
        }
        const char *tiles = find_key(p, object_end, "tiles");
        if (tiles && *tiles == '[') {
            const char *tiles_end = match_scope(tiles, object_end + 1);
            if (tiles_end) parse_tile_properties(map, tiles, tiles_end, set->firstgid);
        }
        Image image = LoadImage(set->path);
        if (!IsImageValid(image)) return false;
        ImageFormat(&image, PIXELFORMAT_UNCOMPRESSED_R8G8B8A8);
        ImageColorReplace(&image, set->alpha_color, BLANK);
        set->sheet = LoadTextureFromImage(image);
        UnloadImage(image);
        if (!IsTextureValid(set->sheet)) return false;
        p = object_end + 1;
    }
    return true;
}

static bool load_layers(Tilemap *map, const char *json, const char *end) {
    const char *layers = find_key(json, end, "layers");
    const char *layers_end = match_scope(layers, end);
    if (!layers || !layers_end) return false;
    /* Load the map itself: terrain data first, then character spawns. */
    const char *terrain = skip_space(layers + 1, layers_end);
    const char *terrain_end = match_scope(terrain, layers_end + 1);
    if (!terrain_end) return false;
    const char *data = find_key(terrain, terrain_end, "data");
    const char *data_end = match_scope(data, terrain_end + 1);
    int tile_count = map->current_width * map->current_height;
    map->current_map = calloc((size_t)tile_count, sizeof(*map->current_map));
    if (!data || !data_end || !map->current_map) return false;
    const char *value = data + 1;
    for (int i = 0; i < tile_count; ++i) {
        value = skip_space(value, data_end);
        map->current_map[i] = (int)strtol(value, (char **)&value, 10);
        value = skip_space(value, data_end);
        if (*value == ',') ++value;
    }

    const char *characters = skip_space(terrain_end + 1, layers_end);
    if (*characters == ',') characters = skip_space(characters + 1, layers_end);
    const char *characters_end = match_scope(characters, layers_end + 1);
    const char *objects = find_key(characters, characters_end, "objects");
    const char *objects_end = match_scope(objects, characters_end + 1);
    if (!characters_end || !objects || !objects_end) return false;
    map->spawn_count = count_objects(objects, objects_end);
    map->characters_to_spawn = calloc((size_t)map->spawn_count, sizeof(*map->characters_to_spawn));
    if (!map->characters_to_spawn) return false;
    const char *p = objects + 1;
    for (int i = 0; i < map->spawn_count; ++i) {
        p = skip_space(p, objects_end);
        if (*p == ',') p = skip_space(p + 1, objects_end);
        const char *object_end = match_scope(p, objects_end + 1);
        char type[32] = {0};
        read_string(p, object_end, "type", type, sizeof(type));
        TilemapCharacter *spawn = &map->characters_to_spawn[i];
        spawn->x = read_int(p, object_end, "x", 0);
        spawn->y = read_int(p, object_end, "y", 0);
        if (strcmp(type, "Player") == 0) spawn->behavior_type = CHARACTER_PLAYER;
        else if (strcmp(type, "JumpingAI") == 0) spawn->behavior_type = CHARACTER_JUMPING_AI;
        else spawn->behavior_type = CHARACTER_BASIC_AI;
        p = object_end + 1;
    }
    return true;
}

bool load_map(Tilemap *map, const char *path) {
    *map = (Tilemap){0};
    char *json = LoadFileText(path);
    if (!json) return false;
    const char *end = json + strlen(json);
    map->current_height = read_int(json, end, "height", 0);
    map->current_width = read_int(json, end, "width", 0);
    map->tilew = read_int(json, end, "tilewidth", 0);
    map->tileh = read_int(json, end, "tileheight", 0);
    bool ok = map->current_width > 0 && map->current_height > 0 &&
              load_tilesets(map, json, end, path) && load_layers(map, json, end);
    UnloadFileText(json);
    if (!ok) unload_map(map);
    return ok;
}

void unload_map(Tilemap *map) {
    if (map->tilesets) {
        for (int i = 0; i < map->tileset_count; ++i) {
            if (IsTextureValid(map->tilesets[i].sheet)) UnloadTexture(map->tilesets[i].sheet);
        }
    }
    free(map->gindex);
    free(map->tilesets);
    free(map->current_map);
    free(map->characters_to_spawn);
    free(map->no_collision);
    free(map->no_peak);
    free(map->coll_dy);
    *map = (Tilemap){0};
}

int get_coll_dy(const Tilemap *map, int tile_id) {
    return tile_id >= 0 && tile_id < map->gindex_count ? map->coll_dy[tile_id] : 0;
}

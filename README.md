# 2D-Platformer

A simple 2D platformer written in C17 with raylib.

![2d platformer pygame](.docs/screenshot-2.png)

## Highlights

* Data-oriented character behaviors in `src/characters.c`.

* Raylib rendering at a 600x400 logical resolution with pixel-perfect window scaling.

  ![2d platformer pygame chunks debug tools](.docs/screenshot-3.png)

* Custom [Tiled](https://www.mapeditor.org/) JSON support, including character spawning and collision metadata.

* Also includes:

    * Static tile collisions and dynamic character collisions.
    * Offset-based side-scrolling camera.
    * State-driven character sprite animations.

## Build

Requires a C17 compiler, `pkg-config`, and raylib.

```bash
./run/dev.sh       # compila y ejecuta bin/dbg-linux/platformer
./run/build.sh     # bin/rel-linux/platformer
```

Run either executable from the project root so it can find `maps/`, `graphics/`, and `sound/`.

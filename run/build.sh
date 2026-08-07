#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"
mkdir -p bin/rel-linux

mapfile -t sources < <(find src -type f -name '*.c' -print | sort)
read -r -a raylib_flags <<< "$(pkg-config --cflags --libs raylib)"
raylib_libdir="$(pkg-config --variable=libdir raylib)"

gcc -std=c17 -pedantic -Wall -Wextra -Wshadow -Wconversion \
    -O2 -DNDEBUG -Isrc "${sources[@]}" -o bin/rel-linux/platformer \
    "${raylib_flags[@]}" -Wl,-rpath,"$raylib_libdir" -lm -pthread

strip bin/rel-linux/platformer
echo "Built bin/rel-linux/platformer"

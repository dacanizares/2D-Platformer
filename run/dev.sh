#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"
mkdir -p bin/dbg-linux

mapfile -t sources < <(find src -type f -name '*.c' -print | sort)
read -r -a raylib_flags <<< "$(pkg-config --cflags --libs raylib)"
raylib_libdir="$(pkg-config --variable=libdir raylib)"

gcc -std=c17 -pedantic -Wall -Wextra -Wshadow -Wconversion \
    -g3 -O0 -Isrc "${sources[@]}" -o bin/dbg-linux/platformer \
    "${raylib_flags[@]}" -Wl,-rpath,"$raylib_libdir" -lm -pthread

echo "Built bin/dbg-linux/platformer"
if [[ "${1:-}" == "--build-only" ]]; then
    exit 0
fi
exec bin/dbg-linux/platformer

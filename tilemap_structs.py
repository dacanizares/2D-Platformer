import pygame
from dataclasses import dataclass

@dataclass
class Tilemap:
    gindex = {}
    tilesets = []
    current_map: list = None
    current_width: int = 0
    current_height: int = 0
    tilew: int = 0
    tileh: int = 0
    no_collision = { 0: True }
    no_peak = { 0: True }

@dataclass
class Tile:
    x: int
    y: int
    tileset_idx: int

@dataclass
class Tileset:
    path: str
    w: int
    h: int
    tilew: int
    tileh: int
    margin: int
    spacing: int
    firstgid: str
    alpha_color: tuple
    sheet: pygame.Surface

from pygame import Surface
from dataclasses import dataclass

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
    sheet: Surface

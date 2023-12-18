import game
import pygame
from pygame.locals import *
from dataclasses import dataclass

@dataclass
class Tile:
    x: int
    y: int
    tileset_idx: int

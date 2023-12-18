import pygame
from dataclasses import dataclass

@dataclass
class Camera:
    x: int
    y: int
    offset: float = 0.25
    always_centered: bool = False


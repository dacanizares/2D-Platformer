import pygame
from typing import Callable
from dataclasses import dataclass
from enum import Enum

@dataclass
class Camera:
    x: int
    y: int
    offset_x: float = 0.3
    offset_y: float = 0.35
    always_centered: bool = False

class CharacterBehaviors(Enum):
    PLAYER = 0
    JUMPING_AI = 1
    BASIC_AI = 2

@dataclass
class Character:
    x: float
    y: float

    collider: pygame.Rect

    # Actions
    idle: list[pygame.Surface]
    walking: list[pygame.Surface]
    jumping: list[pygame.Surface]

    behavior_type: CharacterBehaviors

    # Default state
    vy: float = 0
    frame: float = 0
    direction: bool = True
    land: bool = False
    right: bool = False
    left: bool = False
    jump: bool  = False
    delta_frames: bool = 0
    stop: bool = False


@dataclass
class CharacterBehavior:
    # Events
    update: Callable[[Character, dict], None]
    on_land: Callable[[Character], None]
    on_peak: Callable[[Character], None]
    on_air: Callable[[Character], None]
    on_left: Callable[[Character], None]
    on_right: Callable[[Character], None]
    on_start: Callable[[Character], None]

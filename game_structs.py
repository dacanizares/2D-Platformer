from typing import Callable
import pygame
from dataclasses import dataclass

@dataclass
class Camera:
    x: int
    y: int
    offset: float = 0.25
    always_centered: bool = False



@dataclass
class Character:
    x: float
    y: float

    collider: pygame.Rect

    # Actions
    idle: list[pygame.Surface]
    walking: list[pygame.Surface]
    jumping: list[pygame.Surface]

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

@dataclass
class CharacterConfig:
    character: Character
    behavior: CharacterBehavior

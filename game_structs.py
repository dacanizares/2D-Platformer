import pygame
from typing import Callable
from dataclasses import dataclass
from enum import Enum
from constants import *

@dataclass
class Camera:
    x: int
    y: int
    offset_x: float = OFFSET_X
    offset_y: float = OFFSET_Y
    always_centered: bool = False

class CharacterBehaviors(Enum):
    PLAYER = 0
    JUMPING_AI = 1
    BASIC_AI = 2

class CharacterAnims(Enum):
    IDLE = 0
    WALK = 1
    JUMP = 2
    SLEEP = 3

@dataclass
class CharacterAnim:
    sets: dict[CharacterAnims, list[list[pygame.Surface]]]
    state: CharacterAnims = CharacterAnims.IDLE
    frame: int = 0
    next_update: int = 0
    last_update: bool = 0

@dataclass
class Character:
    x: int
    y: int
    w: int
    h: int
    w: int   

    anim: CharacterAnim
    behavior_type: CharacterBehaviors

    # Default state
    collider: pygame.Rect = None
    coll_dy: int = 0
    sleep: int = 0
    has_coll_enemy: bool = False
    vy: float = 0
    
    direction: bool = True
    land: bool = False
    right: bool = False
    left: bool = False
    jump: bool  = False    
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
    on_collide: Callable[[Character, bool], None]

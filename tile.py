import game
import pygame
from pygame.locals import *

class Tile:
    def __init__(self, x, y, resources, fps=1):        
        self.x = x
        self.y = y
        self.frame = 0
        self.deltaframe = 0
        self.fps = 1
        self.tile = resources

    def draw(self, xcam, ycam):
        self.deltaframe = (self.deltaframe + 1) % self.fps
        if self.deltaframe == 0:        
            self.frame = (self.frame + 1) % len(self.tile)
        game.draw(self.tile[self.frame], (xcam, ycam))
        
    

    

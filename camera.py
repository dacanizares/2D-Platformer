import game
import pygame
from pygame.locals import *
from constants import *

class Camera:
    def __init__(self, x, y, player, tilemap):        
        self.x = x
        self.y = y
        self.player = player
        self.tilemap = tilemap

    def update(self):
        self.x = self.player.x - DISP_W / 2
        self.y = self.player.y - DISP_H * 3 / 4        

    def draw(self):
        self.tilemap.draw(self.x, self.y, DISP_W, DISP_H)
        self.player.draw(self.player.x - self.x, self.player.y - self.y)        

        if S_COLLIDER:
            col = self.player.static_col
            rect = pygame.Rect(0,0,3,3)            
    

    

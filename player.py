import game
import pygame
from pygame.locals import *
from constants import *

class Player:
    def __init__(self, x, y, static_col, resources):        
        self.x = x
        self.y = y
        self.vy = 0
        self.frame = 0
        self.direction = True
        self.land = False
        self.right = False
        self.left = False
        self.jump  = False
        self.delta_frames = 0

        # Colisiones estaticas
        self.last_x = x
        self.last_y = y
        self.static_col = static_col
        
        self.walking = resources[0]
        self.idle = resources[1]
        self.jumping = resources[2]

    def update_events(self, events):
        if K_RIGHT in events:
            if not self.right:
                self.direction = True
                self.frame = 0
            self.right = events[K_RIGHT]
            
        if K_LEFT in events:
            if not self.left:
                self.direction = False
                self.frame = 0
            self.left = events[K_LEFT]
            
        if K_UP in events:
            self.jump = events[K_UP]
            self.frame = 0

    def update(self):        
        # X movement
        if self.right:
            self.x += VEL_X            
        if self.left:
            self.x -= VEL_X           
                           
        # Y movement
        if self.land:
            vy = 0
        if self.land and self.jump:
            self.vy = -VEL_y
            self.land = False
            
        if not self.land:
            self.vy = min(self.vy + GRAVITY, MAX_VY)
            self.y += self.vy
            
        if DEBUG:
            game.debug_txt('XY: '+str(self.x)+','+str(self.y), (100,0), RED)
        


    def draw(self, xcam, ycam):
        if self.direction:
            anim_index = 0
        else:
            anim_index = 1
            
        if not self.land:
            if self.vy < 0:
                sprite = self.jumping[anim_index][1]
            else:
                sprite = self.jumping[anim_index][0]
        else:
            if self.right or self.left:
                sprite = self.walking[anim_index][self.frame]
                self.frame = (self.frame + 1) % len(self.walking[anim_index])                
            else:
                self.delta_frames = (self.delta_frames + 1) % 120                
                if self.delta_frames < 90:
                    sprite = self.idle[anim_index][0]
                else:
                    sprite = self.idle[anim_index][1]
        # Center image
        xoffset = -sprite.get_width()/2
        yoffset = -sprite.get_height()
        game.draw(sprite, (xcam + xoffset, ycam + yoffset))
        if S_COLLIDER:
            game.draw_rect(pygame.Rect(xcam - self.static_col.w/2, ycam - self.static_col.h, self.static_col.w, self.static_col.h))
    
    

    

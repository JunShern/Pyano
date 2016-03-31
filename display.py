import pygame
from pygame import gfxdraw
from helpers import *


class Display(object):
    def __init__(self):
        self.screen = None

    def setup(self, fullscreen):
        pygame.init()

        ## Dimensions
        infoObject = pygame.display.Info()
        pygame.display.set_caption("Pyano")
        self.img = pygame.image.load("LogoResized.png")
        self.width = int(infoObject.current_w)
        self.height = int(infoObject.current_h) 

        ## Screen setup
        if (fullscreen==1):
            self.screen = pygame.display.set_mode((self.width,self.height), pygame.FULLSCREEN) #pygame.RESIZABLE
        else:
            self.screen = pygame.display.set_mode((self.width,self.height), pygame.RESIZABLE)
        pygame.mouse.set_visible(False) # Hide cursor

        ## Color scheme
        #colours_ = [(242,151,84),(221,221,221),(128,206,185)]
        self.colour = (65,170,196) # This does not change, this is a reference for colour_ 
        self.colour_ = self.colour
        self.circle_w = 8
        self.circle_w_ = 8
        self.circle_r = 230
        self.circle_r_ = 230
        self.bg_color = pygame.Color(5,5,5)
        self.in_color = pygame.Color(15,15,15)
        self.walk_count = 1
        self.rad_step = [1]

        ## Font
        self.pFont = pygame.font.SysFont("monospace", int(self.width/(self.width/17)), True)

        # Display
        self.screen.fill(self.bg_color)
        pygame.draw.circle(self.screen, self.in_color, (self.width/2,self.height/2), self.circle_r, 0)

    def close(self):
        pygame.display.quit()
        #pygame.quit() # Do this in main.py, after closing MIDI

    def update(self):
        pygame.display.update()

    def fillBackground(self):
        self.screen.fill(self.bg_color)

    def drawCircle(self):
        pygame.draw.circle(self.screen, (24,24,24), (self.width/2,self.height/2), self.circle_r_, 0)
        pygame.gfxdraw.filled_circle(self.screen, self.width/2, self.height/2, self.circle_r_, self.colour_)
        pygame.gfxdraw.filled_circle(self.screen, self.width/2, self.height/2, self.circle_r_-self.circle_w, self.in_color)
        pygame.gfxdraw.aacircle(self.screen, self.width/2, self.height/2, self.circle_r_-self.circle_w, self.colour_)
        pygame.gfxdraw.aacircle(self.screen, self.width/2, self.height/2, self.circle_r_, self.colour_)

    def drawLogo(self):
        self.screen.blit(self.img, (self.width/2-self.img.get_rect().size[0]/2,self.height/2-self.img.get_rect().size[1]/2))

    def drawMemory(self, inst_mem, base_mem, vol_mem, vel_mem):
        # Transparent surface
        s = pygame.Surface((self.width,self.height))
        s.set_alpha(150)
        s.fill(self.bg_color)
        self.screen.blit(s, (0,0))
        # Text colour
        c = pygame.Color(255,255,255)
        # Text
        info = "Default Slot : INST %03d | BASE %3s | VOL %03d | VEL %03d" %\
            (4, strNote(36), 70, 70)
        w, h = self.pFont.size(info)
        text = self.pFont.render(info, 1, (255,255,255))
        self.screen.blit(text, (self.width/2-w/2, 200))
        for num in range(1,10):
            info = "Memory Slot %i: INST %03d | BASE %3s | VOL %03d | VEL %03d" %\
                (num, inst_mem[num-1], strNote(base_mem[num-1]), vol_mem[num-1], vel_mem[num-1])
            w, h = self.pFont.size(info)
            text = self.pFont.render(info, 1, c)
            self.screen.blit(text, (self.width/2-w/2, 200 + num*(self.height-400)/9))

    def drawStatus(self, info, kbCount):
        w, h = self.pFont.size(info)
        text = self.pFont.render(info, 1, (255,255,255))
        self.screen.blit(text, (self.width/2-w/2, (self.height/2+self.circle_r) + 20 + kbCount*(h+10) ))

    def pulseCircle(self):
        self.colour_ = colourWalk(self.colour_, self.colour, 80)
    	self.walk_count = 1 - self.walk_count
    	if self.walk_count == 1:
            self.circle_r_ = smootherWalk(self.circle_r_, self.circle_r-2, self.circle_r+8, self.rad_step)

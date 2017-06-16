import pygame
from pygame.locals import *
import math
import random

WHITE = (255, 255, 255)

#Wall class.  Simulates static obstacles
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        #Call parent constructor
        super(Wall, self).__init__()

        #Create surface sprite will be drawn onto
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        # this rect determinies the position the wall is drawn
        self.rect = self.image.get_rect()
        # Draw the rectangle onto the surface
        pygame.draw.rect(self.image, (0,0,255), [0,0,width,height], 1)
        self.rect.center = [x,y]
        self.width=width
        self.height=height

        print "Wall initialized at "+str(x)+", "+str(y)

    def calc_forces(self, robots):
        for r in robots:
            dx = max(abs(r.get_pos()[0] - self.rect.center[0]) - self.width / 2, 0.01);
            dy = max(abs(r.get_pos()[1] - self.rect.center[1]) - self.height / 2, 0.01);
            dist = math.sqrt(dx*dx + dy*dy)

            #normalize direction
            if (r.get_pos()[0] < self.rect.center[0]):
                dx = -dx
            dx=dx/dist
            if (r.get_pos()[1] < self.rect.center[1]):
                dy = -dy
            dy=dy/dist
            fmag=0

            if (dist < 20):
                if (dist < 5):
                    r.stop()
                fmag = 50/(dist)

            r.push(fmag*dx, fmag*dy, 10)

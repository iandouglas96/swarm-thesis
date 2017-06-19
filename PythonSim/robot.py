import pygame
from pygame.locals import *
import math
import random

WHITE = (255, 255, 255)

#Robot class -- controls each individual robot
class Robot(pygame.sprite.Sprite):
    id = 0

    def __init__(self, x, y):
        self.id = Robot.id
        Robot.id += 1
        #Call parent constructor
        super(Robot, self).__init__()

        #Create surface sprite will be drawn onto
        self.image = pygame.Surface([50, 50])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        # this rect determinies the position the ball is drawn
        self.rect = self.image.get_rect()
        # Draw the ellipse onto the surface
        pygame.draw.ellipse(self.image, (255,0,0), [20,20,10,10], 1)

        self.rect = self.image.get_rect()
        self.pos = (x,y)
        self.momentum = (0,0)
        self.newpos = self.pos
        self.rect.center = self.pos

        #offset time used to simulate async scans
        self.offset = random.randrange(20)
        self.count = 0

        print "Robot initialized at "+str(x)+", "+str(y)

    def calc_force(self, robots):
        #only allow force to be calculated once every so often
        if (self.offset+20 == self.count):
            #Assemble vector
            force = []
            force.append(0)
            force.append(0)

            for r in robots:
                xcomp = r.get_pos()[0]-self.pos[0]
                ycomp = r.get_pos()[1]-self.pos[1]

                fdist = math.sqrt(xcomp**2 + ycomp**2)
                if (fdist > 0.001):
                    #Add randomness
                    #fdist = math.sqrt((xcomp+random.uniform(-2,2))**2 + (ycomp+random.uniform(-2,2))**2)
                    #Process further if we aren't comparing to ourselves
                    fdir = (xcomp/fdist, ycomp/fdist)

                    if (fdist < 30):
                        #Very strong repulsive force
                        fmag = (fdist-30)/10
                    elif (fdist > 30 and fdist < 100):
                        #Weak(er) attraction
                        fmag = (fdist-35)/40
                    else:
                        fmag = 0

                    force[0] += fmag * fdir[0]
                    force[1] += fmag * fdir[1]

            self.push(force[0],force[1],2)
            self.count = self.offset

            print str(self.id)+" updated\n"

        self.count += 1

    def stop(self):
        self.momentum = [0,0]

    def push(self, xf, yf, limit):
        print str(xf)+" "+str(yf)
        self.momentum = self.mag_limit(xf, yf, limit)

    def update(self):
        self.pos = self.pos[0]+self.momentum[0], self.pos[1]+self.momentum[1]
        self.rect.center = self.pos

    def mag_limit(self, x, y, limit):
        mag = math.sqrt(x**2 + y**2)
        if (mag != 0):
            dir = (x/mag, y/mag)
        else:
            dir = (0,0)

        if (mag > limit):
            mag = limit
        return (dir[0]*mag, dir[1]*mag)

    def get_pos(self):
        return self.pos

    def get_id(self):
        return self.id

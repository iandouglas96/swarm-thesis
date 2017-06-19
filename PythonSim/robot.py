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
        self.original_image = pygame.Surface([50, 50])
        self.original_image.fill(WHITE)
        self.original_image.set_colorkey(WHITE)
        # this rect determinies the position the ball is drawn
        self.rect = self.original_image.get_rect()
        # Draw the rect
        pygame.draw.rect(self.original_image, (255,0,0), [20,20,10,10], 1)
        # Solid front just so we can tell the orientation
        pygame.draw.rect(self.original_image, (255,0,0), [20,20,10,5], 0)
        self.image = self.original_image

        self.rect = self.image.get_rect()
        self.pos = (x,y)
        self.angle = 0
        self.targetangle = 0
        self.linearv = 0
        self.angularv = 0
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
                #only do something if this is a different robot
                if (r.id != self.id):
                    xcomp = r.get_pos()[0]-self.pos[0]
                    ycomp = r.get_pos()[1]-self.pos[1]

                    fdist = math.sqrt(xcomp**2 + ycomp**2)
                    #Add randomness
                    #fdist = math.sqrt((xcomp+random.uniform(-2,2))**2 + (ycomp+random.uniform(-2,2))**2)
                    #Process further if we aren't comparing to ourselves
                    fdir = (xcomp/fdist, ycomp/fdist)

                    if (fdist < 50):
                        #Very strong repulsive force
                        fmag = (fdist-50)/10
                    elif (fdist > 55 and fdist < 100):
                        #Weak(er) attraction
                        fmag = (fdist-55)/30
                    else:
                        fmag = 0

                    force[0] += fmag * fdir[0]
                    force[1] += fmag * fdir[1]

            self.calc_movement(force[0], force[1])

            self.count = self.offset

        self.count += 1

    def calc_movement(self, x, y):
        fangle = math.atan2(y,x)
        fmag = math.sqrt(x**2 + y**2)
        if (fmag > 2):
            fmag = 2

        #find difference in angle
        anglediff = fangle-self.angle
        if (anglediff > math.pi):
            anglediff -= 2*math.pi
        elif (anglediff < -math.pi):
            anglediff += 2*math.pi

        #don't ever really have difference > 90 degrees, since we can reverse
        if (anglediff > math.pi/2):
            anglediff -= math.pi
            fmag *= -1
        elif (anglediff < -math.pi/2):
            anglediff += math.pi
            fmag *= -1

        self.targetangle = self.angle+anglediff
        self.angularv = anglediff*0.1
        self.linearv = fmag*math.cos(anglediff)

    def stop(self):
        self.linearv = 0
        self.angularv = 0

    def update(self):
        if (math.fabs(self.angle-self.targetangle) > 0.05):
            self.angle = self.angle + self.angularv
        self.linearv *= 0.95

        self.pos = self.pos[0]+self.linearv*math.cos(self.angle), self.pos[1]+self.linearv*math.sin(self.angle)
        self.image = pygame.transform.rotate(self.original_image, -90-math.degrees(self.angle))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def get_pos(self):
        return self.pos

    def get_id(self):
        return self.id

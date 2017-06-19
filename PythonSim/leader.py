import pygame
from pygame.locals import *
import math
import random
from robot import Robot

class Leader(Robot):
    def __init__(self, x, y):
        super(Leader, self).__init__(x,y)

    def calc_force(self, robots):
        xcomp = (pygame.mouse.get_pos()[0]-self.pos[0])/10
        ycomp = (pygame.mouse.get_pos()[1]-self.pos[1])/10
        self.calc_movement(xcomp, ycomp)

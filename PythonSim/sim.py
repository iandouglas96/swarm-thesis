import pygame, sys
from pygame.locals import *
from robot import Robot
from wall import Wall
from leader import Leader
import random

def main(num_robots, width, height):
    print "Initializing..."
    #Create graphics window
    pygame.init()
    screen = pygame.display.set_mode((width, height),0,32)
    pygame.display.set_caption('Swarm Simulation')

    # walls = pygame.sprite.RenderUpdates()
    robots = pygame.sprite.RenderUpdates()
    clock = pygame.time.Clock()

    screen.fill((255,255,255))

    # w = Wall(100,300,200,20)
    # walls.add(w)
    # w = Wall(400,300,200,20)
    # walls.add(w)

    #Create robots
    for i in range(0, num_robots):
        r = Robot(width/2 + random.uniform(-100,100), height/2 + + random.uniform(-100,100))
        robots.add(r)

    #Create Leader
    leader = Leader(width/2, height/2)
    robots.add(leader)

    print "Starting Simulation"
    while (True):
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

        for r in robots:
            r.calc_force(robots)

        # for w in walls:
        #     w.calc_forces(robots)

        #Cycle forward
        robots.update()

        #Clear screen
        screen.fill((255,255,255))
        #Redraw
        dirty = robots.draw(screen)
        #Refresh screen
        pygame.display.update()
        #draw walls
        # dirty = walls.draw(screen)
        # pygame.display.update()

        clock.tick(30)

main(2, 500, 500)

import pygame, sys
from pygame.locals import *
import serial
import math

colors = [(255,0,0), (0,255,0), (0,0,255)]

#Read in data stream into usable array format
def read_positions(ser):
    data = ser.readline()
    #truncate the last characters(, \n\r)
    parsed = data[:-4].split(", ")
    intdata = []
    print parsed
    for d in parsed:
        intdata.append(float(d))
    return intdata

def main():
    print "Initializing..."
    #Start pygame
    pygame.init()
    #Setup window
    screen = pygame.display.set_mode((600, 600),0,32)
    pygame.display.set_caption('Virtual Force Exterted')

    #Set up serial connection
    ser = serial.Serial('COM4')

    while(True):
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

        #Clear screen
        screen.fill((255,255,255))

        #draw origin
        pygame.draw.circle(screen, (0,0,0), (300,300), 10, 0)
        #draw range markers every 10cm
        pygame.draw.circle(screen, (0,0,0), (300,300), 40, 1)
        pygame.draw.circle(screen, (0,0,0), (300,300), 80, 1)
        pygame.draw.circle(screen, (0,0,0), (300,300), 120, 1)
        pygame.draw.circle(screen, (0,0,0), (300,300), 160, 1)

        positions = read_positions(ser)
        #Scan through all the detected objects and draw them
        for i in range(0, len(positions)-1, 3):
            if (positions[i] != 0):
                dist = 4*-math.log(positions[i]/1.8956)*14.9
                theta = math.radians(positions[i+1])
                group = positions[i+2]
                x = 300+int(dist*math.cos(theta))
                y = 300-int(dist*math.sin(theta))
                pygame.draw.circle(screen, colors[int(group)], (x,y), 5, 0)

        #Let's draw stuff!
        pygame.display.update()

#Start program
main()

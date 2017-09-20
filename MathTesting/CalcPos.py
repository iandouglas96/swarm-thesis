import numpy as np
from scipy.optimize import minimize
from graphics import *

#p is of the following format
#p[n][v]
#n is the robot number, v the position vector (x,y,theta)
#we also have another matrix, Dp[n][m][v] giving the measured rel pos
#n,m give the robot number, v the x,y components
def sum_errors(p):
    #load up the measured input data
    global Dp
    #reformat p to be easier to work with
    p = np.reshape(p, (p.shape[0]/3,3))
    #create the matrix
    D = np.zeros((p.shape[0],p.shape[0],2))

    for n in range(0,p.shape[0]):
        for m in range(0,p.shape[0]):
            D[n][m][0] = (p[m][0]-p[n][0])*np.cos(p[n][2])-(p[m][1]-p[n][1])*np.sin(p[n][2])
            D[n][m][1] = (p[m][0]-p[n][0])*np.sin(p[n][2])+(p[m][1]-p[n][1])*np.cos(p[n][2])

    #Find all differences
    errors = D-Dp
    #sum of sqaure of errors
    return np.sum(np.square(errors))

Dp = np.array([[[0,0], [-1,1], [0,2]],[[-1,-1], [0,0], [1,-1]],[[-2,0], [-1,1], [0,0]]])
x0 = np.zeros((Dp.shape[0],Dp.shape[0]))
out = minimize(sum_errors, x0)

pts = np.reshape(out.x,(out.x.shape[0]/3,3))
print pts
print "Final error: "+str(out.fun)

win = GraphWin("plot", 500, 500)

for pt in pts:
    pt_graphics = Point(int(250+pt[0]*100), int(250-pt[1]*100))
    cir = Circle(pt_graphics, 5)
    cir.draw(win)
    line = Line(pt_graphics, Point(pt_graphics.x+5*np.cos(-pt[2]+np.pi/2),pt_graphics.y-5*np.sin(-pt[2]+np.pi/2)))
    line.draw(win)

#wait before closing window
win.getMouse()

import numpy as np
from scipy.optimize import minimize
from graphics import *
import random
import math

# Basically just a struct to store node data
class Node:
    def __init__(self, pos, angle, id_num):
        self.pos = pos
        self.angle = angle
        self.id_num = id_num

def gen_configuration(num_nodes):
    global Dp
    node_list = []
    pts = np.zeros((num_nodes, 3))
    # Create nodes
    for n in range(0, num_nodes):
        # Create a new Node with random position
        pos = [random.random()*500, random.random()*500]
        angle = random.random()*360
        node_list.append(Node(pos, angle, n))
        pts[n][0] = pos[0]
        pts[n][1] = pos[1]
        pts[n][2] = np.radians(angle)

    # Create adjacency list
    Dp = np.zeros((len(node_list), len(node_list), 2))
    for n in node_list:
        for adj_n in scan_for_neighbors(n, node_list):
            Dp[n.id_num][adj_n['bin']][0] = adj_n['distance']*np.cos(adj_n['direction'])
            Dp[n.id_num][adj_n['bin']][1] = adj_n['distance']*np.sin(adj_n['direction'])

    return pts

def scan_for_neighbors(node, node_list):
    list = []
    for n in node_list:
        if (n != node):
            dist = math.sqrt((n.pos[0]-node.pos[0])**2+(n.pos[1]-node.pos[1])**2)
            angle = -(math.atan2(n.pos[1]-node.pos[1], n.pos[0]-node.pos[0])-math.radians(node.angle))
            # add error
            # dist += np.random.normal(0, 10)
            # angle += np.random.normal(0, 0.1)
            list.append({'distance': dist, 'direction': angle, 'bin': n.id_num})

    return list

# process points to fit pts1 onto pts2
# uses algorithm described here: http://nghiaho.com/?page_id=671
def normalize_pts(pts1, pts2):
    A = pts1[:, 0:2]
    B = pts2[:, 0:2]
    print A
    print B

    assert len(A) == len(B)

    N = A.shape[0]  # total points

    # find centroids
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)

    # centre the points
    AA = A - np.tile(centroid_A, (N, 1))
    BB = B - np.tile(centroid_B, (N, 1))

    H = np.dot(np.transpose(AA), BB)
    U, S, Vt = np.linalg.svd(H)

    # rotation matrix
    R = np.dot(Vt.T, U.T)

    # special reflection case
    if np.linalg.det(R) > 0:
        print "Reflection detected"
        Vt[1, :] *= -1
        R = np.dot(Vt.T, U.T)

    # calculate transposition
    t = np.dot(-R, centroid_A.T) + centroid_B.T

    # Apply transformation
    A2 = np.dot(R, A.T) + np.tile(t[:, None], (1, N))
    A2 = A2.T

    pts1[:, 0:2] = A2
    # rotate the rotations
    print R
    pts1[:, 2] += math.atan2(R[0][1], R[0][0])

    # calculate the error
    err = A2 - B
    err = np.multiply(err, err)
    err = np.sum(err)
    return err

# p is of the following format
# p[n][v]
# n is the robot number, v the position vector (x,y,theta)
# we also have another matrix, Dp[n][m][v] giving the measured rel pos
# n,m give the robot number, v the x,y components
def sum_errors(p):
    # load up the measured input data
    global Dp
    # reformat p to be easier to work with
    p = np.reshape(p, (p.shape[0]/3, 3))
    # create the matrix
    D = np.zeros((p.shape[0], p.shape[0], 2))

    for n in range(0, p.shape[0]):
        for m in range(0, p.shape[0]):
            # only find relative distance if we have the measured data
            if (Dp[n][m].any()):
                D[n][m][0] = (p[m][0]-p[n][0])*np.cos(p[n][2])-(p[m][1]-p[n][1])*np.sin(p[n][2])
                D[n][m][1] = (p[m][0]-p[n][0])*np.sin(p[n][2])+(p[m][1]-p[n][1])*np.cos(p[n][2])

    # Find all differences
    errors = D-Dp
    # sum of sqaure of errors
    return np.sum(np.square(errors))

# Dp = np.array([[[0,0], [-1,1], [0,2], [0,0]],[[-1,-1], [0,0], [1,-1], [1,0]],[[-2,0], [-1,1], [0,0], [0,1]],[[0,0], [1,0], [0,1], [0,0]]])
# load data
# Dp_raw = np.load('adj.npy')
# add noise
# noise = np.random.normal(0, 10, Dp_raw.size)
# noise = np.reshape(noise, Dp_raw.shape)

# generate random config
pts_act = gen_configuration(10)

# try to minimize error
x0 = np.zeros((Dp.shape[0], 3))
out = minimize(sum_errors, x0)

# format stuff nicely and output
pts = np.reshape(out.x, (out.x.shape[0]/3, 3))
err = normalize_pts(pts, pts_act)

print out
print "=================================="
print pts
print "Final error: "+str(out.fun)
print "Actual error: "+str(err)

# draw calculated locations on screen
win = GraphWin("plot", 500, 500)

for pt in pts:
    pt_graphics = Point(int(pt[0]), int(pt[1]))
    cir = Circle(pt_graphics, 8)
    cir.draw(win)
    line = Line(pt_graphics, Point(pt_graphics.x+8*np.cos(-pt[2]), pt_graphics.y+8*np.sin(-pt[2])))
    line.draw(win)

for pt in pts_act:
    pt_graphics = Point(int(pt[0]), int(pt[1]))
    cir = Circle(pt_graphics, 8)
    cir.setOutline('red')
    cir.draw(win)
    line = Line(pt_graphics, Point(pt_graphics.x+8*np.cos(-pt[2]), pt_graphics.y+8*np.sin(-pt[2])))
    line.draw(win)

# wait before closing window
win.getMouse()

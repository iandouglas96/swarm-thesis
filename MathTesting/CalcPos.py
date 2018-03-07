import numpy as np
from scipy.optimize import minimize
from graphics import *
import random
import math
import timeit
import csv
import rmsd

# Basically just a struct to store node data
class Node:
    def __init__(self, pos, angle, id_num):
        self.pos = pos
        self.angle = angle
        self.id_num = id_num

def gen_configuration(num_nodes):
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

    return pts, Dp

def scan_for_neighbors(node, node_list):
    list = []
    for n in node_list:
        if (n != node):
            dist = math.sqrt((n.pos[0]-node.pos[0])**2+(n.pos[1]-node.pos[1])**2)
            angle = (math.atan2(n.pos[1]-node.pos[1], n.pos[0]-node.pos[0])+math.radians(node.angle))
            # add error
            #dist += np.random.normal(0, 30)
            #angle += np.random.normal(0, 0.1)
            if (dist < 500):
                list.append({'distance': dist, 'direction': angle, 'bin': n.id_num})

    print list
    return list

# process points to fit pts1 onto pts2
# uses algorithm described here: http://nghiaho.com/?page_id=671
def normalize_pts_old(pts1, pts2, win):
    #print pts1
    A = pts1[:, 0:2]
    B = pts2[:, 0:2]

    assert len(A) == len(B)

    N = A.shape[0]  # total points

    # find centroids
    centroid_A = rmsd.centroid(A)
    centroid_B = rmsd.centroid(B)

    # centre the points
    AA = A - centroid_A
    BB = B - centroid_B
    
    #get optimal rotation matrix
    R = rmsd.kabsch(AA, BB)
    # Apply transformation
    AA1 = np.dot(AA, R)
    angle1 = math.atan2(R[1][0], R[1][1])
    
    i=0
    for pt in pts1:
        pt_graphics = Point(int(pt[0]-centroid_A[0]+centroid_B[0]), int(pt[1]-centroid_A[1]+centroid_B[1]))
        cir = Circle(pt_graphics, 8)
        cir.setOutline('green')
        cir.draw(win)
        line = Line(pt_graphics, Point(pt_graphics.x+8*np.cos(-pt[2]), pt_graphics.y+8*np.sin(-pt[2])))
        line.draw(win)
        text = Text(pt_graphics, str(i))
        i += 1
        text.draw(win)
    
    pts1[:, 0:2] = AA1 + centroid_B
    # rotate the rotations
    pts1[:, 2] -= angle1
    return rmsd.rmsd(AA1, BB)

def normalize_pts(pts1, pts2):
    #print pts1
    A = pts1[:, 0:2]
    B = pts2[:, 0:2]

    assert len(A) == len(B)

    N = A.shape[0]  # total points

    # find centroids
    centroid_A = rmsd.centroid(A)
    centroid_B = rmsd.centroid(B)

    # centre the points
    AA = A - centroid_A
    BB = B - centroid_B
    
    #get optimal rotation matrix
    R = rmsd.kabsch(AA, BB)
    # Apply transformation
    AA1 = np.dot(AA, R)
    angle1 = math.atan2(R[1][0], R[1][1])
    
    #try flippin' it
    AA[:, 1] *= -1
    #get optimal rotation matrix
    R = rmsd.kabsch(AA, BB)
    # Apply transformation
    AA2 = np.dot(AA, R)#get optimal rotation matrix
    angle2 = math.atan2(R[1][0], R[1][1])
    
    #go with whichever one is better
    a2diff = np.abs(pts2[:,2]-(pts1[:,2]-angle2))
    a1diff = np.abs(pts2[:,2]-(pts1[:,2]+angle1))
    #angle differences are fun!
    for i in range(0, len(a1diff)):
        while (a2diff[i] > np.pi):
            a2diff[i] -= 2*np.pi
        while (a1diff[i] > np.pi):
            a1diff[i] -= 2*np.pi
    print np.degrees(a2diff), np.degrees(a1diff)
    if (np.sum(np.abs(a1diff)) > np.sum(np.abs(a2diff))):
        pts1[:, 0:2] = AA2 + centroid_B
        # rotate the rotations (backwards, since we mirrored the thing)
        pts1[:, 2] -= angle2
        return rmsd.rmsd(AA2, BB)
    else:
        pts1[:, 0:2] = AA1 + centroid_B
        # rotate the rotations
        pts1[:, 2] += angle1
        return rmsd.rmsd(AA1, BB)

# p is of the following format
# p[n][v]
# n is the robot number, v the position vector (x,y,theta)
# we also have another matrix, Dp[n][m][v] giving the measured rel pos
# n,m give the robot number, v the x,y components
def sum_errors(p, *args):
    # reformat p to be easier to work with
    p = np.reshape(p, (p.shape[0]/3, 3))
    # create the matrix
    D = np.zeros((p.shape[0], p.shape[0], 2))

    #find difference matrices
    px_outer = -np.subtract.outer(p[:, 0], p[:, 0])
    py_outer = -np.subtract.outer(p[:, 1], p[:, 1])
    #trig stuff
    cos_mat = np.cos(p[:, 2])
    sin_mat = np.sin(p[:, 2])

    #x-component
    D[:,:,0] = np.multiply(px_outer, cos_mat[:, np.newaxis])
    D[:,:,0] -= np.multiply(py_outer, sin_mat[:, np.newaxis])
    #y-component
    D[:,:,1] = np.multiply(px_outer, sin_mat[:, np.newaxis])
    D[:,:,1] += np.multiply(py_outer, cos_mat[:, np.newaxis])

    #print D
    
    #remove data that we don't have sensor data for
    D = np.multiply(D, args[0].any(axis = 2)[:, :, np.newaxis])
    # Find all differences
    D -= args[0]
    # sum of sqaure of errors
    return np.sum(np.square(D))

# Dp = np.array([[[0,0], [-1,1], [0,2], [0,0]],[[-1,-1], [0,0], [1,-1], [1,0]],[[-2,0], [-1,1], [0,0], [0,1]],[[0,0], [1,0], [0,1], [0,0]]])
# load data
# Dp_raw = np.load('adj.npy')
# add noise
# noise = np.random.normal(0, 10, Dp_raw.size)
# noise = np.reshape(noise, Dp_raw.shape)

#open file for writing
csvfile = open(name="data.csv", mode='wb')
csvwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
csvwriter.writerow(['num', 'err_solve', 'error_abs', 'time'])

#uncomment for uniformity
#random.seed(10)
for i in range(0, 1):
    # generate random config
    num = 3

    print "iter "+str(i) + ": "+ str(num)+" nodes"
    
    pts_act, Dp = gen_configuration(num)
    
    print Dp

    # try to minimize error
    x0 = np.zeros((Dp.shape[0], 3))

    #Run minimization, but also time execution
    start_time = timeit.default_timer()
    #args has to be a tuple, because of weird numpy problems
    out = minimize(fun=sum_errors, x0=x0, args=(Dp,), method='SLSQP')
    solve_time = timeit.default_timer() - start_time

    print solve_time
    
    # format stuff nicely and output
    pts = np.reshape(out.x, (out.x.shape[0]/3, 3))
    
    '''
    pts = np.array([[ 100+25.4,        100-20.2,          +1.60570291],
                     [ 100-2.2,         100+51.4,         -0.78539816],
                     [100-40.4,          100+8.,          -0.17453293]])
    pts_act = np.array([[100+31.44893379, 100-30.22211118,   +1.13694827],
                        [100-36.55305224, 100-28.97042214,  -2.87720222],
                        [100-6.91792634, 100-75.77796166,  -1.86272542]])
                        '''
    win = GraphWin("plot", 500, 500)
    
    err = normalize_pts_old(pts,pts_act,win)

    # print out
    # print "=================================="
    # print pts
    print "Final error: "+str(out.fun)
    print "Actual error: "+str(err)

    #if we have a solver failure, say something!
    '''if (err > 0.001):
        print out
        print "=================================="
        print pts
        print "Final error: "+str(out.fun)
        print "Actual error: "+str(err)'''

    #csvwriter.writerow([num, out.fun, err, solve_time])

#csvfile.close()

# draw calculated locations on screen
i=0
for pt in pts:
    pt_graphics = Point(int(pt[0]), int(pt[1]))
    cir = Circle(pt_graphics, 8)
    cir.draw(win)
    line = Line(pt_graphics, Point(pt_graphics.x+8*np.cos(-pt[2]), pt_graphics.y+8*np.sin(-pt[2])))
    line.draw(win)
    text = Text(pt_graphics, str(i))
    i += 1
    text.draw(win)

i=0
for pt in pts_act:
    pt_graphics = Point(int(pt[0]), int(pt[1]))
    cir = Circle(pt_graphics, 8)
    cir.setOutline('red')
    cir.draw(win)
    line = Line(pt_graphics, Point(pt_graphics.x+8*np.cos(-pt[2]), pt_graphics.y+8*np.sin(-pt[2])))
    line.setOutline('red')
    line.draw(win)
    text = Text(pt_graphics, str(i))
    i += 1
    text.draw(win)

# wait before closing window
win.getMouse()

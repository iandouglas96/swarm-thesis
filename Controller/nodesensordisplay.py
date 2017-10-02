from kivy.uix.widget import Widget
from kivy.clock import Clock

from constants import *

import math
import numpy as np
from scipy.optimize import minimize

# process points to fit pts1 onto pts2
# uses algorithm described here: http://nghiaho.com/?page_id=671
def normalize_pts(pts1, pts2):
    A = pts1[:, 0:2]
    B = pts2[:, 0:2]

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
def sum_errors(p, Dp):
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
    D -= Dp
    # sum of sqaure of errors
    return np.sum(np.square(D))

class NodeSensorDisplay(Widget):
    def __init__(self, **kwargs):
        super(NodeSensorDisplay, self).__init__(**kwargs)
        self.node_list = []
        Clock.schedule_interval(self.update, 1)

    def set_list(self, node_list):
        self.node_list = []
        for node in node_list:
            self.add_widget(node['data'])
            self.node_list.append(node['data'])

        print self.node_list

    def update(self, dt):
        print "updating"
        Dp = self.gen_adjacencies()

        if (Dp.any()):
            # try to minimize error
            x0 = np.zeros((Dp.shape[0], 3))

            #args has to be a tuple, because of weird numpy problems
            out = minimize(fun=sum_errors, x0=x0, args=(Dp,), method='SLSQP')

            # format stuff nicely and output
            pts = np.reshape(out.x, (out.x.shape[0]/3, 3))

            #update nodes with postitions and angles
            for i in range(0, len(self.node_list)):
                self.node_list[i].pos = [int(pts[i][0]), -int(pts[i][1])]
                self.node_list[i].angle = int(np.degrees(pts[i][2]))

    #generate adjacency list, assuming all frequencies are unique
    def gen_adjacencies(self):
        #create a new array to hold the data
        print len(self.node_list)
        adj = np.zeros((len(self.node_list),len(self.node_list),2))
        for n in self.node_list:
            for adj_n in n.target_list:
                dist = 4*((adj_n['magnitude']/5428)**-(1/2.191))
                adj[FREQUENCIES[n.freq]][adj_n['bin']][0] = dist*np.cos(np.radians(adj_n['direction']))
                adj[FREQUENCIES[n.freq]][adj_n['bin']][1] = dist*np.sin(np.radians(adj_n['direction']))
        return adj

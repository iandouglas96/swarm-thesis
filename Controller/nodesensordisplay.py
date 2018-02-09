from kivy.uix.widget import Widget
from kivy.clock import Clock

from constants import *

import math
import numpy as np
from scipy.optimize import minimize

class NodeSensorDisplay(Widget):
    def __init__(self, **kwargs):
        super(NodeSensorDisplay, self).__init__(**kwargs)
        self.node_list = []
        self.has_init = False
        self.timer = Clock.schedule_interval(self.update, 1)
        
    # process points to fit pts1 onto pts2
    # uses algorithm described here: http://nghiaho.com/?page_id=671
    def normalize_pts(self, pts1, pts2):
        print pts1
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
    def sum_errors(self, p, *args):
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

        #remove data that we don't have sensor data for
        D = np.multiply(D, args[0].any(axis = 2)[:, :, np.newaxis])
        # Find all differences
        D -= args[0]
        # sum of sqaure of errors
        return np.sum(np.square(D))

    def set_list(self, node_list):
        self.node_list = []
        for node in node_list:
            self.add_widget(node['data'])
            self.node_list.append(node['data'])

        print self.node_list

    def update(self, dt):
        if (not self.has_init):
            Dp = self.gen_adjacencies()

            if (Dp.any()):
                print "initializing"
                # try to minimize error
                x0 = np.zeros((Dp.shape[0], 3))

                #args has to be a tuple, because of weird numpy problems
                out = minimize(fun=self.sum_errors, x0=x0, args=(Dp,), method='SLSQP')

                # format stuff nicely and output
                self.pts = np.reshape(out.x, (out.x.shape[0]/3, 3))
                if (hasattr(self, 'last_pts')):
                    #align points to be closest to the last
                    self.normalize_pts(self.pts, self.last_pts)

                #update nodes with postitions and angles
                all_reports_heard = True
                for i in range(0, len(self.node_list)):
                    if (len(self.node_list[i].target_list) == 0):
                        all_reports_heard = False
                    
                    print self.pts[i]
                    
                    for n in self.node_list:
                        if (FREQUENCIES[n.freq] == i):
                            n.pos = [int(self.pts[i][0]), int(self.pts[i][1])]
                            n.angle = int(np.degrees(self.pts[i][2]))
                    
                #If all robots have adjancencies, we are fully initialized
                self.has_init = all_reports_heard
                
                if (all_reports_heard):
                    print "Initialized"
                    #init all the ekfs
                    for n in self.node_list:
                        n.ukf_init()
                    self.timer.cancel()
                    self.timer = Clock.schedule_interval(self.update, 1./60)
                    
                self.last_pts = np.copy(self.pts)
        else:
            #print "Ready for EKF"
            for n in self.node_list:
                n.ukf_predict(dt)

    #generate adjacency list, assuming all frequencies are unique
    def gen_adjacencies(self):
        #create a new array to hold the data
        print len(self.node_list)
        adj = np.zeros((len(self.node_list),len(self.node_list),2))
        for n in self.node_list:
            for adj_n in n.target_list:
                dist = 5.*(adj_n['magnitude'])
                adj[FREQUENCIES[n.freq]][adj_n['bin']][0] = dist*np.cos(np.radians(adj_n['direction']))
                adj[FREQUENCIES[n.freq]][adj_n['bin']][1] = dist*np.sin(np.radians(adj_n['direction']))
        return adj

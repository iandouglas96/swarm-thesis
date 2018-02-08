from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from constants import *
from nodesensordisplay import NodeSensorDisplay

import math
import numpy as np

import cv2

#Defines direction of arrow to render for each robot
robot_arrow = np.float32([[-50,0,0], [50,0,0]]).reshape(-1,3)
#Definition of aruco board sizes
m_width = 71
m_sep = 35.5

class MotionCapture(Image, NodeSensorDisplay):
    def __init__(self, **kwargs):
        super(MotionCapture, self).__init__(**kwargs)
        #load calibration constants for camera
        self.camera_calib_mtx = np.load('camera_calib_mtx.npy')
        self.camera_calib_dist = np.load('camera_calib_dist.npy')
        #grab dict of aruco tags
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
        self.parameters =  cv2.aruco.DetectorParameters_create()
        #aruco board generator
        self.aruco_board = cv2.aruco.Board_create([np.array([[m_sep/2, m_width/2 ,0.],[m_sep/2+m_width, m_width/2, 0. ],[m_sep/2+m_width, -m_width/2, 0.],[m_sep/2, -m_width/2, 0.]], dtype=np.float32),
                                np.array([[-(m_sep/2+m_width), m_width/2 ,0.],[-m_sep/2, m_width/2, 0. ],[-m_sep/2, -m_width/2, 0.],[-(m_sep/2+m_width), -m_width/2, 0.]], dtype=np.float32)], 
                                self.aruco_dict, np.array([0,1]))
        #grab a hook to the webcam
        self.capture = cv2.VideoCapture(0)
        
    #override nodesensordisplay version
    #don't add widget, so we don't actually render nodes
    #rendering will be done through OpenCV
    def set_list(self, node_list):
        self.node_list = []
        for node in node_list:
            self.node_list.append(node['data'])
        #print self.node_list
        
    def draw_robot(self, pos, angle, color, frame):
        #project lines of detected robot locations onto the screen for rendering
        pts, jac = cv2.projectPoints(robot_arrow, np.array([0,0,angle], np.float32),
                                     np.array([pos[0],pos[1],2100], np.float32),
                                     self.camera_calib_mtx, self.camera_calib_dist)
        #draw robots on screen
        frame = cv2.arrowedLine(frame, tuple(pts[0].ravel()), tuple(pts[1].ravel()), color, 5, tipLength=0.3)
        
    def track_robots(self, frame):
        #detect the corners and ids of all the aruco markers
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, self.aruco_dict, parameters=self.parameters)
        
        #if we detected some stuff
        success = False
        if (ids is not None):
            success, rvec, tvec = cv2.aruco.estimatePoseBoard(corners, ids, self.aruco_board, self.camera_calib_mtx, self.camera_calib_dist)

        try:
            if (success):
                #current rotation returned in axis-angle representation.  See Wikipedia for helpful treatment
                #we want to convert to euler angles, and are only interested in rotation about z
                angle = np.linalg.norm(rvec)
                axis = rvec/angle
                s = np.sin(angle)
                c = np.cos(angle)
                t = 1-c
                z_angle = np.arctan2(axis[2]*s - axis[1]*axis[0]*t, 1-(axis[2]**2 + axis[0]**2)*t)-3.14159/2
                return (z_angle, [tvec[0], tvec[1]])
        except TypeError:
            #nothing detected
            pass
        return (None,None)
    
    def update(self, dt):
        #Call NodeSensorDisplay update method
        super(MotionCapture, self).update(dt)
        
        #draw video feed (like a boss)
        ret, frame = self.capture.read()
        if ret:
            for n in self.node_list:
                self.draw_robot([n.pos[0], n.pos[1]], np.radians(n.angle), (255,0,0), frame)
                
            #detect robots
            angle, pos = self.track_robots(frame)
            
            if (angle is not None):
                print angle
                print pos
                self.draw_robot(pos, angle, (0,0,255), frame)
            
            # convert OpenCV image to Kivy texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

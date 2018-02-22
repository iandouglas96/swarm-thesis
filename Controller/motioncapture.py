from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from constants import *
from nodesensordisplay import NodeSensorDisplay

import csv
import math
import numpy as np

import cv2

#Defines direction of arrow to render for each robot
robot_arrow = np.float32([[-5,0,0], [5,0,0]]).reshape(-1,3)
#Definition of aruco board sizes
m_width = 7.1
m_sep = 3.55

class MotionCapture(Image, NodeSensorDisplay):
    def __init__(self, **kwargs):
        super(MotionCapture, self).__init__(**kwargs)
        self.logging = False
        #load calibration constants for camera
        self.camera_calib_mtx = np.load('camera_calib_mtx.npy')
        self.camera_calib_dist = np.load('camera_calib_dist.npy')
        #grab dict of aruco tags
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
        self.parameters =  cv2.aruco.DetectorParameters_create()
        #aruco board generator
        self.aruco_boards = []
        for i in range(0,3):
            self.aruco_boards.append(cv2.aruco.Board_create([np.array([[m_sep/2, m_width/2 ,0.],[m_sep/2+m_width, m_width/2, 0.],[m_sep/2+m_width, -m_width/2, 0.],[m_sep/2, -m_width/2, 0.]], dtype=np.float32),
                                np.array([[-(m_sep/2+m_width), m_width/2 ,0.],[-m_sep/2, m_width/2, 0.],[-m_sep/2, -m_width/2, 0.],[-(m_sep/2+m_width), -m_width/2, 0.]], dtype=np.float32)], 
                                self.aruco_dict, np.array([i*2,i*2+1])))
        #grab a hook to the webcam
        self.capture = cv2.VideoCapture(0)
    
    def toggle_logging(self):
        if (self.logging):
            #close up file
            self.log_file.close()
            #Update button name and flip the boolean
            self.ids.toggle_logging_button.text = "Log"
            self.logging = False
        else:
            #Open file and csv writer
            self.log_file = open('data.csv',"wb")
            self.csv_writer = csv.writer(self.log_file)
            #Update button name and flip the boolean
            self.ids.toggle_logging_button.text = "Stop"
            self.logging = True
        
    #override nodesensordisplay version
    #don't add widget, so we don't actually render nodes
    #rendering will be done through OpenCV
    def set_list(self, node_list):
        self.node_list = []
        for node in node_list:
            self.node_list.append(node['data'])
        #print self.node_list
        
    def draw_robot(self, pos, color, frame):
        #project lines of detected robot locations onto the screen for rendering
        pts, jac = cv2.projectPoints(robot_arrow, np.array([0,0,pos[2]], np.float32),
                                     np.array([pos[0],pos[1],220], np.float32),
                                     self.camera_calib_mtx, self.camera_calib_dist)
        #draw robots on screen
        frame = cv2.arrowedLine(frame, tuple(pts[0].ravel()), tuple(pts[1].ravel()), color, 5, tipLength=0.3)
        
    def track_robots(self, frame):
        #detect the corners and ids of all the aruco markers
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, self.aruco_dict, parameters=self.parameters)
        
        if ids is not None:
            robot_positions = np.zeros([ids.max()/2+1, 3])
        else:
            return np.zeros([0, 3])
            
        for board in self.aruco_boards:
            #if we detected some stuff
            success = False
            if (ids is not None):
                success, rvec, tvec = cv2.aruco.estimatePoseBoard(corners, ids, board, self.camera_calib_mtx, self.camera_calib_dist)

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
                    #add position vector to the overall vector
                    robot_positions[board.ids[0][0]/2] = [tvec[0], tvec[1], z_angle]
            except TypeError:
                #nothing detected
                pass
                
        return robot_positions
    
    def update(self, dt):
        #Call NodeSensorDisplay update method
        super(MotionCapture, self).update(dt)
        
        #draw video feed (like a boss)
        ret, frame = self.capture.read()
        if ret:
            #detect robots
            measured_pos = self.track_robots(frame)
                
            #draw calculated robot positions
            calculated_pos = np.zeros([len(self.node_list), 3])
            for n in self.node_list:
                #expects nodes to be numbered 2,3,4...
                calculated_pos[n.node_id-2] = [n.pos[0]/5., n.pos[1]/5., -np.radians(n.angle)]
            
            if (len(calculated_pos) == len(measured_pos)): 
                #fit points onto eachother
                err = self.normalize_pts(calculated_pos, measured_pos)
                if (self.logging):
                    #find difference b/w known and calculated states
                    difference = calculated_pos-measured_pos
                    #log difference data to csv (like a boss)
                    self.csv_writer.writerow(difference.flatten())
                
            #actually draw stuff
            for p in calculated_pos:
                self.draw_robot(p, (255,0,0), frame)
            for p in measured_pos:   
                self.draw_robot(p, (0,255,0), frame)
            
            # convert OpenCV image to Kivy texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

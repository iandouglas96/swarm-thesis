from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

from constants import *
from nodesensordisplay import NodeSensorDisplay

import math
import numpy as np

import cv2

class MotionCapture(Image, NodeSensorDisplay):
    def __init__(self, **kwargs):
        super(MotionCapture, self).__init__(**kwargs)
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
    
    def update(self, dt):
        #Call NodeSensorDisplay update method
        super(MotionCapture, self).update(dt)
        
        #draw video feed (like a boss)
        ret, frame = self.capture.read()
        if ret:
            # convert OpenCV image to Kivy texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

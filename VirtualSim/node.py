from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.clock import Clock

from constants import *

import math
import random
import struct

class Node(Widget):
    #link node_id to the .kv file by making it a kivy property
    node_id = NumericProperty(0)

    def __init__(self, **kwargs):
        super(Node, self).__init__(**kwargs)
        #configuration numbers
        self.node_id = kwargs['id_num']
        self.verbose_flag = False
        self.target_separation = 40
        self.attraction_const = 1
        self.repulsion_const = 2
        self.angular_v_const = 50
        self.linear_v_const = 3
        self.bin = 0
        self.freq = 1000

        self.manual = False

        self.linear_v = 0
        self.angular_v = 0
        #reference back to the node field
        self.field = kwargs['field']

        self.pos = [600+random.random()*200, 600+random.random()*200]
        self.angle = random.random()*360

        Clock.schedule_once(self.setup_scan, random.random()*1)

    #callback function to create random offset for update scans
    def setup_scan(self, dt):
        Clock.schedule_interval(self.process_targets, 1)

    def process_targets(self, dt):
        #"scan" for the list of relative target locations
        self.targets = self.field.scan_for_neighbors(self)

        #figure out force vector
        force_fwd = 0
        force_side = 0

        for n in self.targets:
            if (n['distance'] < self.target_separation*1.5):
                force_mag = 0
                if (n['distance'] > self.target_separation):
                    force_mag = (n['distance']-self.target_separation)*self.attraction_const
                elif (n['distance'] < self.target_separation):
                    force_mag = (n['distance']-self.target_separation)*self.repulsion_const

                force_fwd += force_mag*math.cos(n['direction'])
                force_side += force_mag*math.sin(n['direction'])

        if (not self.manual):
            self.calc_movement(force_fwd, force_side)

    def calc_movement(self, force_fwd, force_side):
        #convert force vector to motion settings
        if (force_fwd != 0 or force_side != 0):
            #Go back to circular coordinates
            force_angle = math.pi/2-math.atan2(force_fwd, force_side);
            force_mag = math.sqrt(force_fwd*force_fwd + force_side*force_side);

            #put angle in the +-90 degree range
            while (force_angle > math.pi/2):
                force_angle -= math.pi;
                force_mag *= -1;
            while (force_angle < -math.pi/2):
                force_angle += math.pi;
                force_mag *= -1;

            self.angular_v = -(self.angular_v_const * force_angle);
            self.linear_v = (self.linear_v_const * force_mag * math.cos(force_angle));
        else:
            #stop
            self.angular_v = 0
            self.linear_v = 0

    def update(self):
        if (abs(self.linear_v) > 1):
            self.linear_v = math.copysign(50, self.linear_v)
        self.pos[0] += 5 * (self.linear_v/1000.0) * math.cos(math.radians(self.angle))
        self.pos[1] += 5 * (self.linear_v/1000.0) * math.sin(math.radians(self.angle))
        self.angle += self.angular_v/100.0

    def process_cmd(self, cmd):
        payload = ""
        if (ord(cmd[0]) == DUMP_COMMAND):
            payload = struct.pack(FORMATS[DUMP_COMMAND], self.node_id, self.verbose_flag,
                                  self.target_separation, self.attraction_const,
                                  self.repulsion_const, self.angular_v_const, self.linear_v_const,
                                  self.freq)
            self.field.send_reply(self.node_id, CONTROLLER_ID, ord(cmd[0]), payload)
        elif (ord(cmd[0]) == DRIVE_COMMAND):
            #get information back
            self.manual = True
            speeds = struct.unpack(FORMATS[DRIVE_COMMAND], cmd[1:])

            self.linear_v = (speeds[0]+speeds[1])/2
            self.angular_v = (speeds[0]-speeds[1])/2
        elif (ord(cmd[0]) == AUTO_COMMAND):
            self.manual = False

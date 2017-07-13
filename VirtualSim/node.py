from kivy.uix.widget import Widget
from kivy.properties import BoundedNumericProperty
from kivy.clock import Clock
import math
import random

class Node(Widget):
    def __init__(self, **kwargs):
        super(Node, self).__init__(**kwargs)
        #configuration numbers
        self.node_id = kwargs['id_num']
        self.verbose = False
        self.target_separation = 25
        self.attraction_const = 1
        self.repulsion_const = 2
        self.angular_v_const = 50
        self.linear_v_const = 10
        self.bin = 0

        self.linear_v = 0
        self.angular_v = 0
        #reference back to the node field
        self.field = kwargs['field']
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
        
        for (n in neighbors):
            if (n['dist'] < self.target_separation*1.5):
                force_mag = 0
                if (n['dist'] > self.target_separation):
                    force_mag = (n['dist']-self.target_separation)*self.attraction_const
                else if (n['dist'] > self.target_separation):
                    force_mag = (n['dist']-self.target_separation)*self.repulsion_const

    def update(self):
        self.pos[0] += 5 * self.linear_v * math.cos(math.radians(self.angle))
        self.pos[1] += 5 * self.linear_v * math.sin(math.radians(self.angle))
        self.angle += self.angular_v

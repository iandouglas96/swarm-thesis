from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.clock import Clock
import math
import random

class Node(Widget):
    #link node_id to the .kv file by making it a kivy property
    node_id = NumericProperty(0)

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
        self.pos = [300+random.random()*200, 300+random.random()*200]
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

            self.angular_v = (self.angular_v_const * force_angle);
            self.linear_v = (self.linear_v_const * force_mag * math.cos(force_angle));
        else:
            #stop
            self.angular_v = 0
            self.linear_v = 0

    def update(self):
        self.pos[0] += 5 * self.linear_v/500 * math.cos(math.radians(self.angle))
        self.pos[1] += 5 * self.linear_v/500 * math.sin(math.radians(self.angle))
        self.angle += self.angular_v/100

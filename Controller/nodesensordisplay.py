from kivy.uix.widget import Widget
from kivy.graphics import *

import math

class NodeSensorDisplay(Widget):
    def __init__(self, **kwargs):
        super(NodeSensorDisplay, self).__init__(**kwargs)
        self.node = None

    def disp_node(self, node):
        self.node = node

    def update(self):
        #get a nice clean slate
        self.canvas.clear()
        if (self.node != None):
            if (hasattr(self.node, 'target_list')):
                targets = InstructionGroup()
                targets.add(Color(1, 0, 0, 1))

                #we are supposed to display something...
                for target in self.node.target_list:
                    dist = 4*((target['magnitude']/532.03)**-(1/1.854))
                    print dist
                    theta = -math.radians(target['direction'])+math.pi/2
                    x_pos = int(dist*math.cos(theta))
                    y_pos = int(dist*math.sin(theta))
                    targets.add(Ellipse(pos=(self.pos[0]+x_pos+self.size[0]/2-15, self.pos[1]+y_pos+self.size[0]/2-15), size=(30, 30)))

                self.canvas.add(targets)

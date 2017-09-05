from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

from constants import *
from node import Node
import math

#This class acts as the "field" that nodes move around on.  Manages list of nodes as a group
class NodeField(FloatLayout):
    def __init__(self, **kwargs):
        super(NodeField, self).__init__(**kwargs)

        #generate a bunch of robots
        self.node_list = []
        for n in range(2,20):
            #create and configure nodes
            node = Node(id_num=n, field=self)
            self.add_widget(node)
            self.node_list.append(node)

        #create clock to regularly update movement (60fps)
        self.update_clock = Clock.schedule_interval(self.update, 1/60)

    def scan_for_neighbors(self, node):
        list = []
        for n in self.node_list:
            if (n != node):
                dist = math.sqrt((n.pos[0]-node.pos[0])**2+(n.pos[1]-node.pos[1])**2)/5
                angle = -(math.atan2(n.pos[1]-node.pos[1], n.pos[0]-node.pos[0])-math.radians(node.angle))
                list.append({'distance':dist, 'direction':angle, 'bin':n.bin})

        return list

    def update(self, dt):
        for node in self.node_list:
            node.update()

    def process_cmd(self, target_id, cmd):
        if (target_id == BROADCAST_ID):
            #send command to everyone
            for node in self.node_list:
                node.process_cmd(cmd)
        else:
            #send command to target only
            for node in self.node_list:
                if (node.node_id == target_id):
                    node.process_cmd(cmd)

    def send_reply(self, sender, target, cmd, reply):
        self.parent.ser.send_reply_packet(sender, target, cmd, reply)

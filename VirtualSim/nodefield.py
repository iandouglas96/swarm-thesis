from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

from constants import *
from node import Node
import math
import numpy as np

#This class acts as the "field" that nodes move around on.  Manages list of nodes as a group
class NodeField(FloatLayout):
    def __init__(self, **kwargs):
        super(NodeField, self).__init__(**kwargs)

        #generate a bunch of robots
        self.node_list = []
        for n in range(2,7):
            #create and configure nodes
            node = Node(id_num=n, freq = 1000+(n-2)*200, field=self)
            self.add_widget(node)
            self.node_list.append(node)

        #create clock to regularly update movement (60fps)
        self.updating = True
        self.update_clock = Clock.schedule_interval(self.update, 1/60)

    def pause_sim(self):
        self.updating = False

    #generate adjacency list, assuming all frequencies are unique
    def gen_adjacencies(self):
        #create a new array to hold the data
        adj = np.zeros((len(self.node_list),len(self.node_list),2))
        for n in self.node_list:
            for adj_n in self.scan_for_neighbors(n):
                adj[FREQUENCIES[n.freq]][adj_n['bin']][0] = adj_n['distance']*np.cos(adj_n['direction'])
                adj[FREQUENCIES[n.freq]][adj_n['bin']][1] = adj_n['distance']*np.sin(adj_n['direction'])
        np.save('adj.npy', adj)
        return adj

    def scan_for_neighbors(self, node):
        list = []
        for n in self.node_list:
            if (n != node):
                dist = math.sqrt((n.pos[0]-node.pos[0])**2+(n.pos[1]-node.pos[1])**2)/5.
                angle = -(math.atan2(n.pos[1]-node.pos[1], n.pos[0]-node.pos[0])-math.radians(node.angle))
                #add error
                dist += np.random.normal(5, 5)
                angle += np.random.normal(0.05, 0.1)
                list.append({'distance':dist, 'direction':angle, 'bin':FREQUENCIES[n.freq]})
        
        list.append({'distance':np.random.uniform(40,60), 'direction':np.random.uniform(0., 6.), 'bin':np.random.randint(0,4)})
        return list

    def update(self, dt):
        if (self.updating):
            for node in self.node_list:
                node.update(dt)

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

    def send_update(self, sender, target, update_type, update):
        self.parent.ser.send_update_packet(sender, target, update_type, update)

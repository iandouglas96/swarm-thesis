from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

from node import Node

#This class acts as the "field" that nodes move around on.  Manages list of nodes as a group
class NodeField(FloatLayout):
    def __init__(self, **kwargs):
        super(NodeField, self).__init__(**kwargs)
        self.node_list = []
        self.node_list.append(Node())
        self.add_widget(self.node_list[0])
        self.node_list[0].update()

        self.update_clock = Clock.schedule_interval(self.update, 1/60)

    def update(self, dt):
        for node in self.node_list:
            node.update()

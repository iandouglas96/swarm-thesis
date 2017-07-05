from constants import *

from random import sample
from string import ascii_lowercase

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

from serialinterface import SerialInterface

class NodeList(BoxLayout):
    def __init__(self, comm):
        super(BoxLayout, self).__init__()
        self.comm = comm

    def scan(self):
        #scan for robots
        self.node_list = self.comm.send_command(BROADCAST_ID, DUMP_COMMMAND)
        print self.node_list
        #populate list with list of detected nodes
        self.rv.data = []
        self.rv.data = [{'value': "ID: "+str(node['data'][DUMP_DATA_NODE_ID])}
                        for node in self.node_list]

class ControllerApp(App):
    def build(self):
        comm = SerialInterface('COM6')
        return NodeList(comm)

if __name__ == '__main__':
    ControllerApp().run()

#set our main window size
#have to do this first
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '800')

import os

from constants import *

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

from Queue import Queue
from serialinterface import SerialInterface
from nodefield import NodeField

class VirtualSim(FloatLayout):
    def __init__(self, **kwargs):
        super(VirtualSim, self).__init__(**kwargs)
        #open a serial port for controller to hook into
        self.ser = SerialInterface()
        #display the name of the serial port to hook into
        self.ids.serial_label.text = self.ser.get_port_name()
        #set up a timer to regularly check for incoming commands over the serial port
        self.cmd_check = Clock.schedule_interval(self.check_for_commands, 1/10)

    def check_for_commands(self, dt):
        while (self.ser.has_packets()):
            cmd = self.ser.get_next_packet()
            #print "received: "+str([hex(ord(c)) for c in cmd])
            self.ids.node_field.process_cmd(ord(cmd[1]), cmd[2:])

    def gen_adjacencies(self):
        #print self.ids.node_field.gen_adjacencies()
        self.ids.node_field.pause_sim()

class VirtualSimApp(App):
    def build(self):
        return VirtualSim()

if __name__ == '__main__':
    #set our main window size
    VirtualSimApp().run()

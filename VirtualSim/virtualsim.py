#set our main window size
#have to do this first
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '800')

import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from Queue import Queue
from serialinterface import SerialInterface
from nodefield import NodeField

class VirtualSim(BoxLayout):
    def __init__(self, **kwargs):
        super(VirtualSim, self).__init__(**kwargs)
        self.rx = Queue()
        self.tx = Queue()
        self.ser = SerialInterface()
        self.cmd_check = Clock.schedule_interval(self.check_for_commands, 1/10)

    def check_for_commands(self, dt):
        while (self.ser.has_packets()):
            pass

class VirtualSimApp(App):
    def build(self):
        return VirtualSim()

if __name__ == '__main__':
    #set our main window size
    VirtualSimApp().run()

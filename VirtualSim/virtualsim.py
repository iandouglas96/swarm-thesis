import os

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

from Queue import Queue
from serialinterface import SerialInterface

class VirtualSim(FloatLayout):
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
    VirtualSimApp().run()

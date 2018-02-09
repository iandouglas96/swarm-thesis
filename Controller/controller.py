#set our main window size
#have to do this first
from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '500')

from constants import *

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from serialinterface import SerialInterface

from nodelist import *
from editdatapanel import *
from nodesensordisplay import *
from motioncapture import *

class Controller(BoxLayout):
    def __init__(self, **kwargs):
        super(Controller, self).__init__(**kwargs)
        self.comm = SerialInterface('/dev/tty.usbmodem1782091')
        #self.comm = SerialInterface('/dev/ttys002')

    def set_list(self, node_list):
        self.ids.motion_capture.set_list(node_list)

    #Pass data to panel to be populatedd
    def new_selection(self, node):
        self.set_visible_node(True)
        self.ids.data_panel.disp_node(node)

    def update_callback(self):
        #self.ids.sensor_disp.update()
        pass

    def set_visible_node(self, visible):
        if (not visible):
            #"hide" by moving way off screen
            self.ids.data_panel.y = 5000
        else:
            self.ids.data_panel.y = 0

class ControllerApp(App):
    def build(self):
        return Controller()

if __name__ == '__main__':
    #off to the races!
    ControllerApp().run()

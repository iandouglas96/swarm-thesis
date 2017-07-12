from constants import *

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.config import Config

from serialinterface import SerialInterface

from nodelist import *
from editdatapanel import *
from nodesensordisplay import *

class Controller(BoxLayout):
    def __init__(self, **kwargs): 
        super(Controller, self).__init__(**kwargs)
        self.comm = SerialInterface('/dev/tty.usbmodem2654621')

    #Pass data to panel to be populatedd
    def new_selection(self, node):
        self.ids.data_panel.disp_node(node)
        self.ids.sensor_disp.disp_node(node)

    def update_callback(self):
        self.ids.sensor_disp.update()

class ControllerApp(App):
    def build(self):
        return Controller()

if __name__ == '__main__':
    #set our main window size
    Config.set('graphics', 'width', '900')
    Config.set('graphics', 'height', '500')
    Config.write()
    #off to the races!
    ControllerApp().run()

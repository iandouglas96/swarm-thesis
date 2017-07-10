from constants import *

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from serialinterface import SerialInterface

from nodelist import *
from editdatapanel import *

class Controller(BoxLayout):
    def __init__(self, **kwargs):
        super(Controller, self).__init__(**kwargs)
        self.comm = SerialInterface('/dev/tty.usbmodem2654621')

    #Pass data to panel to be populatedd
    def new_selection(self, node):
        self.ids.data_panel.disp_node(node)

class ControllerApp(App):
    def build(self):
        return Controller()

if __name__ == '__main__':
    ControllerApp().run()

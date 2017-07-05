from constants import *

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from serialinterface import SerialInterface

from nodelist import *

class Controller(BoxLayout):
    def __init__(self, comm):
        super(Controller, self).__init__()
        self.comm = comm

    def new_selection(self, data):
        print data

class ControllerApp(App):
    def build(self):
        comm = SerialInterface('COM6')
        return Controller(comm)

if __name__ == '__main__':
    ControllerApp().run()

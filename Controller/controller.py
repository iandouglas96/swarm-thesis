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
        #clear list
        print self.comm.send_command(255, 0x10)
        self.rv.data = []
        self.rv.data = [{'value': ''.join(sample(ascii_lowercase, 6))}
                        for x in range(50)]

class ControllerApp(App):
    def build(self):
        comm = SerialInterface('COM6')
        return NodeList(comm)

if __name__ == '__main__':
    ControllerApp().run()

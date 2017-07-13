from kivy.uix.widget import Widget
from kivy.properties import BoundedNumericProperty

class Node(Widget):
    def __init__(self, **kwargs):
        super(Node, self).__init__(**kwargs)

    def update(self):
        #self.pos[0] += 1
        self.angle += 5

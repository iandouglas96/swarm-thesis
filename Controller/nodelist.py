from constants import *

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout

from serialinterface import SerialInterface
from node import Node

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass
    #Want layout to inherit these superclasses so we can select stuff

class NodeRowEntry(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        #Catch and handle the view changes
        self.index = index
        return super(NodeRowEntry, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        #Add selection on touch down
        if super(NodeRowEntry, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        #Set selected property so graphics update appropriately
        self.selected = is_selected
        if is_selected:
            #If we were just selected, tell the list so it can act accordingly
            rv.parent.new_selection(index);

class NodeList(BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def scan(self):
        #scan for robots
        self.node_list = self.parent.comm.send_command(BROADCAST_ID, DUMP_COMMAND)
        print self.node_list
        #populate list with list of detected nodes
        self.rv.data = []
        self.rv.data = [{'value': "ID: "+str(node['data'][DUMP_DATA_NODE_ID]), 'data':Node(node['data'], self.parent.comm)} for node in self.node_list]

    def new_selection(self, index):
        #Pass back to the highest level so it knows what to do
        self.parent.new_selection(self.rv.data[index]['data'])

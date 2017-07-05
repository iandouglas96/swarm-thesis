from kivy.uix.boxlayout import BoxLayout
from constants import *

class EditDataPanel(BoxLayout):
    def test(self, data):
        #Load all the current data values into their respective textboxes
        self.ids.target_separation.text_box.text = str(data[DUMP_DATA_TARGET_SEPARATION])
        self.ids.attraction_const.text_box.text = str(data[DUMP_DATA_ATTRACTION_CONST])
        self.ids.repulsion_const.text_box.text = str(data[DUMP_DATA_REPULSION_CONST])
        self.ids.angular_v_const.text_box.text = str(data[DUMP_DATA_ANGULAR_VELOCITY_CONST])
        self.ids.linear_v_const.text_box.text = str(data[DUMP_DATA_LINEAR_VELOCITY_CONST])
        self.ids.node_id.text_box.text = str(data[DUMP_DATA_NODE_ID])

        self.ids.verbose.active = data[DUMP_DATA_VERBOSE]

    def apply_changes(self):
        print "apply those changes"

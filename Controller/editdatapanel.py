from kivy.uix.boxlayout import BoxLayout
from constants import *
import struct

class EditDataPanel(BoxLayout):
    def test(self, data):
        self.current_id = data[DUMP_DATA_NODE_ID]
        #Load all the current data values into their respective textboxes
        self.ids.target_separation.text_box.text = str(data[DUMP_DATA_TARGET_SEPARATION])
        self.ids.attraction_const.text_box.text = str(data[DUMP_DATA_ATTRACTION_CONST])
        self.ids.repulsion_const.text_box.text = str(data[DUMP_DATA_REPULSION_CONST])
        self.ids.angular_v_const.text_box.text = str(data[DUMP_DATA_ANGULAR_VELOCITY_CONST])
        self.ids.linear_v_const.text_box.text = str(data[DUMP_DATA_LINEAR_VELOCITY_CONST])
        self.ids.node_id.text_box.text = str(data[DUMP_DATA_NODE_ID])

        self.ids.verbose.active = data[DUMP_DATA_VERBOSE]

    def apply_changes(self):
        target_separation = int(self.ids.target_separation.text_box.text)
        attraction_const = int(self.ids.attraction_const.text_box.text)
        repulsion_const = int(self.ids.repulsion_const.text_box.text)
        angular_v_const = int(self.ids.angular_v_const.text_box.text)
        linear_v_const = int(self.ids.linear_v_const.text_box.text)
        node_id = int(self.ids.node_id.text_box.text)

        verbose_flag = self.ids.verbose.active

        #pack all the data we want to send
        args = struct.pack(FORMATS[DUMP_COMMAND], node_id, verbose_flag, target_separation, attraction_const,
                            repulsion_const, angular_v_const, linear_v_const)

        #send the command
        self.parent.comm.send_command(self.current_id, SET_CONSTS_COMMAND, args)
        #Node now has a new id
        self.current_id = node_id

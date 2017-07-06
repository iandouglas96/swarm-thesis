from kivy.uix.boxlayout import BoxLayout
from constants import *
import struct

class EditDataPanel(BoxLayout):
    def disp_node(self, node):
        self.node = node
        self.current_id = node.node_id
        #Load all the current data values into their respective textboxes
        self.ids.target_separation.text_box.text = str(node.target_separation)
        self.ids.attraction_const.text_box.text = str(node.attraction_const)
        self.ids.repulsion_const.text_box.text = str(node.repulsion_const)
        self.ids.angular_v_const.text_box.text = str(node.angular_v_const)
        self.ids.linear_v_const.text_box.text = str(node.linear_v_const)
        self.ids.node_id.text_box.text = str(node.node_id)

        self.ids.verbose.active = node.verbose_flag

    def apply_changes(self):
        self.node.target_separation = int(self.ids.target_separation.text_box.text)
        self.node.attraction_const = int(self.ids.attraction_const.text_box.text)
        self.node.repulsion_const = int(self.ids.repulsion_const.text_box.text)
        self.node.angular_v_const = int(self.ids.angular_v_const.text_box.text)
        self.node.linear_v_const = int(self.ids.linear_v_const.text_box.text)
        self.node.node_id = int(self.ids.node_id.text_box.text)
        self.node.verbose_flag = self.ids.verbose.active

        #Tell the node to send data over comm link
        self.node.send_data()

    def toggle_control_mode(self, state):
        print state
        if (state == "normal"):
            self.node.set_manual(False)
        else:
            self.node.set_manual(True)

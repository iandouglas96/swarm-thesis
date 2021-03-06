from kivy.uix.boxlayout import BoxLayout
from constants import *
import struct

class EditDataPanel(BoxLayout):
    def disp_node(self, node):
        try:
            self.node.set_active(False)
        except:
            #ignore exceptions
            pass

        self.node = node
        self.node.set_active(True)
        self.current_id = node.node_id
        #Load all the current data values into their respective textboxes
        self.ids.target_separation.text_box.text = str(node.target_separation)
        self.ids.attraction_const.text_box.text = str(node.attraction_const)
        self.ids.repulsion_const.text_box.text = str(node.repulsion_const)
        self.ids.sensor_calib_1.text_box.text = str(node.sensor_calib_1)
        self.ids.sensor_calib_2.text_box.text = str(node.sensor_calib_2)
        self.ids.angular_v_const.text_box.text = str(node.angular_v_const)
        self.ids.linear_v_const.text_box.text = str(node.linear_v_const)
        self.ids.node_id.text_box.text = str(node.node_id)

        self.ids.verbose.active = node.verbose_flag

        print node.manual
        if (node.manual):
            self.ids.manual_control.state = 'down'
        else:
            self.ids.manual_control.state = 'normal'

        self.ids.freq.text_box.text = str(node.freq)

    def apply_changes(self):
        self.node.target_separation = int(self.ids.target_separation.text_box.text)
        self.node.attraction_const = float(self.ids.attraction_const.text_box.text)
        self.node.repulsion_const = float(self.ids.repulsion_const.text_box.text)
        self.node.sensor_calib_1 = float(self.ids.sensor_calib_1.text_box.text)
        self.node.sensor_calib_2 = float(self.ids.sensor_calib_2.text_box.text)
        self.node.angular_v_const = int(self.ids.angular_v_const.text_box.text)
        self.node.linear_v_const = int(self.ids.linear_v_const.text_box.text)
        self.node.node_id = int(self.ids.node_id.text_box.text)
        self.node.verbose_flag = self.ids.verbose.active
        self.node.freq = int(self.ids.freq.text_box.text)

        #Tell the node to send data over comm link
        self.node.send_data()

    def toggle_control_mode(self, state):
        print state
        if (state == "normal"):
            self.node.set_manual(False)
        else:
            self.node.set_manual(True)

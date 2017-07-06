from kivy.core.window import Window
from constants import *
from serialinterface import SerialInterface
import struct

#A Class for keeping track of robot data
class Node():
    def __init__(self, data, ser):
        #parse data
        self.set_data(data)
        self.current_id = self.node_id
        self.comm = ser
        self.manual = False

    #Parse data struct
    def set_data(self, data):
        self.node_id = data[DUMP_DATA_NODE_ID]
        self.verbose_flag = data[DUMP_DATA_VERBOSE]
        self.target_separation = data[DUMP_DATA_TARGET_SEPARATION]
        self.attraction_const = data[DUMP_DATA_ATTRACTION_CONST]
        self.repulsion_const = data[DUMP_DATA_REPULSION_CONST]
        self.angular_v_const = data[DUMP_DATA_ANGULAR_VELOCITY_CONST]
        self.linear_v_const = data[DUMP_DATA_LINEAR_VELOCITY_CONST]

    #Update prefs over communication link
    def send_data(self):
        #pack all the data we want to send
        args = struct.pack(FORMATS[DUMP_COMMAND], self.node_id, self.verbose_flag,
                            self.target_separation, self.attraction_const,
                            self.repulsion_const, self.angular_v_const, self.linear_v_const)

        #send the command
        self.comm.send_command(self.current_id, SET_CONSTS_COMMAND, args)

        #Now the ID has actually changed
        self.current_id = self.node_id

    def set_manual(self, manual):
        if (manual):
            #take over the keyboard
            Window.bind(on_key_down=self.key_action)
        else:
            #relinquish the keyboard
            Window.unbind(on_key_down=self.key_action)

    def key_action(self, *args):
        print "got a key event: %s" % list(args)

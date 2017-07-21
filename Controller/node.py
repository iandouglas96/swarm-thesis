from kivy.core.window import Window
from constants import *
from serialinterface import SerialInterface
import struct

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

#A Class for keeping track of robot data
class Node():
    def __init__(self, data, ser):
        #parse data
        self.set_data(data)
        self.current_id = self.node_id
        self.comm = ser
        self.manual = True
        #u, r, d, l
        self.key_matrix = [False, False, False, False]
        self.old_matrix = [False, False, False, False]

    #Parse data struct
    def set_data(self, data):
        self.node_id = data[DUMP_DATA_NODE_ID]
        self.verbose_flag = data[DUMP_DATA_VERBOSE]
        self.target_separation = data[DUMP_DATA_TARGET_SEPARATION]
        self.attraction_const = data[DUMP_DATA_ATTRACTION_CONST]
        self.repulsion_const = data[DUMP_DATA_REPULSION_CONST]
        self.angular_v_const = data[DUMP_DATA_ANGULAR_VELOCITY_CONST]
        self.linear_v_const = data[DUMP_DATA_LINEAR_VELOCITY_CONST]
        self.freq = data[DUMP_DATA_FREQ]

    #Update prefs over communication link
    def send_data(self):
        #pack all the data we want to send
        args = struct.pack(FORMATS[DUMP_COMMAND], self.node_id, self.verbose_flag,
                            self.target_separation, self.attraction_const,
                            self.repulsion_const, self.angular_v_const, self.linear_v_const,
                            self.freq)

        #send the command
        self.comm.send_command(self.current_id, SET_CONSTS_COMMAND, args)

        #Now the ID has actually changed
        self.current_id = self.node_id

    #turn off or on manual mode
    def set_manual(self, manual):
        self.manual = manual
        if (manual):
            #take over the keyboard
            Window.bind(on_key_down=self.key_down)
            Window.bind(on_key_up=self.key_up)

            #enter manual control mode (and stop)
            args = struct.pack(FORMATS[DRIVE_COMMAND], 0, 0)
            self.comm.send_command(self.current_id, DRIVE_COMMAND, args)
        else:
            #relinquish the keyboard
            Window.unbind(on_key_down=self.key_down)
            Window.unbind(on_key_up=self.key_up)
            self.key_matrix = [False, False, False, False]

            #return to auto control
            self.comm.send_command(self.current_id, AUTO_COMMAND)

    #called when user changes focus to or away
    def set_active(self, active):
        if (active and self.manual):
            #take over the keyboard
            Window.bind(on_key_down=self.key_down)
            Window.bind(on_key_up=self.key_up)
        elif (not active and self.manual):
            #relinquish the keyboard
            Window.unbind(on_key_down=self.key_down)
            Window.unbind(on_key_up=self.key_up)

    def key_down(self, window, key, *args):
        if (key == 273):
            #up
            self.key_matrix[UP] = True
        elif (key == 275):
            #right
            self.key_matrix[RIGHT] = True
        elif (key == 274):
            #down
            self.key_matrix[DOWN] = True
        elif (key == 276):
            #left
            self.key_matrix[LEFT] = True

        self.command_motion()

    def key_up(self, window, key, *args):
        if (key == 273):
            #up
            self.key_matrix[UP] = False
        elif (key == 275):
            #right
            self.key_matrix[RIGHT] = False
        elif (key == 274):
            #down
            self.key_matrix[DOWN] = False
        elif (key == 276):
            #left
            self.key_matrix[LEFT] = False

        self.command_motion()

    #If motion controls changed, send the appropriate command to the robot
    def command_motion(self):
        #only send command if something changed, so we don't spam the comm system
        if (self.old_matrix != self.key_matrix):
            r_speed = 150*(self.key_matrix[UP]-self.key_matrix[DOWN])+100*(self.key_matrix[LEFT]-self.key_matrix[RIGHT])
            l_speed = 150*(self.key_matrix[UP]-self.key_matrix[DOWN])+100*(self.key_matrix[RIGHT]-self.key_matrix[LEFT])

            #payload, assemble!
            args = struct.pack(FORMATS[DRIVE_COMMAND], r_speed, l_speed)

            #send the command
            self.comm.send_command(self.current_id, DRIVE_COMMAND, args)

            #slice so we copy values instead of ref
            self.old_matrix = self.key_matrix[:]

    def update(self, update_type, data):
        if (update_type == TARGET_LIST_UPDATE):
            #clear out list before we load in new values
            self.target_list = []
            for bin in range(0, TARGET_LIST_NUM_TARGETS):
                #verify that the magnitude is nonzero to see if it is a target
                if (data[bin*3] != 0):
                    target = {'magnitude':data[bin*3+TARGET_LIST_UPDATE_MAGNITUDE],
                              'direction':data[bin*3+TARGET_LIST_UPDATE_DIRECTION],
                              'bin':data[bin*3+TARGET_LIST_UPDATE_BIN]}
                    self.target_list.append(target)
            print self.target_list

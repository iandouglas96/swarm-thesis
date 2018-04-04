import threading
import time
import numpy as np

class RunPreset(threading.Thread):
    def __init__(self, node_list, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        #internally save node list reference for sending commands later
        self.node_list = node_list
        self.daemon = True

    #Send wheel speed command to a particular robot
    def send_command(self, id_num, Vl, Vr):
        for n in self.node_list:
            if (n.current_id == id_num):
                #found the right robot, set new speeds
                n.control = np.array([Vl, Vr])
                #apply changes, send wireless command
                n.send_motion_command()
                return
        #if we get here, robot was not found
        print "Error, robot with id "+str(id_num)+" not found!"
    
    def formation1(self):
        '''
        print "Running formation 1: CCW circle"
        self.send_command(2, 120, 100)
        self.send_command(3, 120, 100)
        self.send_command(4, 120, 100)
        time.sleep(60)
        self.send_command(2, 0, 0)
        self.send_command(3, 0, 0)
        self.send_command(4, 0, 0)
        print "Formation 1 complete"
        '''

        print "Running formation 2: Star expand"
        self.send_command(2, 100, 100)
        self.send_command(3, 100, 100)
        self.send_command(4, 100, 100)
        time.sleep(10)
        self.send_command(2, -100, -100)
        self.send_command(3, -100, -100)
        self.send_command(4, -100, -100)
        time.sleep(10)
        self.send_command(2, 0, 0)
        self.send_command(3, 0, 0)
        self.send_command(4, 0, 0)
        print "Formation 2 complete"

    def run(self):
        #run through sequence of commands, then finish.
        self.formation1()
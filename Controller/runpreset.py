import threading
import time

class RunPreset(threading.Thread):
    def __init__(self, node_list, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        #internally save node list reference for sending commands later
        self.node_list = node_list
        self.daemon = True
    
    def run(self):
        #run through sequence of commands, then finish.
        print "hello"
        time.sleep(5)
        print "goodbye"
import threading
from Queue import Queue
import os

class SerialInterface:
    def __init__(self):
        master,slave = os.openpty()

        #create queues
        self.tx = Queue()
        self.rx = Queue()

        #start rx/tx threads
        TxManager(master, self.tx).start()
        RxManager(master, self.rx).start()

        #print out the port we should connect to
        self.port_name = os.ttyname(slave)

    def has_packets(self):
        #return True if there is something in the queue
        return not self.rx.empty()

    def get_port_name(self):
        return self.port_name

class TxManager(threading.Thread):
    def __init__(self, port, tx_queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.tx_queue = tx_queue
        #quit when the parent quits
        self.daemon = True

    #This method is called when thread is started
    def run(self):
        #Loop 4eva
        while True:
            msg = self.tx_queue.get()
            os.write(self.port, msg)

class RxManager(threading.Thread):
    def __init__(self, port, rx_queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.rx_queue = rx_queue
        self.port = port
        #quit when the parent quits
        self.daemon = True

    def run(self):
        while True:
            #this is blocking, which is why we use another thread
            msg = os.read(self.port,1024)
            self.rx_queue.put(msg)

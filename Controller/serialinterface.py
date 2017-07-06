from serial import Serial
import struct
from constants import *

#Helper class to manage wireless comms
class SerialInterface:
    def __init__(self, port):
        #open serial port, set read timeout
        self.ser = Serial(port, timeout=0.5)

    def __del__(self):
        print "closing serial port..."
        self.ser.close()

    #package and send a command
    def send_command(self, target_id, cmd, args=''):
        #total message length, target id, followed by command and any arguments
        payload = chr(len(args)+3)+chr(target_id)+chr(cmd)+args

        print "Sending: "+str([hex(ord(c)) for c in payload])

        self.ser.write(payload)
        self.ser.flush() #make sure we push out the whole command

        #If we are broadcasting, we want to receive multiple response packets
        if (target_id == BROADCAST_ID and (cmd == DUMP_COMMAND)):
            response_list = []
            #Keep looking for responses until we timeout
            while True:
                response = self.handle_response()
                if (response == None):
                    break
                response_list.append(response)
            self.ser.reset_input_buffer();
            return response_list
        else:
            #Was this a command expecting a reply?
            if (cmd == DUMP_COMMAND):
                #We only want one response
                return self.handle_response()

    def handle_response(self):
        #process header
        header = self.ser.read(struct.calcsize(HEADER_FORMAT))
        try:
            header_struct = struct.unpack(HEADER_FORMAT, header)
        except struct.error:
            if (len(header) == 0):
                print "No response"
            else:
                print "Bad header.  Raw data: " + str([hex(ord(c)) for c in header])
            return

        #send to appropriate handler depending on the command
        #Length is the overall packet length minus the length of the header
        data = self.ser.read(header_struct[HEADER_LENGTH]-struct.calcsize(HEADER_FORMAT))
        try:
            print header_struct[HEADER_COMMAND]
            data_struct = struct.unpack(FORMATS[header_struct[HEADER_COMMAND]], data)
        except struct.error:
            print "Data not of correct format.  Raw data: " + str([hex(ord(c)) for c in data])
            return

        return {'sender_id':header_struct[HEADER_SENDER], 'cmd':header_struct[HEADER_COMMAND], 'data':data_struct}

    #check for incoming data
    def receive_data(self):
        pass

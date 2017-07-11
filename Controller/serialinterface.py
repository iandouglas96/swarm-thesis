from serial import Serial
import struct
from constants import *

#Helper class to manage wireless comms
class SerialInterface:
    def __init__(self, port):
        #open serial port, set read timeout
        self.ser = Serial(port, timeout=0.5)
        self.update_packet_on = 0
        self.update_data = ''

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

    #Handle the response to the command we just sent
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
            data_struct = struct.unpack(FORMATS[header_struct[HEADER_COMMAND]], data)
        except struct.error:
            print "Data not of correct format.  Raw data: " + str([hex(ord(c)) for c in data])
            return

        return {'sender_id':header_struct[HEADER_SENDER], 'cmd':header_struct[HEADER_COMMAND], 'data':data_struct}

    #check for incoming data
    def check_for_updates(self):
        #we have to have at least a header worth of data for this to be useful
        if (self.ser.in_waiting > struct.calcsize(HEADER_FORMAT+LONG_HEADER_FORMAT)):
            header = self.ser.read(struct.calcsize(HEADER_FORMAT+LONG_HEADER_FORMAT))
            print "update packet received"
            try:
                header_struct = struct.unpack(HEADER_FORMAT+LONG_HEADER_FORMAT, header)
            except struct.error:
                print "Bad update header.  Raw data: " + str([hex(ord(c)) for c in header])
                self.ser.reset_input_buffer()
                return

            #Verify that we are receiving packets in the correct order
            if (self.update_packet_on != header_struct[LONG_HEADER_ID]):
                print "Received packet out of order"
                self.update_packet_on = 0
                self.update_data = ''
                self.ser.reset_input_buffer();
                return

            self.update_packet_on += 1

            #Length is the overall packet length minus the length of the header
            data = self.ser.read(header_struct[HEADER_LENGTH]-struct.calcsize(HEADER_FORMAT+LONG_HEADER_FORMAT))
            #append data
            self.update_data += data

            #have we received the whole packet?
            if (header_struct[LONG_HEADER_ID] == header_struct[LONG_HEADER_NUM_PACKETS]):
                try:
                    data_struct = struct.unpack(UPDATE_FORMATS[header_struct[HEADER_COMMAND]], self.update_data)
                    #reset stuff
                    self.update_packet_on = 0
                    self.update_data = ''
                    print "complete packet parsed"
                    return {"id_num":header_struct[HEADER_SENDER], "cmd":header_struct[HEADER_COMMAND], "data":data_struct}
                except struct.error:
                    print "Data not of correct format.  Raw data: " + str([hex(ord(c)) for c in self.update_data])

                    return

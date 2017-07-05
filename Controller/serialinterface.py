from serial import Serial
import struct

BROADCAST_ID = 255
#This must be consistent with eeprom_structure.h in the swarm arduino project
HEADER_FORMAT = "BBB"

DUMP_COMMMAND = 0x10
FORMATS = {DUMP_COMMMAND:"IIIIIB?I"}

#Helper class to manage wireless comms
class SerialInterface:
    def __init__(self, port):
        #open serial port, set read timeout
        self.ser = Serial(port, timeout=0.1)

    def __del__(self):
        self.ser.close()

    #package and send a command
    def send_command(self, target_id, cmd, args=''):
        #target id, followed by command and any arguments, then \n
        payload = chr(target_id)+chr(cmd)+args+chr(0x0A)
        self.ser.write(payload)
        self.ser.flush() #make sure we push out the whole command

        if (cmd == DUMP_COMMMAND):
            print self.handle_response()

    def handle_response(self):
        #process header
        try:
            header = self.ser.read(struct.calcsize(HEADER_FORMAT))
            header_struct = struct.unpack(HEADER_FORMAT, header)
        except struct.error:
            print "Bad header or No response"
            return

        #send to appropriate handler depending on the command
        data = self.ser.read(struct.calcsize(FORMATS[header_struct[2]]))
        try:
            data_struct = struct.unpack(FORMATS[header_struct[2]], data)
        except struct.error:
            print "Data not of correct format.  Raw data: " + str([hex(ord(c)) for c in data])
            return

        return {'sender_id':header_struct[0], 'cmd':header_struct[2], 'data':data_struct}

    #check for incoming data
    def receive_data(self):
        pass

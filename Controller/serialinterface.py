from serial import Serial
import struct

BROADCAST_ID = 255
#This must be consistent with eeprom_structure.h in the swarm arduino project
DUMP_STRUCT_FORMAT = "BBB"+"IIIIIB?I"

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

        if (cmd == 0x10):
            return self.handle_dump(target_id)

    #Handle response from "dump" command
    def handle_dump(self, target_id):
        dump_data = []
        #Loop to process
        while (True):
            line = self.ser.readline()
            print "raw: "+line
            try:
                dump_struct = struct.unpack(DUMP_STRUCT_FORMAT, line)
                dump_data.append(dump_struct)
            except struct.error:
                print "Dump data not of correct format.  Raw data: "+line
                return 0

            if (target_id != BROADCAST_ID):
                break

        return dump_data

    #check for incoming data
    def receive_data(self):
        pass

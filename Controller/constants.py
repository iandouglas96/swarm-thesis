#ID to send to to send to all nodes
BROADCAST_ID = 255
#This must be consistent with eeprom_structure.h in the swarm arduino project
HEADER_FORMAT = "BBB"
HEADER_SENDER = 0
HEADER_TYPE = 1
HEADER_COMMAND = 2

#Command listing
DUMP_COMMMAND = 0x10

#Format of returned data from commands
FORMATS = {DUMP_COMMMAND:"IIIIIB?I"}

#definitions for data structure
DUMP_DATA_TARGET_SEPARATION = 0
DUMP_DATA_ATTRACTION_CONST = 1
DUMP_DATA_REPULSION_CONST = 2
DUMP_DATA_ANGULAR_VELOCITY_CONST = 3
DUMP_DATA_LINEAR_VELOCITY_CONST = 4
DUMP_DATA_NODE_ID = 5
DUMP_DATA_VERBOSE = 6
DUMP_DATA_CHECKSUM = 7

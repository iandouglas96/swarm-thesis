#ID to send to to send to all nodes
BROADCAST_ID = 255
#This must be consistent with eeprom_structure.h in the swarm arduino project
HEADER_FORMAT = "BBB"
HEADER_SENDER = 0
HEADER_TYPE = 1
HEADER_COMMAND = 2

#Command listing
DUMP_COMMAND = 0x10
SET_CONSTS_COMMAND = 0x13

#Format of returned data from commands
FORMATS = {DUMP_COMMAND:"B?IIIII"}

#definitions for data structure
DUMP_DATA_NODE_ID = 0
DUMP_DATA_VERBOSE = 1
DUMP_DATA_TARGET_SEPARATION = 2
DUMP_DATA_ATTRACTION_CONST = 3
DUMP_DATA_REPULSION_CONST = 4
DUMP_DATA_ANGULAR_VELOCITY_CONST = 5
DUMP_DATA_LINEAR_VELOCITY_CONST = 6

#ID to send to to send to all nodes
BROADCAST_ID = 0
CONTROLLER_ID = 1
#This must be consistent with eeprom_structure.h in the swarm arduino project
HEADER_FORMAT = "BBBB"
HEADER_LENGTH = 0
HEADER_SENDER = 1
HEADER_TYPE = 2
HEADER_COMMAND = 3

LONG_HEADER_FORMAT = "BB"
LONG_HEADER_ID = 4
LONG_HEADER_NUM_PACKETS = 5

#Command listing
TARGET_LIST_UPDATE = 0x10

DUMP_COMMAND = 0x10
SET_CONSTS_COMMAND = 0x13
DRIVE_COMMAND = 0x16
AUTO_COMMAND = 0x18

#Format of returned data from commands
FORMATS = {DUMP_COMMAND:"B?IffIII", DRIVE_COMMAND:"ii"}

#definitions for data structures
DUMP_DATA_NODE_ID = 0
DUMP_DATA_VERBOSE = 1
DUMP_DATA_TARGET_SEPARATION = 2
DUMP_DATA_ATTRACTION_CONST = 3
DUMP_DATA_REPULSION_CONST = 4
DUMP_DATA_ANGULAR_VELOCITY_CONST = 5
DUMP_DATA_LINEAR_VELOCITY_CONST = 6
DUMP_DATA_FREQ = 7

UPDATE_FORMATS = {TARGET_LIST_UPDATE:"fhhfhhfhhfhhfhhfhhfhhfhhfhhfhh"}

TARGET_LIST_UPDATE_MAGNITUDE = 0
TARGET_LIST_UPDATE_DIRECTION = 1
TARGET_LIST_UPDATE_BIN = 2
TARGET_LIST_NUM_TARGETS = 10

#List of frequencies with their bins
FREQUENCIES = {1000:0, 1200:1, 1400:2, 1600:3}
FREQUENCY_BIN_COLORS = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1)]

//This file should be identical to the one compiled into the sender code

#ifndef COMM_PROTOCOL_H
#define COMM_PROTOCOL_H

//Reserved to indicate the beginning of a reply payload
#define REPLY_SIGNAL 0x00
#define REPLY_SIGNAL_ACK 0x02
//Reserved to indicate a status update
#define STATUS_SIGNAL 0x01
//The hex value commands begin at (reserve lower values)
#define COMMAND_BEGINNING 0x10

//Send to this address to send to all robots
#define BROADCAST_ID 255
//ID number of control radio
#define CONTROLLER_ID 1

//Listing of all commands that can be sent to the robot
typedef enum COMMAND {
  DUMP = COMMAND_BEGINNING, //Get robot config
  SET_ID,                   //Set robot's ID (0 to 255)
  VERBOSE,                  //Tell robot to send constant status updates
  SET_CONSTS,               //Set robot configuration (dump's opposite)
  SET_CONST,                //Set sepcified calibration constant to value
  STOP,                     //Shut down motors
  DRIVE,                    //Manually set motor speeds
  SET_CHANNEL,              //Set frequency beacon channel
  AUTO                      //Reset manual command overrides
} COMMAND;

//Listing of all update signals that the robot can send
typedef enum UPDATE {
  TARGET_LIST = COMMAND_BEGINNING //The list of all targets seen by the robot on a sweep
} UPDATE;

//Structs for defining form of command arguments
typedef struct DRIVE_ARGS {
  int RSpeed;
  int LSpeed;
} DRIVE_ARGS;

#endif //COMM_PROTOCOL_H

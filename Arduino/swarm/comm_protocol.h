//This file should be identical to the one compiled into the sender code

#ifndef COMM_PROTOCOL_H
#define COMM_PROTOCOL_H

//Reserved to indicate the beginning of a reply payload
#define REPLY_SIGNAL 0x00
//Reserved to indicate a status update
#define STATUS_SIGNAL 0x01
//The hex value commands begin at (reserve lower values)
#define COMMAND_BEGINNING 0x10

//Send to this address to send to all robots
#define BROADCAST_ID 255

//Listing of all commands that can be sent to the robot
typedef enum COMMAND {
  DUMP = COMMAND_BEGINNING, //Get robot config
  SET_ID,                   //Set robot's ID (0 to 255)
  VERBOSE,                  //Tell robot to send constant status updates
  SET_CONST,                //Set sepcified calibration constant to value
  STOP,                     //Shut down motors
  DRIVE,                    //Manually set motor speeds
  SET_CHANNEL,              //Set frequency beacon channel
  AUTO                      //Reset manual command overrides
} COMMAND;

#endif //COMM_PROTOCOL_H

#include "comm_protocol.h"
#include <RFM69_ATC.h>

//915MHz in the US
#define FREQUENCY RF69_915MHZ
//Network all robots must be on
#define NETWORK_ID 100

//The noise floor for automatic transmit power adjustment
#define ATC_RSSI -80

//ID number of control radio
#define CONTROLLER_ID 1

//We'll use ATC to save some battery, adjust power output automatically
RFM69_ATC radio(10,0);

void setupWireless() {
  radio.initialize(FREQUENCY, ConstData.NodeID, NETWORK_ID);
  radio.setHighPower(); //Needed for HCW models
  radio.enableAutoPower(ATC_RSSI); //Throttle transmit power automatically
}

void checkForCommands() {
  //Do we have any new packets to process?
  if (radio.receiveDone()) {
    switch (radio.DATA[0]) {
      case DUMP:
        //Send everything except the checksum
        sendResponse(radio.SENDERID, DUMP, (char*)&ConstData, sizeof(ConstData));
        break;
      case SET_CONSTS:
        //Ok, in that case the rest of the packet is the ConstData struct
        //Make sure it isn't corrupted or weird somehow
        if (radio.DATALEN-1 == sizeof(ConstData)) {
          //A bit sketchy, since radio.DATA is technically volatile.
          //Copy radio data into our struct
          memcpy(&ConstData, (char *)&(radio.DATA[1]), sizeof(ConstData));
          //Save new values to EEPROM
          saveEepromData();
        } else {
          sendResponse(radio.SENDERID, SET_CONSTS, (char *)&radio.DATALEN, sizeof(radio.DATALEN));
        }
        break;
      default:
        //Unsupported command
        break;
    }
  }
}

//Used to respond to a command requesting a response
void sendResponse(int targetId, char cmd, char * payload, int payloadLength) {
  //Prepend response header to payload
  char fullPayload[payloadLength+2];
  fullPayload[0] = REPLY_SIGNAL;
  fullPayload[1] = cmd;
  for (int i=0; i<payloadLength; i++) {
    fullPayload[i+2] = payload[i];
  }
  //Send the assembled packet
  radio.send(targetId, fullPayload, payloadLength+2, false);
}

//Used to push updates to the controller
void sendStatusUpdate(int targetId, char * payload, int payloadLength) {
  
}


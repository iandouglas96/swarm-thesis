#include "comm_protocol.h"
#include <plainRFM69.h>

//915MHz in the US
#define FREQUENCY 915
//Network all robots must be on
#define NETWORK_ID 100

//The noise floor for automatic transmit power adjustment
#define ATC_RSSI -80

//ID number of control radio
#define CONTROLLER_ID 1

#define MAX_PACKET_LENGTH 64

// slave select pin.
#define SLAVE_SELECT_PIN 10     

// connected to the reset pin of the RFM69.
#define RESET_PIN 1

// Pin DIO 2 on the RFM69 is attached to this digital pin.
#define DIO2_PIN 0

//Receive Buffer
char ReceiveBuffer[MAX_PACKET_LENGTH];
//Radio object
plainRFM69 rfm = plainRFM69(SLAVE_SELECT_PIN);

void setupWireless() {
  SPI.begin();

  bareRFM69::reset(RESET_PIN); // sent the RFM69 a hard-reset.

  rfm.setRecommended();
  //We have variable length packets, and want to use addressing.
  rfm.setPacketType(true, true);
  rfm.setNodeAddress(ConstData.NodeID);

  // allocate buffer in the library for received packets
  rfm.setBufferSize(10);      // allow buffering of up to ten packets.
  rfm.setPacketLength(64);    // maximum length of packets.

  rfm.setFrequency((uint32_t) FREQUENCY*1000*1000); // set frequency to 915 MHz.
  rfm.baud300000(); // Set the baudRate to 300000 bps

  //Enable high power transmit
  rfm.setPALevel(RFM69_PA_LEVEL_PA1_ON | RFM69_PA_LEVEL_PA2_ON, 31); 
  rfm.setOCP(0);
  rfm.setPa13dBm1(true);
  rfm.setPa13dBm2(true);

  // At higher packetrates it is necessary to increase this in order to ensure
  // packet detection at the receiving side.
  rfm.setPreambleSize(5); 

  // tell the RFM to represent whether we are in automode on DIO 2.
  rfm.setDioMapping1(RFM69_PACKET_DIO_2_AUTOMODE);

  // set pinmode to input.
  pinMode(DIO2_PIN, INPUT);

  // Tell the SPI library we're going to use the SPI bus from an interrupt.
  SPI.usingInterrupt(DIO2_PIN);

  // hook our interrupt function to any edge.
  attachInterrupt(DIO2_PIN, interrupt_RFM, CHANGE);

  // start receiving.
  rfm.receive();
}

//Interrupt handler for the radio
void interrupt_RFM(){
    rfm.poll(); // in the interrupt, call the poll function.
}

void checkForCommands() {
  //Do we have any new packets to process?
  if (rfm.available()) {
    char msgLength = rfm.read(&ReceiveBuffer);
    //First byte is the target address, which we don't need
    switch (ReceiveBuffer[1]) {
      case DUMP:
        //Send everything except the checksum
        sendResponse(254, DUMP, (char*)&ConstData, sizeof(ConstData));
        break;
      case SET_CONSTS:
        //Ok, in that case the rest of the packet is the ConstData struct
        //Make sure it isn't corrupted or weird somehow
        if (msgLength-1 == sizeof(ConstData)) {
          //A bit sketchy, since radio.DATA is technically volatile.
          //Copy radio data into our struct
          memcpy(&ConstData, (char *)&(ReceiveBuffer[1]), sizeof(ConstData));
          //Save new values to EEPROM
          saveEepromData();
          //Apply the new ID
          rfm.setNodeAddress(ConstData.NodeID);
        }
        break;
      case DRIVE:
        //Make sure our packet is max gucci
        if (msgLength-1 == sizeof(DRIVE_ARGS)) {
          ManualMode = true;
          //Cast arguments into struct for more easy access
          DRIVE_ARGS * args; 
          args = (DRIVE_ARGS*)&(ReceiveBuffer[1]);
  
          Serial.print("driving: ");
          Serial.println(args->RSpeed);
          
          setSpeeds(args->RSpeed, args->LSpeed);
        }
        break;
      case AUTO:
        ManualMode = false;
        setSpeeds(0,0);
        break;
      default:
        //Unsupported command
        break;
    }
  }
}

//Used to respond to a command requesting a response
void sendResponse(int targetId, char cmd, void * payload, int payloadLength) {
  Serial.print("sent dump: ");
  Serial.println(payloadLength);
  //Prepend response header to payload
  char fullPayload[payloadLength+2];
  fullPayload[0] = REPLY_SIGNAL;
  fullPayload[1] = cmd;
  for (int i=0; i<payloadLength; i++) {
    fullPayload[i+2] = *((char*)payload+i);
  }
  //Send the assembled packet
  rfm.sendAddressedVariable(targetId, fullPayload, payloadLength+2);
}

//Used to push updates to the controller
void sendStatusUpdate(int targetId, char updateType, void * payload, int payloadLength) {
  /*char packetNumber = 0;
  char numPackets = payloadLength/MAX_PACKET_LENGTH;
  int packetLength = 0;
  char fullPayload[MAX_PACKET_LENGTH+4];

  do {
    //Prepend update header to payload
    packetLength = min((payloadLength)-(packetNumber*MAX_PACKET_LENGTH), MAX_PACKET_LENGTH);
    fullPayload[0] = STATUS_SIGNAL;
    fullPayload[1] = updateType;
    fullPayload[2] = packetNumber;
    fullPayload[3] = numPackets;
    for (int i=0; i<packetLength; i++) {
      fullPayload[i+4] = *((char*)payload+i+(packetNumber*MAX_PACKET_LENGTH));
    }
    //Send the assembled packet
    if (radio.sendWithRetry(targetId, fullPayload, packetLength+4)) {
      packetNumber++;
    } else {
      Serial.println("packet sending failed, retry");
    }
  } while (packetLength == MAX_PACKET_LENGTH); //Keep going while we have more to transmit*/
}


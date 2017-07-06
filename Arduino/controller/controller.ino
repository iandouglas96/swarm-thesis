#include <RFM69_ATC.h>
//915MHz in the US
#define FREQUENCY RF69_915MHZ
//Network all robots must be on
#define NETWORK_ID 100

//The noise floor for automatic transmit power adjustment
#define ATC_RSSI -80

//ID number of control radio
#define CONTROLLER_ID 1

#define MAX_CMD_LENGTH 50

//We'll use ATC to save some battery, adjust power output automatically
RFM69_ATC radio(10,0,false,0);

//Buffer to hold command to send
char Command[MAX_CMD_LENGTH];
int CommandLength;

void setup() {
  //Setup serial connection to computer
  Serial.begin(9600);
  CommandLength = 0;
  
  //Setup wireless
  radio.initialize(FREQUENCY, CONTROLLER_ID, NETWORK_ID);
  radio.setHighPower(); //Needed for HCW models
  radio.enableAutoPower(ATC_RSSI); //Throttle transmit power automatically
}

void loop() {
  //Do we have any new packets to process?
  if (radio.receiveDone()) {
    Serial.print((char)radio.SENDERID);
    for (int i=0; i<radio.DATALEN; i++) {
      Serial.print((char)radio.DATA[i]);
    }
  }

  //Do we have any commands sent from the computer?
  if (Serial.available() > 0) {
    Command[CommandLength] = Serial.read();
    CommandLength++;
    //First char in the command string gives the total length
    if (CommandLength==Command[0]) {
      //We have reached the end of the command
      //Second char is the address, rest is the payload
      radio.send(Command[1], &(Command[2]), CommandLength-2, false);
      
      CommandLength = 0;
    }
  }
}


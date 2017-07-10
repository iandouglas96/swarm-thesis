#include <plainRFM69.h>
//915MHz in the US
#define FREQUENCY 915

//ID number of control radio
#define CONTROLLER_ID 1

#define MAX_PACKET_LENGTH 64

// slave select pin.
#define SLAVE_SELECT_PIN 10     

// connected to the reset pin of the RFM69.
#define RESET_PIN 1

// Pin DIO 2 on the RFM69 is attached to this digital pin.
#define DIO2_PIN 0

//Buffer to hold command to send
char Command[MAX_PACKET_LENGTH];
char ReceiveBuffer[MAX_PACKET_LENGTH];
int CommandLength;

//Radio object
plainRFM69 rfm = plainRFM69(SLAVE_SELECT_PIN);

void setup() {
  //Setup serial connection to computer
  Serial.begin(115200);
  CommandLength = 0;
  
  SPI.begin();

  bareRFM69::reset(RESET_PIN); // sent the RFM69 a hard-reset.

  rfm.setRecommended();
  //We have variable length packets, and want to use addressing.
  rfm.setPacketType(true, true);
  rfm.setNodeAddress(CONTROLLER_ID);

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

void loop() {
  //Do we have any new packets to process?
  if (rfm.available()) {
    char msgLength = rfm.read(&ReceiveBuffer);
    
    Serial.print((char)(msgLength));
    //First byte is the target address, which we don't need
    for (int i=1; i<msgLength; i++) {
      Serial.print(ReceiveBuffer[i]);
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
      char targetAddress = Command[1];
      Command[1] = CONTROLLER_ID;
      rfm.sendAddressedVariable(targetAddress, &(Command[1]), CommandLength-1);
      
      CommandLength = 0;
    }
  }
}


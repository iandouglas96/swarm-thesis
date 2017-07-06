#ifndef EEPROM_STRUCTURE_H
#define EEPROM_STRUCTURE_H

#define EEPROM_START_ADDRESS 0x00

//struct to be read/written from/to EEPROM
//Put ints at the end for alignment compatibility with Python
typedef struct EEPROM_DATA {
  //Wireless related constants
  unsigned char NodeID;

  //Do we want to send updates to controller?
  uint8_t Verbose;
  
  //Constants relating to swarm behavior
  unsigned int TargetSeparation;
  unsigned int AttractionConst;
  unsigned int RepulsionConst;
  unsigned int AngularVelocityConst;
  unsigned int LinearVelocityConst;
};

//Checksum in memory immediately after above struct
#define EEPROM_CHECKSUM_ADDRESS sizeof(EEPROM_DATA)  //Checksum
#define EEPROM_CHECKSUM_DEFAULT 0x11223344

//Default values for EEPROM
const EEPROM_DATA EEPROM_DATA_DEFAULT = {
  254,              //NodeID

  true,             //Verbose
  
  25,               //TargetSeparation
  1,                //AttractionConst
  2,                //RepulsionConst
  50,               //AngularVelocityConst
  10                //LinearVelocityConst
};

extern EEPROM_DATA ConstData;

#endif //EEPROM_STRUCTURE_H

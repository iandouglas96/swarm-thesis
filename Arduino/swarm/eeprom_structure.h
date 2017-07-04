#ifndef EEPROM_STRUCTURE_H
#define EEPROM_STRUCTURE_H

#define EEPROM_START_ADDRESS 0x00

#define EEPROM_CHECKSUM 1234

//struct to be read/written from/to EEPROM
typedef struct EEPROM_DATA {
  //Constants relating to swarm behavior
  unsigned int TargetSeparation;
  unsigned int AttractionConst;
  unsigned int RepulsionConst;
  unsigned int AngularVelocityConst;
  unsigned int LinearVelocityConst;

  //marker to see if EEPROM has been initialized
  unsigned int Checksum;
};

//Default values for EEPROM
const struct EEPROM_DATA EEPROM_DATA_DEFAULT = {
  25,               //TargetSeparation
  1,                //AttractionConst
  2,                //RepulsionConst
  50,               //AngularVelocityConst
  10,               //LinearVelocityConst

  EEPROM_CHECKSUM   //Checksum
};

extern EEPROM_DATA ConstData;

#endif //EEPROM_STRUCTURE_H

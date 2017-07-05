#include <EEPROM.h>
#include "eeprom_structure.h"

unsigned int Checksum;

void setupEepromDriver() {
  //Load EEPROM data into struct
  EEPROM.get(EEPROM_START_ADDRESS, ConstData);
  EEPROM.get(EEPROM_CHECKSUM_ADDRESS, Checksum);

  //If the checksum isn't set, then we load default values
  if (Checksum != EEPROM_CHECKSUM_DEFAULT) {
    ConstData = EEPROM_DATA_DEFAULT;
    saveEepromData();
    EEPROM.put(EEPROM_CHECKSUM_ADDRESS, Checksum);
  }
}

void saveEepromData() {
  EEPROM.put(EEPROM_START_ADDRESS, ConstData);
}


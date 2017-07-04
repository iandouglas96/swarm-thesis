#include <EEPROM.h>
#include "eeprom_structure.h"

void setupEepromDriver() {
  //Load EEPROM data into struct
  EEPROM.get(EEPROM_START_ADDRESS, ConstData);

  //If the checksum isn't set, then we load default values
  if (ConstData.Checksum != EEPROM_CHECKSUM) {
    ConstData = EEPROM_DATA_DEFAULT;
    saveEepromData();
  }
}

void saveEepromData() {
  EEPROM.put(EEPROM_START_ADDRESS, ConstData);
}


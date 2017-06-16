
/** 
 *  Set up modulated LED driver
 *  Modified from from http://shawnhymel.com/649/learning-the-teensy-lc-manual-pwm/
 *  
 *  Output on pin 6
 **/
void setupLedDriver() {
  // The order of setting the TPMx_SC, TPMx_CNT, and TPMx_MOD
  // seems to matter. You must clear _SC, set _CNT to 0, set _MOD
  // to the desired value, then you can set the bit fields in _SC.
  
  // Clear TPM0_SC register
  FTM0_SC = 0;
  
  // Reset the TPM0_CNT counter
  FTM0_CNT = 0;
  
  // Set overflow value (modulo)
  // (48 MHz) * (1 prescaler) / 38kHz = 1263 = 0x4EF
  FTM0_MOD = 0x04EF;
  
  // Set TPM0_SC register
  // Bits | Va1ue | Description
  //  8   |    0  | DMA: Disable DMA
  //  7   |    1  | TOF: Clear Timer Overflow Flag
  //  6   |    1  | TOIE: Enable Timer Overflow Interrupt
  //  5   |    0  | CPWMS: TPM in up counting mode
  // 4-3  |   01  | CMOD: Counter incrememnts every TPM clock
  // 2-0  |  000  | PS: Prescale = 1
  FTM0_SC = 0b011001000;
  
  // Set TPM0_C4SC register (Teensy LC - pin 6)
  // As per the note on p. 575, we must disable the channel
  // first before switching channel modes. We also introduce
  // a magical 1 us delay to allow the new value to take.
  // Bits | Va1ue | Description
  //  7   |    1  | CHF: Clear Channel Flag
  //  6   |    0  | CHIE: Disable Channel Interrupt
  // 5-4  |   10  | MS: Edge-aligned PWM
  // 3-2  |   00  | ELS: Set on reload, clear on match
  //  1   |    0  | Reserved
  //  0   |    0  | DMA: Disable DMA
  FTM0_C4SC = 0;
  delayMicroseconds(1);
  FTM0_C4SC = 0b10101000;
  
  // Set PWM value (0 - 65535) to TPM0_C4V
  // Set to overflow over 2: 50% duty cycle
  FTM0_C4V = FTM0_MOD / 2;
}

//Turn on or off the modulated IR led
void setBeacon(bool on) {
  if (on) {
    // Set PORTD_PCR4 register (Teensy LC - pin 6)
    // Set mux to 4: FTM0_CH4 output
    *portConfigRegister(6) = PORT_PCR_MUX(4);
  } else {
    *portConfigRegister(6) = PORT_PCR_MUX(0);
  }
}

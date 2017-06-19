/**
* Simple library to manage a stepper motor controlled by a Pololu Allegro A4988 stepper driver
* or similar
*/

// ensure this library description is only included once
#ifndef PololuStepper_h
#define PololuStepper_h

#include "Arduino.h"

#define MIN_STEP_INTERVAL_US	5
#define COUNT_OVERFLOW			1024

class PololuStepper {
	public:
		//Create a new Stepper motor
		PololuStepper(int, int);
		//Run motor at a given speed
		void setSpeed(int);
		//Get the current motor speed
		int getSpeed(void);
		//Needs to be called regularly
		void step(void);

	private:
		//The current motor speed
		int period;
		int stepPin, dirPin;
		//Possible step() will get called from interrupt context
		volatile int cnt;
};

#endif //PololuStepper_h
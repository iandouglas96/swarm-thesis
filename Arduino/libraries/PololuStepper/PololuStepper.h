/**
* Simple library to manage a stepper motor controlled by a Pololu Allegro A4988 stepper driver
* or similar
*/

// ensure this library description is only included once
#ifndef PololuStepper_h
#define PololuStepper_h

#include "IntervalTimer.h"

#define MIN_STEP_INTERVAL_US	5
#define COUNT_OVERFLOW			255

class PololuStepper {
	public:
		//Create a new Stepper motor
		PololuStepper(int, int);
		//Run motor at a given speed
		void setSpeed(int, int);
		//Get the current motor speed
		int getSpeedRight(void);
		int getSpeedLeft(void);

	private:
		//Counter used by step function
		static volatile unsigned int cnt;
		//The current motor speed
		int speed_r;
		int speed_l;
		//Timer to drive steps
		IntervalTimer timer;
		int stepPin;
		int dirPin;

		//Method called by timer
		static void step(void);
};

#endif //PololuStepper_h
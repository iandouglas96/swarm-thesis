#include "PololuStepper.h"

//Constructor, instantiate the stepper, set up timer, etc.
PololuStepper::PololuStepper(int stepPin, int dirPin) {
	cnt = 0;

	this->stepPin = stepPin;
	this->dirPin = dirPin;

	//Intermediate priority.  We want decent timing, but doesn't have to be great
	this->timer.priority(125);
	this->timer.begin(step, MIN_STEP_INTERVAL_US);
}

static void step(void) {
	cnt++;
	if (cnt > COUNT_OVERFLOW) {
		cnt = 0;
	}
}
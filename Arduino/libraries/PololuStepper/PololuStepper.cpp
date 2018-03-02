#include "PololuStepper.h"

//Constructor, instantiate the stepper, set up timer, etc.
PololuStepper::PololuStepper(int stepPin, int dirPin) {
	this->stepPin = stepPin;
	this->dirPin = dirPin;

	pinMode(stepPin, OUTPUT);
	pinMode(dirPin, OUTPUT);

	//Start stopped
	period = 0;
}

//Run motor at a given speed
void PololuStepper::setSpeed(int speed ) {
	//Special case for being stopped
	if (speed == 0) {
		period = 0;
		return;
	}

	//Set the speed
	period = COUNT_OVERFLOW / abs(speed);

	//Set the current direction
	if (speed > 0) {
		digitalWrite(dirPin, HIGH);
	}
	else {
		digitalWrite(dirPin, LOW);
	}
}

//Get the current motor speed
//Note: due to rounding error, may not return the exact value
//	given originally to setSpeed()
int PololuStepper::getSpeed(void) {
    if (period == 0) {
        return 0;
    } else if (digitalRead(dirPin)) {
        return (COUNT_OVERFLOW / period);
    } else {
        return -(COUNT_OVERFLOW / period);
    }
}

//This function should be regularly called at some set frequency
//(probably an interrupt of some sort)
void PololuStepper::step(void) {
	if (period != 0) {
		cnt++;
		if (cnt >= COUNT_OVERFLOW) {
			cnt = 0;
		}
		if (cnt % period == 0) {
			digitalWrite(stepPin, !digitalRead(stepPin));
		}
	}
}

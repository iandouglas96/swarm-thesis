#include <PololuStepper.h>

//Pin definitions
#define STEPPER_PIN_STEP_R 23
#define STEPPER_PIN_STEP_L 22
#define STEPPER_PIN_DIR_R 21
#define STEPPER_PIN_DIR_L 20

//Timer period (in us)
#define STEPPER_TIMER_PERIOD 100
//Timer priority (out of 255.  Use lowish priority, since not that timing critical)
#define STEPPER_TIMER_PRIORITY 145

//R and L stepper controller objects
PololuStepper StepperR(STEPPER_PIN_STEP_R,STEPPER_PIN_DIR_R);
PololuStepper StepperL(STEPPER_PIN_STEP_L,STEPPER_PIN_DIR_L);

IntervalTimer StepperTimer;

//Configure the stepper timings
void setupSteppers() {
  StepperTimer.begin(timerStep, STEPPER_TIMER_PERIOD);
  StepperTimer.priority(STEPPER_TIMER_PRIORITY);
}

//Set the speeds of both steppers.
void setSpeeds(int speedR, int speedL) {
  StepperR.setSpeed(speedR);
  StepperL.setSpeed(speedL);
}

//Call the step() functions at regular timing interval (defined by IntervalTimer)
void timerStep() {
  StepperR.step();
  StepperL.step();
}


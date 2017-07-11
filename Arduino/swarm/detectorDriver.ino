#include <Audio.h>
#include <PWMServo.h>

PWMServo servo;

AudioInputAnalogStereo   adcs1(A2, A3);           
AudioAnalyzeFFT1024      fft[2];     
AudioConnection          patchCord1(adcs1, 0, fft[0], 0);
AudioConnection          patchCord2(adcs1, 1, fft[1], 0);

//Top of noise floor
#define DETECTOR_FLOOR 0.02
//Minimum height of peak
#define MIN_PEAK_HEIGHT 0.07

//Number of degrees servo lags behind stated value (experimentally determined)
#define SERVO_LAG_COMP 8
#define SERVO_SPEED 2

//Define the location of bins on the FFT
#define NUM_FREQ_BINS 2
const int FREQ_BINS[NUM_FREQ_BINS] = {23, 28};
//Array to keep track of the last values in each bin (for peak detection).  2d array for each fft
float LastMagnitude[NUM_FREQ_BINS];
//Starting magnitude of a peak
float PeakDetected[NUM_FREQ_BINS];

float RawData[360/SERVO_SPEED][NUM_FREQ_BINS];

//Current position of servo (degrees)
int pos;
//Direction the servo is moving (+- 1)
int dir;

//Number of targets detected
int NumTargets;
//Array of targets detected (dynamic array)
TARGET TargetsInProgress[MAX_TARGETS];

//Clear arrays to prepare for next scan
//IMPORTANT: Must be manually called after targetScan returns something
void resetScan() {
  //Clear magnitudes to 0
  for (int i=0; i<MAX_TARGETS; i++) {
    TargetsInProgress[i].magnitude = 0;
  }
  for (int i=0; i<NUM_FREQ_BINS; i++) {
    PeakDetected[i] = 0;
    LastMagnitude[i] = 0;
  }

  NumTargets = 0;
}

void setupDetector() {
  //FFT requires Audio memory to be allocated for Audio Library
  //Testing shows that the maximum usage is 18, we'll give a couple extra just in case
  AudioMemory(20);
  //Servo on pin 3
  //Note that pin 3 is on FTM1, so it doesn't interfere with the IR PWM, which is on FTM0
  servo.attach(3);
  //Initialize globals
  pos = 0;
  dir = 1;

  resetScan();
}

TARGET * targetScan() {
  // Have we completed scanning a bin?
  if (fft[0].available() && fft[1].available()) {   
    //For debugging
    //Serial.println(fft[0].read(22,24));

    //Store data
    for (int i=0; i<NUM_FREQ_BINS; i++) {
      RawData[pos/SERVO_SPEED][i] = fft[0].read(FREQ_BINS[i]-1,FREQ_BINS[i]+1);
      RawData[(pos+180)/SERVO_SPEED][i] = fft[1].read(FREQ_BINS[i]-1,FREQ_BINS[i]+1);
    }
    
    pos += SERVO_SPEED*dir;
    //Move servo to next location (compensate for servo lag)
    servo.write(180-(pos+(SERVO_LAG_COMP*dir)));

    if (pos > (180-SERVO_SPEED) || pos < SERVO_SPEED) {
      //Get ready for next scan
      dir *= -1;
      parseScan();
      return TargetsInProgress;
    }
  }
  return NULL;
}

void parseScan() {
  //Scan through each bin
  for (int angle=0; angle<260; angle += SERVO_SPEED) {
    for (int i=0; i<NUM_FREQ_BINS; i++) {
      float binMag = RawData[angle/SERVO_SPEED][i];
      //Do we have a peak?
      if (binMag > DETECTOR_FLOOR && binMag >= LastMagnitude[i] && PeakDetected[i]==0) {
        //We are going up a peak
        PeakDetected[i] = binMag;
      } else if (binMag < LastMagnitude[i] && PeakDetected[i]!=0 && LastMagnitude[i]-PeakDetected[i] > MIN_PEAK_HEIGHT) {
        TargetsInProgress[NumTargets].magnitude = LastMagnitude[i]-PeakDetected[i];
        TargetsInProgress[NumTargets].direction = angle;
        TargetsInProgress[NumTargets].bin = i;
        //We just started going down the peak
        PeakDetected[i] = 0;
        if (NumTargets < MAX_TARGETS-1) {
          NumTargets++;
        }
      }
      LastMagnitude[i] = binMag;
    }
  }
}


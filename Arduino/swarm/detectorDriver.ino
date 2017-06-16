#include <Audio.h>
#include <PWMServo.h>

PWMServo servo;

AudioInputAnalogStereo   adcs1(A2, A3);           
AudioAnalyzeFFT1024      fft[2];     
AudioConnection          patchCord1(adcs1, 0, fft[0], 0);
AudioConnection          patchCord2(adcs1, 1, fft[1], 0);

//Define the location of bins on the FFT
#define NUM_FREQ_BINS 2
const int FREQ_BINS[NUM_FREQ_BINS] = {23, 28};
//Array to keep track of the last values in each bin (for peak detection).  2d array for each fft
float LastMagnitude[2][NUM_FREQ_BINS];
//Boolean (true if we are _ascending_ a peak) 2d array for each fft
bool PeakDetected[2][NUM_FREQ_BINS];
//Minimum peak height
#define DETECTOR_FLOOR 0.05

//Number of degrees servo lags behind stated value (experimentally determined)
#define SERVO_LAG_COMP 6
#define SERVO_SPEED 2
//Current position of servo (degrees)
int pos;
//Amount to move servo each FFT (degrees)
unsigned int inc;
//Direction the servo is moving (+- 1)
int dir;

//Number of targets detected
int NumTargets[2];
//Array of targets detected (dynamic array)
struct TARGET TargetsInProgress[MAX_TARGETS];

//Clear arrays to prepare for next scan
//IMPORTANT: Must be manually called after targetScan returns something
void resetScan() {
  //Clear magnitudes to 0
  for (int i=0; i<MAX_TARGETS; i++) {
    TargetsInProgress[i].magnitude = 0;
  }
  for (int side=0; side<2; side++) {
    for (int i=0; i<NUM_FREQ_BINS; i++) {
      PeakDetected[side][i] = false;
      LastMagnitude[side][i] = 0;
    }
  }
  NumTargets[0]=0;
  NumTargets[1]=MAX_TARGETS/2;
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

struct TARGET * targetScan() {
  // Have we completed scanning a bin?
  if (fft[0].available() && fft[1].available()) {   
    //For debugging
    //Serial.println(fft[0].read(22,24));

    //Check each fft, one for each "side".  If side=1, add 180 to the direction
    for (int side=0; side<2; side++) {
      //Scan through each bin
      for (int i=0; i<NUM_FREQ_BINS; i++) {
        float binMag = fft[side].read(FREQ_BINS[i]-1,FREQ_BINS[i]+1);
        //Do we have a peak?
        if (binMag > DETECTOR_FLOOR && binMag > LastMagnitude[side][i]) {
          //We are going up a peak
          PeakDetected[side][i] = true;
          TargetsInProgress[NumTargets[side]].magnitude = binMag;
          TargetsInProgress[NumTargets[side]].direction = (side==0 ? pos : pos+180);
          TargetsInProgress[NumTargets[side]].bin = i;
        } else if (binMag < LastMagnitude[side][i] && PeakDetected[side][i]==true) {
          //We just started going down the peak
          PeakDetected[side][i] = false;
          NumTargets[side]++;
        }
        LastMagnitude[side][i] = binMag;
      }
    }

    pos += SERVO_SPEED*dir;
    //Move servo to next location (compensate for servo lag)
    servo.write(pos+(SERVO_LAG_COMP*dir));

    if (pos > (180-SERVO_SPEED) || pos < SERVO_SPEED) {  
      //Get ready for next scan
      dir *= -1;
      return TargetsInProgress;
    }
  }
  return NULL;
}


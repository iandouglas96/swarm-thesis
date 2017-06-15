#include <Audio.h>
#include <PWMServo.h>

PWMServo servo;

AudioInputAnalog         adc1(A2);           
AudioAnalyzeFFT1024      fft_1;      
AudioConnection          patchCord1(adc1, fft_1);

//Define the location of bins on the FFT
#define NUM_FREQ_BINS 2
const int FREQ_BINS[NUM_FREQ_BINS] = {23, 28};
//Array to keep track of the last values in each bin (for peak detection)
float LastMagnitude[NUM_FREQ_BINS];
//Boolean (true if we are _ascending_ a peak)
bool PeakDetected[NUM_FREQ_BINS];
//Minimum peak height
#define DETECTOR_FLOOR 0.05

//Number of degrees servo lags behind stated value
#define SERVO_LAG_COMP 6
#define SERVO_SPEED 2
//Current position of servo (degrees)
int pos;
//Amount to move servo each FFT (degrees)
unsigned int inc;
//Direction the servo is moving (+- 1)
int dir;

//Number of targets detected
int NumTargets;
//Array of targets detected (dynamic array)
struct TARGET TargetsInProgress[MAX_TARGETS];

//Clear arrays to prepare for next scan
//IMPORTANT: Must be manually called after targetScan returns something
void resetScan() {
  //Clear magnitudes to 0
  for (int i=0; i<MAX_TARGETS; i++) {
    TargetsInProgress[i].magnitude = 0;
  }
  for (int i=0; i<NUM_FREQ_BINS; i++) {
    PeakDetected[i] = false;
    LastMagnitude[i] = 0;
  }

  NumTargets = 0;
}

void setupDetector() {
  //FFT requires Audio memory to be allocated for Audio Library
  AudioMemory(12);
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
  if (fft_1.available()) {   
    //For debugging
    //Serial.println(fft_1.read(22,24));

    //Scan through each bin
    for (int i=0; i<NUM_FREQ_BINS; i++) {
      float binMag = fft_1.read(FREQ_BINS[i]-1,FREQ_BINS[i]+1);
      //Do we have a peak?
      if (binMag > DETECTOR_FLOOR && binMag > LastMagnitude[i]) {
        //We are going up a peak
        PeakDetected[i] = true;
        TargetsInProgress[NumTargets].magnitude = binMag;
        TargetsInProgress[NumTargets].direction = pos;
        TargetsInProgress[NumTargets].bin = i;
      } else if (binMag < LastMagnitude[i] && PeakDetected[i]==true) {
        //We just started going down the peak
        PeakDetected[i] = false;
        NumTargets++;
      }
      LastMagnitude[i] = binMag;
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


#include <Audio.h>
#include <PWMServo.h>

PWMServo servo;

AudioInputAnalogStereo   adcs1(A2, A3);           
AudioAnalyzeFFT1024      fft[2];     
AudioConnection          patchCord1(adcs1, 0, fft[0], 0);
AudioConnection          patchCord2(adcs1, 1, fft[1], 0);

//Top of noise floor
#define DETECTOR_FLOOR 0.03
//Width of peak (must be odd)
#define MIN_PEAK_WIDTH 5

//Number of degrees servo lags behind stated value (experimentally determined)
#define SERVO_LAG_COMP 8
#define SERVO_SPEED 2
#define SERVO_SCALE_FACTOR 0.95

//Define the location of bins on the FFT
#define NUM_FREQ_BINS 2
const int FREQ_BINS[NUM_FREQ_BINS] = {23, 28};

float RawData[(360/SERVO_SPEED)+1][NUM_FREQ_BINS];

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
      RawData[pos/SERVO_SPEED][i] = fft[0].read(FREQ_BINS[i]);
      RawData[(pos+180)/SERVO_SPEED][i] = fft[1].read(FREQ_BINS[i]);
    }
    
    pos += SERVO_SPEED*dir;
    //Move servo to next location (compensate for servo lag)
    servo.write((180-(pos+(SERVO_LAG_COMP*dir)))*SERVO_SCALE_FACTOR);

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
  for (int freq=0; freq<NUM_FREQ_BINS; freq++) {
    for (int angle=0; angle<360; angle += SERVO_SPEED) {
      int binNum = angle/SERVO_SPEED;
      float bin = RawData[binNum][freq];
      //Are we above the noise floor?

      if (freq==0) {
        Serial.println(bin);
      }
      
      if (bin > DETECTOR_FLOOR) {
        bool isPeak = true;
        float sum = 0;
        float lastVal = 0;
        for (int i=-(MIN_PEAK_WIDTH-1)/2; i<=(MIN_PEAK_WIDTH-1)/2; i++) {
          int nearBinNum = binNum+i;
          //Handle wrapping
          if (nearBinNum > 360/SERVO_SPEED) nearBinNum -= 360/SERVO_SPEED;
          else if (nearBinNum < 0) nearBinNum += 360/SERVO_SPEED;
          if (RawData[nearBinNum][freq] > bin || 
             (RawData[nearBinNum][freq]+DETECTOR_FLOOR < lastVal && i < 0) ||
             (RawData[nearBinNum][freq]-DETECTOR_FLOOR > lastVal && i > 0)) {
            isPeak = false;
          } else {
            sum += RawData[nearBinNum][freq];
          }

          lastVal = RawData[nearBinNum][freq];
        }

        if (isPeak) {
          //We have a peak!
          TargetsInProgress[NumTargets].magnitude = sum;
          TargetsInProgress[NumTargets].direction = angle;
          TargetsInProgress[NumTargets].bin = freq; 
          if (NumTargets < MAX_TARGETS - 1) {
            NumTargets++;
          }
        }
      }
    }
  }
}


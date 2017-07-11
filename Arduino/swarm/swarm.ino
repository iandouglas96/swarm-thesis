#include "eeprom_structure.h"
#include "comm_protocol.h"

//The maximum number of trackable targets each robot can see
#define MAX_TARGETS 10
//Struct defining information about a target (another robot)
typedef struct TARGET {
  float magnitude;
  short int direction;
  short int bin;
};

//Config stored in EEPROM
EEPROM_DATA ConstData;

//true if we want to control robot directly from computer
boolean ManualMode;

TARGET targets[MAX_TARGETS];

void setup() {
  Serial.begin(115200);
  Serial.println("Starting up...");

  ManualMode = true;

  setupEepromDriver();
  setupDetector();
  setupLedDriver();
  setupWireless();
  setupSteppers();
  
  //start up at 1kHz
  setBeacon(1000);
  //Start up stationary
  setSpeeds(0,0);
}

void loop() {
  //Repeating commands
  TARGET * newTargets = targetScan();
  if (newTargets != NULL) {
    //We have seen something, let's now act accordingly
    printTargets(newTargets);
    if (!ManualMode) {
      //If we aren't being controlled externally, act according to sensory input
      processTargets(newTargets);
    }
    resetScan();
  }
  checkForCommands();
}

//Generate force vector based on target locations
void processTargets(TARGET targets[MAX_TARGETS]) {
  float forcefwd = 0;
  float forceside = 0;
  for (int i=0; i<MAX_TARGETS; i++) {
    //Look at all bins
    if (targets[i].magnitude != 0) {
      //Nonzero magnitude means this is a real thing
      //Convert magnitude to cm
      float dist = magToCm(targets[i].magnitude);
      //Note: repulsion is considered negative
      float force_mag = 0;

      if (dist > ConstData.TargetSeparation) {
        //attraction
        force_mag = (dist-ConstData.TargetSeparation)*ConstData.AttractionConst;
      } else if (dist < ConstData.TargetSeparation) {
        //repulsion
        force_mag = (dist-ConstData.TargetSeparation)*ConstData.RepulsionConst;
      }

      //Get x and y force components so they can be added.  Convert angle to radians first
      forcefwd += force_mag*cos(targets[i].direction*0.01745);
      forceside += force_mag*sin(targets[i].direction*0.01745);
    }
  }

  /*Serial.print("force: ");
  Serial.print(forcefwd);
  Serial.print(", ");
  Serial.println(forceside);*/

  calcMovement(forcefwd, forceside);
}

//for debugging purposes
void printTargets(TARGET targets[MAX_TARGETS]) {
  if (ConstData.Verbose) {
    //Send the target list via comm link
    sendStatusUpdate(CONTROLLER_ID, TARGET_LIST, targets, sizeof(TARGET)*MAX_TARGETS);
  }
  
  for (int i=0; i<MAX_TARGETS; i++) {
    Serial.print(targets[i].magnitude);
    Serial.print(", ");
    Serial.print(targets[i].direction);
    Serial.print(", ");
    Serial.print((int)targets[i].bin);
    Serial.print(", ");
  }
  Serial.println();
}

//Convert force vector to speed commands for motor drivers
void calcMovement(float forcefwd, float forceside) {
  if (forcefwd != 0 || forceside != 0) {
    //Go back to circular coordinates
    //1.5708 rad = 90 degrees, to make 0 degrees be forwards
    float force_angle = 1.5708-atan2(forcefwd, forceside);
    float force_mag = sqrt(forcefwd*forcefwd + forceside*forceside);
  
    //difference should be +- 90 degrees, since we can reverse
    while (force_angle > 1.5708) {
      force_angle -= 3.1416;
      force_mag *= -1;
    }
    while (force_angle < -1.5708) {
      force_angle += 3.1416;
      force_mag *= -1;
    }
  
    int angularv = (int)(ConstData.AngularVelocityConst * force_angle);
    int linearv = (int)(ConstData.LinearVelocityConst * force_mag * cos(force_angle));
  
    /*Serial.println(force_angle);
    Serial.print("move: ");
    Serial.print(angularv);
    Serial.print(", ");
    Serial.println(linearv);*/

    setSpeeds(linearv-angularv,linearv+angularv);
  } else {
    //stop
    setSpeeds(0,0);
  }
}

//Convert FFT magnitude values to distances.
double magToCm(float magnitude) {
  //empirically determined calibration curve
  return -log(magnitude*0.9022)*20;
}

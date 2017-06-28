//The maximum number of trackable targets each robot can see
#define MAX_TARGETS 10
//Struct defining information about a target (another robot)
struct TARGET {
  float magnitude;
  int direction;
  int bin;
};

//Constants relating to swarm behavior
#define TARGET_SEPARATION 25
#define ATTRACTION_CONST 1
#define REPULSION_CONST 1

void setup() {
  Serial.begin(9600);
  Serial.println("Starting up...");

  setupDetector();
  setupLedDriver();
  setupSteppers();
  
  //start up at 1kHz
  setBeacon(1000);
  //Start up stationary
  setSpeeds(0,0);
}

void loop() {
  //Repeating commands
  struct TARGET * newTargets = targetScan();
  if (newTargets != NULL) {
    //We have seen something, let's now act accordingly
    printTargets(newTargets);
    processTargets(newTargets);
    resetScan();
  }
  delay(1);
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

      if (dist > TARGET_SEPARATION) {
        //attraction
        force_mag = (dist-TARGET_SEPARATION)*ATTRACTION_CONST;
      } else if (dist < TARGET_SEPARATION) {
        //repulsion
        force_mag = (dist-TARGET_SEPARATION)*REPULSION_CONST;
      }

      //Get x and y force components.  Convert angle to radians first
      forcefwd += force_mag*cos(targets[i].direction*0.01745);
      forceside += force_mag*sin(targets[i].direction*0.01745);
    }
  }

  calcMovement(forcefwd, forceside);
}

//for debugging purposes
void printTargets(TARGET targets[MAX_TARGETS]) {
  for (int i=0; i<MAX_TARGETS; i++) {
    Serial.print(targets[i].magnitude);
    Serial.print(", ");
    Serial.print(targets[i].direction);
    Serial.print(", ");
    Serial.print(targets[i].bin);
    Serial.print(", ");
  }
  Serial.println();
}

//Convert force vector to speed commands for motor drivers
void calcMovement(float forcefwd, float forceside) {
  Serial.print(forcefwd);
  Serial.print(", ");
  Serial.println(forceside);
}

//Convert FFT magnitude values to distances.
double magToCm(float magnitude) {
  //empirically determined calibration curve
  return -log(magnitude*0.9022)*20;
}

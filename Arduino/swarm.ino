//The maximum number of trackable targets each robot can see
#define MAX_TARGETS 10
//Struct defining information about a target (another robot)
struct TARGET {
  float magnitude;
  int direction;
  int bin;
};
void setup() {
  Serial.begin(9600);
  Serial.println("Starting up...");

  setupDetector();
  
  setupLedDriver();
  setBeacon(true);
}

void loop() {
  //Repeating commands
  struct TARGET * newTargets = targetScan();
  if (newTargets != NULL) {
    //We have a new set of targets!  Copy them into the permanent buffer
    for (int i=0; i<MAX_TARGETS; i++) {
      Serial.print(newTargets[i].magnitude);
      Serial.print(", ");
      Serial.print(newTargets[i].direction);
      Serial.print(", ");
      Serial.print(newTargets[i].bin);
      Serial.print(", ");
    }
    Serial.println();

    //This must be called on a completed scan after the copy completes
    resetScan();
  }
  delay(1);
}

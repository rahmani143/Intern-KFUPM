#include <AccelStepper.h>
#include <ezButton.h>

// Stepper pins (DM542T connections)
#define PULSE_PIN 9   // STEP to DM542T PUL+
#define DIR_PIN 8     // DIR to DM542T DIR+
AccelStepper stepper(AccelStepper::DRIVER, PULSE_PIN, DIR_PIN);

// Limit switches
ezButton leftSwitch(7);   // Left limit switch (position 0)
ezButton rightSwitch(6);  // Right limit switch (max position)

// Position tracking
long maxPosition = 2176;   // Your calibrated maximum steps
bool systemHomed = false;

void setup() {
  Serial.begin(9600);
  
  // Initialize limit switches with internal pull-ups
  leftSwitch.setDebounceTime(50);
  rightSwitch.setDebounceTime(50);
  
  // Configure stepper motor parameters (from DM542T manual [7.1-7.2.2])
  stepper.setMaxSpeed(1000);     // 1000 steps/sec (adjust based on mechanical limits)
  stepper.setAcceleration(500);  // Smooth acceleration (steps/sec²)
  
  homeSystem();  // Begin automatic homing sequence
}

void homeSystem() {
  Serial.println("Homing system...");
  
  // Phase 1: Move left until left switch is triggered
  while(leftSwitch.getState() == HIGH) {
    leftSwitch.loop();
    stepper.moveTo(-100000);  // Large negative value for continuous movement
    stepper.run();
  }
  
  stepper.stop();
  stepper.setCurrentPosition(0);
  Serial.println("Homed to position 0");
  
  // Phase 2: Find maximum position
  findMaxPosition();
}

void findMaxPosition() {
  Serial.println("Finding maximum position...");
  
  // Move right until right switch is triggered
  while(rightSwitch.getState() == HIGH) {
    rightSwitch.loop();
    stepper.moveTo(100000);  // Large positive value for continuous movement
    stepper.run();
    
    // Update max position tracking
    if(stepper.currentPosition() > maxPosition) {
      maxPosition = stepper.currentPosition();
    }
  }
  
  stepper.stop();
  stepper.setCurrentPosition(maxPosition);
  systemHomed = true;
  Serial.print("Max position found: ");
  Serial.println(maxPosition);
  Serial.println("System ready. Send positions 0.0-1.0 via Serial Monitor");
}

void loop() {
  leftSwitch.loop();
  rightSwitch.loop();
  
  if(systemHomed) {
    handleSerialInput();
    //stepper.run();
    
    // Safety constraints
    //if(stepper.targetPosition() < 0) stepper.stop();
    //stepper.moveTo(0)
    //if(stepper.targetPosition() > maxPosition) stepper.stop();
    //stepper.moveTo(maxPosition)
  }
}

union {
  byte bytes[4];
  float value;
} floatUnion;

void handleSerialInput() {
  float input = -1.0;
  bool validInput = false;

  Serial.println("Enter position (0.0 - 1.0):");

  while (!validInput) {
    if (Serial.available() >= 4) {  // Wait for 4 bytes (size of float)
      // Read 4 bytes into the union
      for (int i = 0; i < 4; i++) {
        floatUnion.bytes[i] = Serial.read();
      }
      
      input = floatUnion.value;
      if (input >= 0.0 && input <= 1.0) {
        validInput = true;
      } else {
        Serial.print("Invalid input: ");
        Serial.print(input, 3);
        Serial.println("! Enter value between 0.0-1.0:");
      }
    }
    leftSwitch.loop();
    rightSwitch.loop();
  }
  moveToNormalized(input);
}



void moveToNormalized(float position) {
  long targetSteps = round(position * maxPosition);
  stepper.moveTo(targetSteps);
  
  Serial.print("Moving to: ");
  Serial.print(position * 100, 1);
  Serial.print("% (");
  Serial.print(targetSteps);
  Serial.println(" steps)");
  //stepper.stop();

  while(stepper.distanceToGo() != 0) {
    stepper.run();
    leftSwitch.loop();
    rightSwitch.loop();
  }
  delay(1500);

  
}

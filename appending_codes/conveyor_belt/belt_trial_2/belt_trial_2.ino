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
  stepper.setMaxSpeed(100);     // 1000 steps/sec (adjust based on mechanical limits)
  stepper.setAcceleration(500);  // Smooth acceleration (steps/sec²)
  
  homeSystem();  // Begin automatic homing sequence
}

void homeSystem() {
  Serial.println("Homing system...");
  stepper.moveTo(-100000);  // Large negative value for continuous movement
    
  // Phase 1: Move left until left switch is triggered
  while(leftSwitch.getState() == HIGH) {
    leftSwitch.loop();
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
  stepper.moveTo(100000);  // Large positive value for continuous movement
    
  // Move right until right switch is triggered
  while(rightSwitch.getState() == HIGH) {
    rightSwitch.loop();
    stepper.run();   
  }
  // Update max position tracking
  stepper.stop();  
  maxPosition = stepper.currentPosition();
  
  systemHomed = true;
  Serial.print("Max position found: ");
  Serial.println(maxPosition);
  Serial.println("System ready. Send position and speed via Serial Monitor");
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

// void handleSerialInput() {
//   float input = -1.0;
//   int speedValue = 0;
//   bool validInput = false;

//   Serial.println("Enter position (0-255) and speed (50-1000): ");

//   while (!validInput) {
//     // Wait for 3 bytes: 1 (position) + 2 (speed)
//     if (Serial.available() >= 3) {  
//       uint8_t posByte = Serial.read();  // Read position byte
//       uint8_t speedLow = Serial.read(); // Speed low byte
//       uint8_t speedHigh = Serial.read();// Speed high byte
      
//       // Combine speed bytes into 16-bit integer
//       speedValue = (speedHigh << 8) | speedLow;
//       input = posByte / 255.0;  // Convert position to 0.0–1.0

//       // Validate inputs
//       if (input >= 0.0 && input <= 1.0 && speedValue >= 50 && speedValue <= 1000) {
//         validInput = true;
//         Serial.print("Position: "); Serial.print(input, 3);
//         Serial.print(", Speed: "); Serial.println(speedValue);
//       } else {
//         Serial.println("Invalid data! Resend values");
//       }
//     }
//     leftSwitch.loop();
//     rightSwitch.loop();

//     // In handleSerialInput():
//   if (Serial.available() >= 3) {
//   uint8_t posByte = Serial.read();
//   uint8_t speedLow = Serial.read();
//   uint8_t speedHigh = Serial.read();
  
//   // Speed reconstruction (little-endian)
//   int speedValue = (speedHigh << 8) | speedLow;  // Should be (0 << 8) | 50 = 50
//   }
//   }

void handleSerialInput() {
  float input = -1.0;
  int speedValue = 0;
  bool validInput = false;

  Serial.println("Enter position (0-255) and speed (50-1000): ");

  while (!validInput) {
    if (Serial.available() >= 3) {  
      uint8_t posByte = Serial.read();
      uint8_t speedLow = Serial.read();
      uint8_t speedHigh = Serial.read();
      
      speedValue = (speedHigh << 8) | speedLow;
      input = posByte / 255.0;

      // Accept speed=0 as "no change"
      if (input >= 0.0 && input <= 1.0 && ((speedValue == 0) || (speedValue >= 50 && speedValue <= 1000))) {
        validInput = true;
        
        if (speedValue >= 50 && speedValue <= 1000) {
          stepper.setMaxSpeed(speedValue);
          Serial.print("Speed set to: "); Serial.println(speedValue);
        } else if (speedValue == 0) {
          Serial.println("Speed unchanged.");
        }
        
        Serial.print("Position: "); Serial.println(input, 3);
      } else {
        Serial.println("Invalid data! Resend values");
      }
    }
    leftSwitch.loop();
    rightSwitch.loop();
  }

  moveToNormalized(input);
}





void moveToNormalized(float position) {
  long targetSteps = round(position * maxPosition);
  Serial.print("Moving to: ");
  Serial.print(position * 100, 1);
  Serial.print("% (");
  Serial.print(targetSteps);
  Serial.print(" steps) at speed ");
  Serial.print(stepper.maxSpeed());
  Serial.println(" steps/sec");

  stepper.moveTo(targetSteps);

  while(stepper.distanceToGo() != 0) {
    stepper.run();
    leftSwitch.loop();
    rightSwitch.loop();
  }
  delay(1500);
}


#include <AFMotor.h>

// Define the motor shield object
AF_DCMotor motor1(1); // Motor connected to M1
AF_DCMotor motor2(2); // Motor connected to M2
AF_DCMotor motor3(3); // Motor connected to M3
AF_DCMotor motor4(4); // Motor connected to M4

char command;

void setup() {
  
  Serial1.begin(9600); 
  Serial1.println("Motor test!");

  // Set the speed of the motors
  motor1.setSpeed(255);
  motor2.setSpeed(255);
  motor3.setSpeed(255);
  motor4.setSpeed(255);
}

void loop() {
  // Check for incoming commands from Python
  if (Serial1.available() > 0) {
    command = Serial1.read();
    Serial1.print("Received command: ");
    Serial1.println(command);
    executeCommand(command);
  }
}

void executeCommand(char command) {
  switch (command) {
    case 'F':
      forward();
      break;
    case 'B':
      backward();
      break;
    case 'L':
      left();
      break;
    case 'R':
      right();
      break;
    case 'S':
      stopMotors();
      break;
    default:
      break;
  }
}

void forward() {
  Serial1.println("Moving forward");
  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}

void backward() {
  Serial1.println("Moving backward");
  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
}

void left() {
  Serial1.println("Turning left");
  motor1.run(BACKWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}

void right() {
  Serial1.println("Turning right");
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(FORWARD);
}

void stopMotors() {
  Serial1.println("Stopping motors");
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
}

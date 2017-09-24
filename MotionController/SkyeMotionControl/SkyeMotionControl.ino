/**********************************
   SKYE Motion Control for RomeoV2
   Version 1.0
   Author: Stephen Mylabathula
   Last Edited: 7/25/2016
 **********************************/

/*************************
  Motor Control Codes:

  0000 - Stop
  0001 - Forward Fast
  0010 - Forward Medium
  0011 - Forward Slow
  0100 - Reverse Fast
  0101 - Reverse Medium
  0110 - Reverse Slow
  0111 - NULL
  1000 - Left Medium
  1001 - Left Slow
  1010 - Right Fast
  1011 - Right Medium
  1100 - Right Slow
  1101 - Left Fast
  1110 - Head Fine Left  NOTE! 
  1111 - Head Fine Right  NOTE! - This is a motor control b/c it must go back to 0000 to stop motors upon fulfilling one fine movement.
**************************/

/*************************
  Servo Control Codes:

  000 - LD, RD, HC
  001 - LD, RD, HL
  010 - LD, RD, HR
  011 - LU, RD, HC
  100 - LD, RU, HC
  101 - LU, RU, HC
  110 - LM, RD, HC
  111 - NULL
**************************/

/*******************************************************
   To Add:
   1. Use null codes.
 ******************************************************/

#include <Servo.h>


/* Motor Pins Setup PWM Mode */
const int M1_DIR = 4;
const int M1_SPEED = 5; //Left Motor
const int M2_SPEED = 6; //Right Motor
const int M2_DIR = 7;

/* Servo Pins Setup */
const int LEFT_WING_PIN = 11;
const int HEAD_PIN = 10;
const int RIGHT_WING_PIN = 9;

/* Setup Servo Objects */
Servo headServo, leftWingServo, rightWingServo;

/* Raspberry Pi Input Control Pins Setup */
const int MOTOR_CONTROL_1 = 0;
const int MOTOR_CONTROL_2 = 1;
const int MOTOR_CONTROL_3 = 2;
const int MOTOR_CONTROL_4 = 3;
const int SERVO_CONTROL_1 = 8;
const int SERVO_CONTROL_2 = 12;
const int SERVO_CONTROL_3 = 13;

/* Raspberry Pi Input Control Pin States*/
int MC1 = 0;
int MC2 = 0;
int MC3 = 0;
int MC4 = 0;
int SC1 = 0;
int SC2 = 0;
int SC3 = 0;

/* Globals Declaring PWM Speed for Relative Speeds */
const int fast = 255;
int medium = 150;
int slow = 100;

/* Declare Potentiometer Variables */
//const int potentiometerPin = A5;
//float potentiometerAdjustmentValue = 0;

/* Globals Declaring readable Servo Positions */
const int wingUp = 0;
const int wingMid = 90;
const int wingDown = 180;
const int headLeft = 180;
const int headCenter = 90;
const int headRight = 0;

/* Globals Declaring Previous Pin States */
String previousMotorControlStateCode = "0000";
String previousServoControlStateCode = "000";

/* Delay Time */
const int servoDelayTime = 15; //delay for servos
const int majorDelayTime = 100; //delay for main loop


/* Stop */
void stopMotors(void) {
  digitalWrite(M1_SPEED, LOW);
  digitalWrite(M2_SPEED, LOW);
}

/* Move Forward */
void moveForward(int desiredSpeed) {
  analogWrite(M1_SPEED, desiredSpeed);
  digitalWrite(M1_DIR, HIGH);
  analogWrite(M2_SPEED, desiredSpeed);
  digitalWrite(M2_DIR, HIGH);
}

/* Move Reverse */
void moveReverse(int desiredSpeed) {
  analogWrite(M1_SPEED, desiredSpeed);
  digitalWrite(M1_DIR, LOW);
  analogWrite(M2_SPEED, desiredSpeed);
  digitalWrite(M2_DIR, LOW);
}

/* Turn Left */
void turnLeft(int desiredSpeed) {
  analogWrite(M1_SPEED, desiredSpeed);
  digitalWrite(M1_DIR, HIGH);
  analogWrite(M2_SPEED, desiredSpeed);
  digitalWrite(M2_DIR, LOW);
}

/* Turn Right */
void turnRight(int desiredSpeed) {
  analogWrite(M1_SPEED, desiredSpeed);
  digitalWrite(M1_DIR, LOW);
  analogWrite(M2_SPEED, desiredSpeed);
  digitalWrite(M2_DIR, HIGH);
}

/* Position Left Wing */
void positionLeftWing(int pos) {
  leftWingServo.write(pos);
  delay(servoDelayTime);
}

/* Position Right Wing */
void positionRightWing(int pos) {
  rightWingServo.write(90);
  delay(servoDelayTime);
}

/* Position Head */
void positionHead(int pos) {
  headServo.write(pos);
  delay(servoDelayTime);
}

void positionHeadFineLeft() {
  headServo.write(headServo.read() + 5);
  delay(servoDelayTime);
}

void positionHeadFineRight() {
  headServo.write(headServo.read() - 5);
  delay(servoDelayTime);
}


/**************************
   Pin Configuration Setup
   Called at Boot
 **************************/
void setup() {
  //Set Input Pins
  pinMode(MOTOR_CONTROL_1, INPUT);
  pinMode(MOTOR_CONTROL_2, INPUT);
  pinMode(MOTOR_CONTROL_3, INPUT);
  pinMode(MOTOR_CONTROL_4, INPUT);
  pinMode(SERVO_CONTROL_1, INPUT);
  pinMode(SERVO_CONTROL_2, INPUT);
  pinMode(SERVO_CONTROL_3, INPUT);

  //Apply Pull-Up Resistance to Set Initial Relative State High
  digitalWrite(MOTOR_CONTROL_1, HIGH);
  digitalWrite(MOTOR_CONTROL_2, HIGH);
  digitalWrite(MOTOR_CONTROL_3, HIGH);
  digitalWrite(MOTOR_CONTROL_4, HIGH);
  digitalWrite(SERVO_CONTROL_1, HIGH);
  digitalWrite(SERVO_CONTROL_2, HIGH);
  digitalWrite(SERVO_CONTROL_3, HIGH);

  //Set Output Pins
  pinMode(M1_DIR, OUTPUT);
  pinMode(M1_SPEED, OUTPUT);
  pinMode(M2_SPEED, OUTPUT);
  pinMode(M2_DIR, OUTPUT);

  //Configure Servos
  headServo.attach(HEAD_PIN);
  leftWingServo.attach(LEFT_WING_PIN);
  rightWingServo.attach(RIGHT_WING_PIN);

  //Get Potentiometer Value
  //potentiometerAdjustmentValue = analogRead(potentiometerPin);
}

void loop() {
  //Update Control Pin States
  MC1 = digitalRead(MOTOR_CONTROL_1);
  MC2 = digitalRead(MOTOR_CONTROL_2);
  MC3 = digitalRead(MOTOR_CONTROL_3);
  MC4 = digitalRead(MOTOR_CONTROL_4);
  SC1 = digitalRead(SERVO_CONTROL_1);
  SC2 = digitalRead(SERVO_CONTROL_2);
  SC3 = digitalRead(SERVO_CONTROL_3);

  //Create Bit Code For Motor and Servo Control
  String motorControlCode = String(MC1) + String(MC2) + String(MC3) + String(MC4);
  String servoControlCode = String(SC1) + String(SC2) + String(SC3);
  Serial.println(servoControlCode);

  //Update Potentiometer Adjustment Level and Relative Speeds
  //potentiometerAdjustmentValue = analogRead(potentiometerPin);
  //medium = int((float(50)/float(337)) * potentiometerAdjustmentValue + 100);
  //slow = int((float(50)/float(337)) * potentiometerAdjustmentValue + 50);
  
  if (motorControlCode.equals(previousMotorControlStateCode)) {
    //Do Nothing
  }
  else {
    if (motorControlCode.equals("0000"))
      stopMotors();
    else if (motorControlCode.equals("0001"))
      moveForward(fast);
    else if (motorControlCode.equals("0010"))
      moveForward(medium);
    else if (motorControlCode.equals("0011"))
      moveForward(slow);
    else if (motorControlCode.equals("0100"))
      moveReverse(fast);
    else if (motorControlCode.equals("0101"))
      moveReverse(medium);
    else if (motorControlCode.equals("0110"))
      moveReverse(slow);
    else if (motorControlCode.equals("1101"))
      turnLeft(fast);
    else if (motorControlCode.equals("1000"))
      turnLeft(medium);
    else if (motorControlCode.equals("1001"))
      turnLeft(slow);
    else if (motorControlCode.equals("1010"))
      turnRight(fast);
    else if (motorControlCode.equals("1011"))
      turnRight(medium);
    else if (motorControlCode.equals("1100"))
      turnRight(slow);
    else if (motorControlCode.equals("1110"))
      positionHeadFineLeft();
    else if (motorControlCode.equals("1111"))
      positionHeadFineRight();
    else
      stopMotors();
  }

  if (servoControlCode.equals(previousServoControlStateCode)) {
    //Do Nothing
  }
  else {
    if (servoControlCode.equals("000")) {
      positionHead(headCenter);
      positionLeftWing(wingDown);
      positionRightWing(wingDown);
    }
    else if (servoControlCode.equals("001")) {
      positionHead(headLeft);
      positionLeftWing(wingDown);
      positionRightWing(wingDown);
    }
    else if (servoControlCode.equals("010")) {
      positionHead(headRight);
      positionLeftWing(wingDown);
      positionRightWing(wingDown);
    }
    else if (servoControlCode.equals("011")) {
      positionHead(headCenter);
      positionLeftWing(wingUp);
      positionRightWing(wingDown);
    }
    else if (servoControlCode.equals("100")) {
      positionHead(headCenter);
      positionLeftWing(wingDown);
      positionRightWing(wingUp);
    }
    else if (servoControlCode.equals("101")) {
      positionHead(headCenter);
      positionLeftWing(wingUp);
      positionRightWing(wingUp);
    }
    else if (servoControlCode.equals("110")) {
      positionHead(headCenter);
      positionLeftWing(wingMid);
      positionRightWing(wingDown);
    }
    else {
      positionHead(headCenter);
      positionLeftWing(wingDown);
      positionRightWing(wingDown);
    }
  }


  previousServoControlStateCode = servoControlCode;
  previousMotorControlStateCode = motorControlCode;
  delay(majorDelayTime);
}

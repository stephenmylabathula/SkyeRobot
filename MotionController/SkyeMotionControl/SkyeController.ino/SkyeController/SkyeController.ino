/**********************************
   SKYE Motion Control for RomeoV2
   Version 2.0
   Author: Stephen Mylabathula
   Last Edited: 8/18/2016
 **********************************/

/*****************************************
  Control Codes:

  00000 - Motors Stop
  00001 - Forward Fast
  00010 - Reverse Fast
  00011 - Left Fast
  00100 - Right Fast
  00101 - Forward-Left Drift Fast
  00110 - Forward-Right Drift Fast
  00111 - Forward Slow
  01000 - Reverse Slow
  01001 - Left Slow
  01010 - Right Slow
  01011 - Forward-Left Drift Slow
  01100 - Forward-Right Drift Slow
  01101 - Head Left
  01110 - Head Center
  01111 - Head Right
  10000 - Head Fine Left
  10001 - Head Fine Right
  10010 - Left Wing Up
  10011 - Left Wing Middle
  10100 - Left Wing Down
  10101 - Right Wing Up
  10110 - Right Wing Middle
  10111 - Right Wing Down
  11000 - Sound Sense 
  11001 - Eyes Effect 1 - Color Wipe Blue
  11010 - Eyes Effect 2 - Flash Blue
  11011 - Eyes Effect 3 - Color Wipe Red
  11100 - Eyes Effect 4 - Blink
  11101 - Eyes Effect 5 - 
  11110 - Eyes Effect 6 - 
  11111 - Eyes Off

******************************************/

/*********************************************

    NOTE: Requires Adafruit Neopixel Library
    NOTE: When passing in a Color it doesn't matter whether the color attribute comes from RightStrip or LeftStrip object.

 ********************************************/

 
#include <Adafruit_NeoPixel.h>
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

/* LED Eye Rings Setup */
const int LEFT_EYE_RING = 3;
const int RIGHT_EYE_RING = 13;

/* Setup Servo Objects */
Servo headServo, leftWingServo, rightWingServo;

/* Setup LED Ring Objects */
//Instantiation Method - Adafruit_NeoPixel(NumberLEDs, PinNumber, Type)
Adafruit_NeoPixel LeftStrip = Adafruit_NeoPixel(12, LEFT_EYE_RING, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel RightStrip = Adafruit_NeoPixel(12, RIGHT_EYE_RING, NEO_GRB + NEO_KHZ800);

/* Raspberry Pi Input Control Pins Setup */
const int CONTROL_1 = 0;
const int CONTROL_2 = 1;
const int CONTROL_3 = 2;
const int CONTROL_4 = 8;
const int CONTROL_5 = 12;

/* Raspberry Pi Input Control Pin States*/
int C1 = 0;
int C2 = 0;
int C3 = 0;
int C4 = 0;
int C5 = 0;

/* Globals Declaring PWM Speed for Relative Speeds */
const int fast = 255;
const int medium = 150;
const int slow = 100;

/* Globals Declaring readable Servo Positions */
const int wingUp = 0;
const int wingMid = 90;
const int wingDown = 180;
const int headLeft = 180;
const int headCenter = 90;
const int headRight = 0;

/* Global Declaring Previous Pin State */
String previousControlStateCode = "00000";

/* Delay Time */
const int servoDelayTime = 15; //delay for servos
const int majorDelayTime = 100; //delay for main loop


/* Stop */
void stopMotors(void) {
  digitalWrite(M1_SPEED, LOW);
  digitalWrite(M2_SPEED, LOW);
}

/* Move Forward */
void moveForward(int desiredSpeedLeft, int desiredSpeedRight) {
  analogWrite(M1_SPEED, desiredSpeedLeft);
  digitalWrite(M1_DIR, HIGH);
  analogWrite(M2_SPEED, desiredSpeedRight);
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

/* LED Effects Functions */
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<LeftStrip.numPixels(); i++) {
    LeftStrip.setPixelColor(i, c);
    LeftStrip.show();
    RightStrip.setPixelColor(i, c);
    RightStrip.show();
    delay(wait);
  }
}

void thinkCycle(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<LeftStrip.numPixels(); i++) {
    LeftStrip.setPixelColor(i, c);
    LeftStrip.setPixelColor(min(i+1, i-12), c);
    LeftStrip.setPixelColor(min(i+2, i-11), c);
    LeftStrip.setPixelColor(min(i+3, i-10), c);
    LeftStrip.setPixelColor(min(i+4, i-9), c);
    LeftStrip.setPixelColor(min(i+5, i-8), c);
    LeftStrip.setPixelColor(min(i+6, i-7), RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(min(i+7, i-6), RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(min(i+8, i-5), RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(min(i+9, i-4), RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(min(i+10, i-3), RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(min(i+11, i-2), RightStrip.Color(0,0,0));
    LeftStrip.show();
    RightStrip.setPixelColor(i, c);
    RightStrip.setPixelColor(min(i+1, i-12), c);
    RightStrip.setPixelColor(min(i+2, i-11), c);
    RightStrip.setPixelColor(min(i+3, i-10), c);
    RightStrip.setPixelColor(min(i+4, i-9), c);
    RightStrip.setPixelColor(min(i+5, i-8), c);
    RightStrip.setPixelColor(min(i+6, i-7), RightStrip.Color(0,0,0));
    RightStrip.setPixelColor(min(i+7, i-6), RightStrip.Color(0,0,0));
    RightStrip.setPixelColor(min(i+8, i-5), RightStrip.Color(0,0,0));
    RightStrip.setPixelColor(min(i+9, i-4), RightStrip.Color(0,0,0));
    RightStrip.setPixelColor(min(i+10, i-3), RightStrip.Color(0,0,0));
    RightStrip.setPixelColor(min(i+11, i-2), RightStrip.Color(0,0,0));
    RightStrip.show();
    delay(wait);
  }
}

void theaterChase(uint32_t c, uint8_t wait) {
  for (int j=0; j<10; j++) {  //do 10 cycles of chasing
    for (int q=0; q < 3; q++) {
      for (uint16_t i=0; i < RightStrip.numPixels(); i=i+3) {
        LeftStrip.setPixelColor(i+q, c);    //turn every third pixel on
        RightStrip.setPixelColor(i+q, c);
      }
      LeftStrip.show();
      RightStrip.show();

      delay(wait);

      for (uint16_t i=0; i < LeftStrip.numPixels(); i=i+3) {
        LeftStrip.setPixelColor(i+q, 0);        //turn every third pixel off
        RightStrip.setPixelColor(i+q, 0); 
      }
    }
  }
}

void blinkDown(){
    RightStrip.setPixelColor(9, RightStrip.Color(0,0,0));
    RightStrip.setPixelColor(10, RightStrip.Color(0,0,0));
    RightStrip.setPixelColor(3, RightStrip.Color(0,0,0));
    RightStrip.setPixelColor(4, RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(9, RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(10, RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(3, RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(4, RightStrip.Color(0,0,0));
    RightStrip.show();
    LeftStrip.show();
    delay(50);

    RightStrip.setPixelColor(8, RightStrip.Color(0,0,0));
    RightStrip.setPixelColor(11, RightStrip.Color(0,0,0));
    RightStrip.setPixelColor(2, RightStrip.Color(0,0,0));
    RightStrip.setPixelColor(5, RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(8, RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(11, RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(2, RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(5, RightStrip.Color(0,0,0));
    RightStrip.show();
    LeftStrip.show();
    delay(50);

    RightStrip.setPixelColor(7, RightStrip.Color(0,0,0));
    RightStrip.setPixelColor(0, RightStrip.Color(0,0,0));
    RightStrip.setPixelColor(1, RightStrip.Color(0,0,0));
    RightStrip.setPixelColor(6, RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(7, RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(0, RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(1, RightStrip.Color(0,0,0));
    LeftStrip.setPixelColor(6, RightStrip.Color(0,0,0));
    RightStrip.show();
    LeftStrip.show();
    delay(50);
}

void blinkUp(){

    RightStrip.setPixelColor(7, RightStrip.Color(0,0,255));
    RightStrip.setPixelColor(0, RightStrip.Color(0,0,255));
    RightStrip.setPixelColor(1, RightStrip.Color(0,0,255));
    RightStrip.setPixelColor(6, RightStrip.Color(0,0,255));
    LeftStrip.setPixelColor(7, RightStrip.Color(0,0,255));
    LeftStrip.setPixelColor(0, RightStrip.Color(0,0,255));
    LeftStrip.setPixelColor(1, RightStrip.Color(0,0,255));
    LeftStrip.setPixelColor(6, RightStrip.Color(0,0,255));
    RightStrip.show();
    LeftStrip.show();
    delay(50);

    RightStrip.setPixelColor(8, RightStrip.Color(0,0,255));
    RightStrip.setPixelColor(11, RightStrip.Color(0,0,255));
    RightStrip.setPixelColor(2, RightStrip.Color(0,0,255));
    RightStrip.setPixelColor(5, RightStrip.Color(0,0,255));
    LeftStrip.setPixelColor(8, RightStrip.Color(0,0,255));
    LeftStrip.setPixelColor(11, RightStrip.Color(0,0,255));
    LeftStrip.setPixelColor(2, RightStrip.Color(0,0,255));
    LeftStrip.setPixelColor(5, RightStrip.Color(0,0,255));
    LeftStrip.show();
    RightStrip.show();
    delay(50);
    
    RightStrip.setPixelColor(9, RightStrip.Color(0,0,255));
    RightStrip.setPixelColor(10, RightStrip.Color(0,0,255));
    RightStrip.setPixelColor(3, RightStrip.Color(0,0,255));
    RightStrip.setPixelColor(4, RightStrip.Color(0,0,255));
    LeftStrip.setPixelColor(9, RightStrip.Color(0,0,255));
    LeftStrip.setPixelColor(10, RightStrip.Color(0,0,255));
    LeftStrip.setPixelColor(3, RightStrip.Color(0,0,255));
    LeftStrip.setPixelColor(4, RightStrip.Color(0,0,255));
    RightStrip.show();
    LeftStrip.show();
    delay(50);
}

/**************************
   Pin Configuration Setup
   Called at Boot
 **************************/
void setup() {
  //Set Input Pins
  pinMode(CONTROL_1, INPUT);
  pinMode(CONTROL_2, INPUT);
  pinMode(CONTROL_3, INPUT);
  pinMode(CONTROL_4, INPUT);
  pinMode(CONTROL_5, INPUT);

  //Apply Pull-Up Resistance to Set Initial Relative State High
  digitalWrite(CONTROL_1, HIGH);
  digitalWrite(CONTROL_2, HIGH);
  digitalWrite(CONTROL_3, HIGH);
  digitalWrite(CONTROL_4, HIGH);
  digitalWrite(CONTROL_5, HIGH);

  //Set Output Pins
  pinMode(M1_DIR, OUTPUT);
  pinMode(M1_SPEED, OUTPUT);
  pinMode(M2_SPEED, OUTPUT);
  pinMode(M2_DIR, OUTPUT);
  pinMode(LEFT_EYE_RING, OUTPUT);
  pinMode(RIGHT_EYE_RING, OUTPUT);

  //Configure Servos
  headServo.attach(HEAD_PIN);
  leftWingServo.attach(LEFT_WING_PIN);
  //rightWingServo.attach(RIGHT_WING_PIN); //NOTE: Commented out because right servo is defective. Also Skye doesn't move its right wing.

  //Configure LED Rings
  LeftStrip.begin();
  RightStrip.begin();
  LeftStrip.show();
  RightStrip.show();
}

void loop() {
  //Update Control Pin States
  C1 = digitalRead(CONTROL_1);
  C2 = digitalRead(CONTROL_2);
  C3 = digitalRead(CONTROL_3);
  C4 = digitalRead(CONTROL_4);
  C5 = digitalRead(CONTROL_5);

  //Create Bit Code For Motor and Servo Control
  String controlCode = String(C1) + String(C2) + String(C3) + String(C4) + String(C5);

  //Don't run the same command twice unless it's special
  if (controlCode.equals(previousControlStateCode)) {
    if (controlCode.equals("11010"))
      theaterChase(LeftStrip.Color(0, 0, 127), 50);
    else if (controlCode.equals("11101"))
      thinkCycle(LeftStrip.Color(0, 0, 255), 50);

/*    UNCOMMENT IF YOU WANT THE SLOW HEAD TURN EFFECT
 *     else if (controlCode.equals("10001"))
      positionHeadFineRight();
    else if (controlCode.equals("10000"))
      positionHeadFineLeft();
*/
  }
  else {
    if (controlCode.equals("00000"))
      stopMotors();
    else if (controlCode.equals("00001"))
      moveForward(fast, fast);
    else if (controlCode.equals("00010"))
      moveReverse(fast);
    else if (controlCode.equals("00011"))
      turnLeft(medium);
    else if (controlCode.equals("00100"))
      turnRight(medium);
    else if (controlCode.equals("00101"))
      moveForward(medium, fast);
    else if (controlCode.equals("00110"))
      moveForward(fast, medium);
    else if (controlCode.equals("00111"))
      moveForward(slow, slow);
    else if (controlCode.equals("01000"))
      moveReverse(slow);
    else if (controlCode.equals("01001"))
      turnLeft(slow);
    else if (controlCode.equals("01010"))
      turnRight(slow);
    else if (controlCode.equals("01011"))
      moveForward(slow, medium);
    else if (controlCode.equals("01100"))
      moveForward(medium, slow);
    else if (controlCode.equals("01101"))
      positionHead(headLeft);
    else if (controlCode.equals("01110"))
      positionHead(headCenter);
    else if (controlCode.equals("01111"))
      positionHead(headRight);
    else if (controlCode.equals("10000"))
      positionHeadFineLeft();
    else if (controlCode.equals("10001"))
      positionHeadFineRight();
    else if (controlCode.equals("10010"))
      positionLeftWing(wingUp);
    else if (controlCode.equals("10011"))
      positionLeftWing(wingMid);
    else if (controlCode.equals("10100"))
      positionLeftWing(wingDown);
    else if (controlCode.equals("10101"))
      positionRightWing(wingUp);
    else if (controlCode.equals("10110"))
      positionRightWing(wingMid);
    else if (controlCode.equals("10111"))
      positionRightWing(wingDown);
    else if (controlCode.equals("11001"))
    {
      colorWipe(LeftStrip.Color(0, 0, 255), 50); // Blue
      colorWipe(RightStrip.Color(0, 0, 255), 50); // Blue
    }
    else if (controlCode.equals("11010"))
    {
      theaterChase(LeftStrip.Color(0, 0, 255), 50); // Blue
    }
    else if (controlCode.equals("11011"))
    {
      colorWipe(LeftStrip.Color(255, 0, 0), 50); // Red
    }
    else if (controlCode.equals("11100"))
    {
      blinkDown();
      delay(50);
      blinkUp();
    }
    else if (controlCode.equals("11101"))
    {
      thinkCycle(LeftStrip.Color(0, 0, 255), 50);
    }
    else if (controlCode.equals("11111"))
    {
      colorWipe(LeftStrip.Color(0, 0, 0), 50); // Black
      colorWipe(RightStrip.Color(0, 0, 0), 50); // Black
    }
    else
      stopMotors();
  }

  previousControlStateCode = controlCode;
  delay(majorDelayTime);
}

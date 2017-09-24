#include <wiringPi.h>
#include <softPwm.h>
#include <stdio.h>

/*******************************************************

Romeo to GPIO Motor Pin Configuration:

	GPIO 7 = Pin 7 = Motor 2 Direction (Violet)
	GPIO 11 = Pin 6 = Motor 2 PWM Speed (Blue)
	GPIO 13 = Pin 5 = Motor 1 PWM Speed (Green)
	GPIO 15 = Pin 4 = Motor 1 Direction (Yellow)

********************************************************/

/* WiringPi Setup */
#define M1_SPEED 2 //GPIO 13
#define M1_DIR 3 //GPIO 15
#define M2_SPEED 0 //GPIO 11
#define M2_DIR 7 //GPIO 7


void initializeMotors(void) {
	//PWM Initialization
	softPwmCreate(M1_SPEED, 0, 100);
	softPwmCreate(M2_SPEED, 0, 100);

	//Motor Pins Initialization
	pinMode(M1_DIR, OUTPUT);
	pinMode(M2_DIR, OUTPUT);
}

void forward(int lSpeed, int rSpeed) {
	softPwmWrite(M1_SPEED, lSpeed);
	softPwmWrite(M2_SPEED, rSpeed);
	digitalWrite(M1_DIR, HIGH);
	digitalWrite(M2_DIR, HIGH);
}

void stop(void) {
	digitalWrite(M1_SPEED, LOW);
	digitalWrite(M2_SPEED, LOW);
}

int main(void) {

	if(wiringPiSetup() == -1) {
		printf("WiringPi Failed!");
		return 1;
	}

	initializeMotors();
        forward(100, 100);
	printf("Hi");
        delay(100);
        stop();
}

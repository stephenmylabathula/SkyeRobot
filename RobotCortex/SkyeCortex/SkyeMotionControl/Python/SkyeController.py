# Skye Motion Control Software
# Author: Stephen Mylabathula 
# Last Edited - 7/1/2016

import RPi.GPIO as GPIO
import time
import sys

# Set Mode to Raw Pins
GPIO.setmode(GPIO.BOARD)

#Initialize Control Pin Variables
MC1 = 23
MC2 = 21
MC3 = 19
MC4 = 15
SC1 = 13
SC2 = 11
SC3 = 7

#Initialize Sensors
collisionSensor = 40
gonnaCrash = True

#Initialize Command Dictionary
motorCommandDictionary = {      "stop" : "0000",
				"forward fast" : "0001",
				"forward medium" : "0010",
				"forward slow" : "0011",
				"reverse fast" : "0100",
				"reverse medium" : "0101",
				"reverse slow" : "0110",
				"left fast" : "1101",
				"left medium" : "1000",
				"left slow" : "1001",
				"right fast" : "1010",
				"right medium" : "1011",
				"right slow" : "1100"
			  }


def initialize():

	#Set Control Pins as Outputs
	GPIO.setup(MC1, GPIO.OUT)
	GPIO.setup(MC2, GPIO.OUT)
	GPIO.setup(MC3, GPIO.OUT)
	GPIO.setup(MC4, GPIO.OUT)
	GPIO.setup(SC1, GPIO.OUT)
	GPIO.setup(SC2, GPIO.OUT)
	GPIO.setup(SC3, GPIO.OUT)

	#Set Sensors as Inputs
	GPIO.setup(collisionSensor, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(collisionSensor, GPIO.BOTH, callback=detect, bouncetime=200)
	
	#Set Initial Pin State Low
	GPIO.output(MC1, GPIO.LOW)
	GPIO.output(MC2, GPIO.LOW)
	GPIO.output(MC3, GPIO.LOW)
	GPIO.output(MC4, GPIO.LOW)
	GPIO.output(SC1, GPIO.LOW)
	GPIO.output(SC2, GPIO.LOW)
	GPIO.output(SC3, GPIO.LOW)

def stop():
	GPIO.cleanup()
	sys.exit()

def detect(chn):
	global gonnaCrash
	if gonnaCrash:
		gonnaCrash = False
		GPIO.output(MC1, 0)
		GPIO.output(MC2, 1)
		GPIO.output(MC3, 0)
		GPIO.output(MC4, 0)
	else:
		gonnaCrash = True
		GPIO.output(MC1, 0)
		GPIO.output(MC2, 0)
		GPIO.output(MC3, 0)
		GPIO.output(MC4, 0)
		
def execute(command):
	if command in motorCommandDictionary:
		commandCode = motorCommandDictionary[command]
		commandList = list(commandCode)		
		print("Exectuing", command, "with code", commandCode)	
		GPIO.output(MC1, int(commandList[0]))
		GPIO.output(MC2, int(commandList[1]))
		GPIO.output(MC3, int(commandList[2]))
		GPIO.output(MC4, int(commandList[3]))

	elif command == "exit":
		stop()
	else:
		print("Command not found!")


# Main Loop
initialize()
command = ""

while 0 == 0:
	command = input(">")
	execute(command)

stop()

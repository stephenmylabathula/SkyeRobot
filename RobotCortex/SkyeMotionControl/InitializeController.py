#Skye Motion Control Initialzation Script
#Author: Stephen Mylabathula
#Last Edited - 8/11/2016

import RPi.GPIO as GPIO
import time
import sys

# Set Mode to Raw Pins
GPIO.setmode(GPIO.BOARD)

#Initialize Control Pin Variables
C1 = 29
C2 = 31
C3 = 33
C4 = 35
C5 = 37

#Set Control Pins as Outputs
GPIO.setup(C1, GPIO.OUT)
GPIO.setup(C2, GPIO.OUT)
GPIO.setup(C3, GPIO.OUT)
GPIO.setup(C4, GPIO.OUT)
GPIO.setup(C5, GPIO.OUT)

#Set Initial Pin State Low
GPIO.output(C1, GPIO.LOW)
GPIO.output(C2, GPIO.LOW)
GPIO.output(C3, GPIO.LOW)
GPIO.output(C4, GPIO.LOW)
GPIO.output(C5, GPIO.LOW)

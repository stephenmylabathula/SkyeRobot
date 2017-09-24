import RPi.GPIO as GPIO

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

#Execute Stop Command - 00000
GPIO.output(C1, 0)
GPIO.output(C2, 0)
GPIO.output(C3, 0)
GPIO.output(C4, 1)
GPIO.output(C5, 0)

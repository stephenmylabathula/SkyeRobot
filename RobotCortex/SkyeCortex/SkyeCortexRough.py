import os
import cv2
import sys
import math
import time
import smbus
import pyvona
import imutils
import threading
import tkinter as tk
import RPi.GPIO as GPIO
from PIL import ImageTk, Image
from Components.Gauge import Gauge
from imutils.video import VideoStream
from Components.AttitudeIndicator import AttitudeIndicator


class SkyeCortex(tk.Frame):
    def __init__(self, master=None):
        #Start SKYE Talk
        self.voice = pyvona.create_voice('GDNAJLXBSXZ5SF2J65LA', 'ZEPIRgVi/bppB7gq4VGlKDesbvJYir24LAdAhRAO')
        self.voice.voice_name = "Salli"

        #Initialize Window Setting
        tk.Frame.__init__(self, master, padx=5, pady=5, bg="light gray")
        master.minsize(width=500, height=700)
        master.maxsize(width=1000, height=900)
        master.title("Skye Cortex")
        master.wm_title("Skye Cortex")
        master.wm_protocol("WM_DELETE_WINDOW", self.onClose)
        self.grid()

        #Start Camera
        print("Initializing Camera...")
        self.vs = VideoStream(usePiCamera=True).start()
        time.sleep(2.0)
        self.frame = None
        self.captureThread = None
        self.stopEvent = None
        self.faceCascade = cv2.CascadeClassifier("Components/HaarClassifier.xml")
        self.stopEvent = threading.Event()
        self.captureThread = threading.Thread(target=self.renderFeed, args=())
        self.captureThread.start()

        #Setup Raspberry Pi GPIO
        self.heartDutyCycle = 100
        self.initializeGPIO()
        self.speed = tk.IntVar()

        # Identify Power Management Registers
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c

        #Setup I2C
        self.bus = smbus.SMBus(1)
        self.address = 0x68 #I2C Address
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0) # Start the sensor in sleep mode
        
        #Draw Graphics
        self.renderGUI()
        self.temp = ImageTk.PhotoImage(Image.open("Components/Hymn.jpg"))
        self.captureDisplay = tk.Label(self.grpVision, image=self.temp, borderwidth=0, highlightthickness=0, width=320, height=240)
        self.captureDisplay.grid(row=0, column=0, padx=5, pady=5, columnspan=3, sticky=tk.N)
        self.captureDisplay.grid_propagate(0)

        #Start Metrics Thread
        self.metricsThread = None
        self.metricsThread = threading.Thread(target=self.updateMetrics, args=())
        self.metricsThread.start()

        #Start Heart PWM Thread
        self.heartPWMThread = None
        self.heartPWMThread = threading.Thread(target=self.heartPulse, args=())
        self.heartPWMThread.start()
        

    def renderGroupINSM(self):
        #Render Group Frame
        self.grpINSM = tk.LabelFrame(self, text="Intelligent Navigation System Monitor", width=530, height=260, bg="light gray")
        self.grpINSM.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N+tk.W, columnspan=2)
        self.grpINSM.grid_propagate(0)

        #Render Group Widgets
        self.INSM_Acceleration = Gauge(self.grpINSM, "Acceleration", "Components/GaugeTransparent.jpg", width = 150, height = 150, radius = 68)
        self.INSM_Acceleration.grid(row=0,column=0, padx=5, pady=0)
        self.INSM_Speed = Gauge(self.grpINSM, "Speed", "Components/GaugeTransparent.jpg", width = 200, height = 200, radius = 93)
        self.INSM_Speed.grid(row=0,column=1, padx=5, pady=0)
        self.INSM_Temperature= Gauge(self.grpINSM, "Temperature", "Components/GaugeWarning.jpg", width = 150, height = 150, radius = 68)
        self.INSM_Temperature.grid(row=0,column=2, padx=5, pady=0)
        
        self.INSM_lblAcceleration = tk.Label(self.grpINSM, text="     4.6     ", font="Digital-7 24", bg="light gray", fg="black", relief="sunken")
        self.INSM_lblAcceleration.grid(row=1,column=0, padx=5, pady=0)
        self.INSM_lblSpeed = tk.Label(self.grpINSM, text="0", font="Digital-7 24", bg="light gray", fg="black", relief="sunken")
        self.INSM_lblSpeed.grid(row=1,column=1, padx=5, pady=0)
        self.INSM_lblTemperature = tk.Label(self.grpINSM, text="     35     ", font="Digital-7 24", bg="light gray", fg="black", relief="sunken")
        self.INSM_lblTemperature.grid(row=1,column=2, padx=5, pady=0)

    def renderGroupCASM(self):
        #Render Group Frame
        self.grpCASM = tk.LabelFrame(self, text="Collision Avoidance System Monitor", width=300, height=100, bg="light gray")
        self.grpCASM.grid(row=1,column=0, padx=5, pady=5, sticky=tk.N+tk.W, columnspan=2)
        self.grpCASM.grid_propagate(0)

        #Render Group Widgets
        self.CASM_lblACDA = tk.Label(self.grpCASM, text="Assured Clear Distance Ahead: ", bg="light gray")
        self.CASM_lblACDA.grid(row=0, column=0, padx=5, pady=10, sticky=tk.E)
        self.CASM_lblRCPW = tk.Label(self.grpCASM, text="Rear Collision Proximity Warning: ", bg="light gray")
        self.CASM_lblRCPW.grid(row=1, column=0, padx=5, pady=0, sticky=tk.W)
        self.CASM_lblRCPWMetric = tk.Label(self.grpCASM, text="Clear", bg="light gray")
        self.CASM_lblRCPWMetric.grid(row=1, column=1, padx=5, pady=0, sticky=tk.W)
        self.CASM_lblACDAMetric = tk.Label(self.grpCASM, text="37.5cm", bg="light gray")
        self.CASM_lblACDAMetric.grid(row=0, column=1, padx=5, pady=0, sticky=tk.E)
#        self.CASM_lblACDAWarning = tk.Label(self.grpCASM, text="WARNING", bg="light gray",fg="red")
#        self.CASM_lblACDAWarning.grid(row=0, column=2, padx=5, pady=0, sticky=tk.E)
#        self.CASM_btnEmergency = tk.Button(self.grpCASM, text="Emergency System Shutoff", bg="light gray", borderwidth=0, highlightthickness=0, highlightbackground="light gray")
#        self.CASM_btnEmergency.grid(row=1, column=2, padx=5, pady=0, sticky=tk.W)

    def renderGroupSPEED(self):
        #Render Group Frame
        self.grpSPEED = tk.LabelFrame(self, text="Speed Setting", width=200, height=100, bg="light gray")
        self.grpSPEED.grid(row=1,column=1, padx=5, pady=5, sticky=tk.N+tk.W, columnspan=1)
        self.grpSPEED.grid_propagate(0)

        #Render Group Widgets
        self.radioFast = tk.Radiobutton(self.grpSPEED, text='Fast', value=2, bg='light gray', variable=self.speed)
        self.radioFast.grid(row=0,column=0, padx = 10, pady = 0, sticky=tk.W)
        self.radioSlow = tk.Radiobutton(self.grpSPEED, text='Slow', value=1, bg='light gray', variable=self.speed)
        self.radioSlow.grid(row=2,column=0, padx = 10, pady = 0, sticky=tk.W)
        self.radioFast.select()
        

    def renderGroupTALK(self):
        #Render Group Frame
        self.grpTalk = tk.LabelFrame(self, text="SKYE Talk", width=530, height=100, bg="light gray")
        self.grpTalk.grid(row=3,column=0, padx=5, pady=5, sticky=tk.N+tk.W, columnspan=2)
        self.grpTalk.grid_columnconfigure(0, weight=1) # allows textbox size to expand to fill frame
        self.grpTalk.grid_propagate(0)

        #Render Group Widgets
        self.TALK_txtSynthesis = tk.Entry(self.grpTalk, text="Enter Text:")
        self.TALK_txtSynthesis.grid(row=0, column=0, padx=5, pady=10, sticky=tk.W+tk.E)       
        self.TALK_btnSynthesis = tk.Button(self.grpTalk, text="Speak Text", bg="light gray", borderwidth=0, highlightthickness=0, highlightbackground="light gray")
        self.TALK_btnSynthesis.grid(row=1, column=0, padx=5, pady=0, sticky=tk.E)

        #Create Event Handler
        self.TALK_btnSynthesis["command"] = self.speak

    def renderGroupATTITUDE(self):
        #Render Group Frame
        self.grpAttitude = tk.LabelFrame(self, text="Attitude Indicator", width=320, height=300, bg="light gray")
        self.grpAttitude.grid(row=4,column=0, padx=5, pady=5, sticky=tk.S+tk.W)
        self.grpAttitude.grid_propagate(0)

        #Render Group Widgets
        self.ATTITUDE_inicator = AttitudeIndicator(self.grpAttitude)
        self.ATTITUDE_inicator.grid(row=0,column=0, padx=15, pady=5)

    def renderGroupVISION(self):
        #Render Group Frame
        self.grpVision = tk.LabelFrame(self, text="SKYE Vision", width=350, height=370, padx=5, pady=5, bg="light gray")
        self.grpVision.grid(row=0, column=2, padx=5, pady=5, rowspan=4, sticky=tk.N+tk.W)
        #self.grpVision.grid_propagate(0)

        #Render Group Widgets
        self.VISION_Canvas = tk.Canvas(self.grpVision, bg="light gray", borderwidth=0, highlightthickness=0, height=80) ### Height was originally 30 when working on the Pi
        self.VISION_Canvas.grid(row=1, column=0, padx=5, pady=5, columnspan=3, sticky=tk.N)
        
        #Draw Group Canvas Objects
        self.head_fine_left = ImageTk.PhotoImage(self.triangle_left_image.resize((30, 30)), Image.ANTIALIAS)
        self.head_fine_right = ImageTk.PhotoImage(self.triangle_right_image.resize((30, 30)), Image.ANTIALIAS)
        self.VISION_Canvas.create_image(110, 15, image=self.head_fine_left, tag="fine_left")
        self.VISION_Canvas.create_image(170, 15, image=self.head_fine_right, tag="fine_right")
        self.VISION_Canvas.create_oval(0, 50, 80, 78, fill="gray", tag="full_left")
        self.VISION_Canvas.create_oval(100, 50, 180, 78, fill="gray", tag="center")
        self.VISION_Canvas.create_oval(200, 50, 280, 78, fill="gray", tag="full_right")
        self.VISION_Canvas.create_text(140, 64, text="Center", fill="black", font="Arial 12", tag="center_text")
        self.VISION_Canvas.create_text(40, 64, text="Full Left", fill="black", font="Arial 12", tag="full_left_text")
        self.VISION_Canvas.create_text(240, 64, text="Full Right", fill="black", font="Arial 12", tag="full_right_text")

        #Create Event Handlers
        self.VISION_Canvas.tag_bind("fine_left", '<ButtonPress-1>', self.btnPressed_VISION_FineLeft)
        self.VISION_Canvas.tag_bind("fine_right", '<ButtonPress-1>', self.btnPressed_VISION_FineRight)

        self.VISION_Canvas.tag_bind("fine_left", '<ButtonRelease-1>', self.btnReleased_MOTION_Stop)
        self.VISION_Canvas.tag_bind("fine_right", '<ButtonRelease-1>', self.btnReleased_MOTION_Stop)
        
        self.VISION_Canvas.tag_bind("full_right", '<ButtonPress-1>', self.btnPressed_VISION_FullRight)
        self.VISION_Canvas.tag_bind("center", '<ButtonPress-1>', self.btnPressed_VISION_Center)
        self.VISION_Canvas.tag_bind("full_left", '<ButtonPress-1>', self.btnPressed_VISION_FullLeft)
        self.VISION_Canvas.tag_bind("full_right_text", '<ButtonPress-1>', self.btnPressed_VISION_FullRight)
        self.VISION_Canvas.tag_bind("center_text", '<ButtonPress-1>', self.btnPressed_VISION_Center)
        self.VISION_Canvas.tag_bind("full_left_text", '<ButtonPress-1>', self.btnPressed_VISION_FullLeft)

    def renderGroupLISTEN(self):
        #Render Group Frame
        self.grpListen = tk.LabelFrame(self, text="SKYE Listen", width=350, height=100, bg="light gray")
        self.grpListen.grid(row=3,column=2, padx=5, pady=5, sticky=tk.N+tk.W, columnspan=2)
        self.grpListen.grid_propagate(0)

        #Render Group Widgets
        self.LISTEN_lblCurrentQuery = tk.Label(self.grpListen, text="In the beginning God created the heavens and the earth. The spirit of God was hovering over the waters.", bg="light gray", wraplength=330, justify=tk.LEFT)
        self.LISTEN_lblCurrentQuery.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

    def renderGroupMOTION(self):
        #Render Group Frame
        self.grpMotion = tk.LabelFrame(self, text="SKYE Motion", width=560, height=300, bg="light gray")
        self.grpMotion.grid(row=4,column=1, padx=5, pady=5, sticky=tk.S, columnspan=2)
        self.grpMotion.grid_propagate(0)

        #Render Group Widgets
        self.MOTION_Canvas = tk.Canvas(self.grpMotion, bg="light gray", borderwidth=0, highlightthickness=0, width=480, height=280)
        self.MOTION_Canvas.grid(row=0, column=0)
        self.MOTION_Canvas.grid_propagate(0)

        #Draw Canvas Objects
        self.MOTION_Canvas.create_oval(20, 10, 280, 270)
        self.MOTION_Canvas.create_rectangle(320, 20, 470, 260)
        
        self.MOTION_Forward = ImageTk.PhotoImage(self.triangle_up_image.resize((70, 70)), Image.ANTIALIAS)
        self.MOTION_Canvas.create_image(150, 55, image=self.MOTION_Forward, tag="forward")
        self.MOTION_Reverse = ImageTk.PhotoImage(self.triangle_down_image.resize((70, 70)), Image.ANTIALIAS)
        self.MOTION_Canvas.create_image(150, 215, image=self.MOTION_Reverse, tag="reverse")
        self.MOTION_Left = ImageTk.PhotoImage(self.triangle_left_image.resize((70, 70)), Image.ANTIALIAS)
        self.MOTION_Canvas.create_image(70, 135, image=self.MOTION_Left, tag="left")
        self.MOTION_Right = ImageTk.PhotoImage(self.triangle_right_image.resize((70, 70)), Image.ANTIALIAS)
        self.MOTION_Canvas.create_image(230, 135, image=self.MOTION_Right, tag="right")
        
        self.MOTION_Canvas.create_arc(170, 45, 240, 115, fill="gray", tag="driftleft")
        self.MOTION_Canvas.create_arc(60, 45, 130, 115, start=90.0, fill="gray", tag="driftright")
        
        self.MOTION_WingUp = ImageTk.PhotoImage(self.triangle_up_image.resize((50, 50)), Image.ANTIALIAS)
        self.MOTION_Canvas.create_image(395, 60, image=self.MOTION_WingUp, tag="wing_up")
        self.MOTION_WingDown = ImageTk.PhotoImage(self.triangle_down_image.resize((50, 50)), Image.ANTIALIAS)
        self.MOTION_Canvas.create_image(395, 170, image=self.MOTION_WingDown, tag="wing_down")
        
        self.MOTION_Canvas.create_oval(385, 105, 405, 125, fill="dark gray", tag="wing_home")
        self.MOTION_Canvas.create_text(395, 230, text="Wing Control", fill="black", font="Arial 16")

        #Create Event Handlers
        self.MOTION_Canvas.tag_bind("forward", '<ButtonPress-1>', self.btnPressed_MOTION_Forward)
        self.MOTION_Canvas.tag_bind("reverse", '<ButtonPress-1>', self.btnPressed_MOTION_Reverse)
        self.MOTION_Canvas.tag_bind("left", '<ButtonPress-1>', self.btnPressed_MOTION_Left)
        self.MOTION_Canvas.tag_bind("right", '<ButtonPress-1>', self.btnPressed_MOTION_Right)
        self.MOTION_Canvas.tag_bind("driftleft", '<ButtonPress-1>', self.btnPressed_MOTION_DriftLeft)
        self.MOTION_Canvas.tag_bind("driftright", '<ButtonPress-1>', self.btnPressed_MOTION_DriftRight)

        self.MOTION_Canvas.tag_bind("forward", '<ButtonRelease-1>', self.btnReleased_MOTION_Stop)
        self.MOTION_Canvas.tag_bind("reverse", '<ButtonRelease-1>', self.btnReleased_MOTION_Stop)
        self.MOTION_Canvas.tag_bind("left", '<ButtonRelease-1>', self.btnReleased_MOTION_Stop)
        self.MOTION_Canvas.tag_bind("right", '<ButtonRelease-1>', self.btnReleased_MOTION_Stop)
        self.MOTION_Canvas.tag_bind("driftleft", '<ButtonRelease-1>', self.btnReleased_MOTION_Stop)
        self.MOTION_Canvas.tag_bind("driftright", '<ButtonRelease-1>', self.btnReleased_MOTION_Stop)
        
        self.MOTION_Canvas.tag_bind("wing_up", '<ButtonPress-1>', self.btnPressed_MOTION_WingUp)
        self.MOTION_Canvas.tag_bind("wing_home", '<ButtonPress-1>', self.btnPressed_MOTION_WingHome)
        self.MOTION_Canvas.tag_bind("wing_down", '<ButtonPress-1>', self.btnPressed_MOTION_WingDown)

        
    def heartPulse(self):
        while not self.stopEvent.is_set():
            time.sleep(0.01)
            if self.heartDutyCycle > 0:
                self.heartDutyCycle -= 1
            else:
                self.heartDutyCycle = 100
            self.heartPWM.ChangeDutyCycle(self.heartDutyCycle)


    def updateMetrics(self):
        while not self.stopEvent.is_set():
            #Delay 1-Second
            time.sleep(1)
            
            #Update Temperature
            temp = int(float(os.popen("vcgencmd measure_temp").read().lstrip("temp=").rstrip("'C\n")))
            self.INSM_Temperature.renderNeedle(temp)
            self.INSM_lblTemperature.configure(text = str(temp))

            #Update Attitude
            accel_xout = self.read_word_2c(0x3b)
            accel_yout = self.read_word_2c(0x3d)
            accel_zout = self.read_word_2c(0x3f)
            te = self.read_word_2c(0x41)
            accel_xout_scaled = accel_xout / 16384.0
            accel_yout_scaled = accel_yout / 16384.0
            accel_zout_scaled = accel_zout / 16384.0
            pitch = int(self.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
            roll = int(self.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
            self.ATTITUDE_inicator.renderBubble(-roll, -pitch)

            #Update Acceleration
#            self.INSM_lblAcceleration.configure(text = str(te))
 #           self.INSM_lblAcceleration.configure(text = str(     int(max(accel_yout_scaled * 100, 0))    ))
#            self.INSM_Acceleration.renderNeedle(int(max(accel_yout_scaled, 0) * 1000))

            #Update Speed
 #           self.INSM_Speed.renderNeedle(int(int(self.INSM_lblSpeed.cget("text")) + (accel_yout_scaled * 1000)))
#            self.INSM_lblSpeed.configure(text = str(int(int(self.INSM_lblSpeed.cget("text")) + (accel_yout_scaled * 1000))))
            
        
        
    def loadShapes(self):
        self.triangle_left_image = Image.open("Components/triangle_left.jpg")
        self.triangle_right_image = Image.open("Components/triangle_right.jpg")
        self.triangle_up_image = Image.open("Components/triangle_up.jpg")
        self.triangle_down_image = Image.open("Components/triangle_down.jpg")

        
    def renderGUI(self):
        self.loadShapes()
        self.renderGroupINSM()
        self.renderGroupCASM()
        self.renderGroupSPEED()
        self.renderGroupTALK()
        self.renderGroupATTITUDE()
        self.renderGroupVISION()
        self.renderGroupLISTEN()
        self.renderGroupMOTION()

    def renderFeed(self):
        try:
            while not self.stopEvent.is_set():
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=320)
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
                faces = self.faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )

                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                self.captureDisplay.configure(image=image)
                self.captureDisplay.image = image

        except RuntimeError:
            print("RuntimeError")

    def onClose(self):
        print("Closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.heartPWM.stop()
        GPIO.cleanup()
        self.quit()
        sys.exit(0)

    def btnPressed_VISION_FineLeft(self, event):
        self.executeCommand('10000')

    def btnPressed_VISION_FineRight(self, event):
        self.executeCommand('10001')

    def btnPressed_VISION_FullLeft(self, event):
        self.executeCommand('01101')

    def btnPressed_VISION_Center(self, event):
        self.executeCommand('01110')

    def btnPressed_VISION_FullRight(self, event):
        self.executeCommand('01111')

    def btnPressed_MOTION_Forward(self, event):
        if self.speed.get() == 1:
            motionThread = threading.Thread(target=self.executeCommand, args = ('00111', ))
            motionThread.start()
        elif self.speed.get() == 2:
            motionThread = threading.Thread(target=self.executeCommand, args = ('00001', ))
            motionThread.start()

    def btnPressed_MOTION_Reverse(self, event):
        if self.speed.get() == 1:
            motionThread = threading.Thread(target=self.executeCommand, args = ('01000', ))
            motionThread.start()
        elif self.speed.get() == 2:
            motionThread = threading.Thread(target=self.executeCommand, args = ('00010', ))
            motionThread.start()

    def btnPressed_MOTION_Left(self, event):
        if self.speed.get() == 1:
            motionThread = threading.Thread(target=self.executeCommand, args = ('01001', ))
            motionThread.start()
        elif self.speed.get() == 2:
            motionThread = threading.Thread(target=self.executeCommand, args = ('00011', ))
            motionThread.start()

    def btnPressed_MOTION_Right(self, event):
        if self.speed.get() == 1:
            motionThread = threading.Thread(target=self.executeCommand, args = ('01010', ))
            motionThread.start()
        elif self.speed.get() == 2:
            motionThread = threading.Thread(target=self.executeCommand, args = ('00100', ))
            motionThread.start()

    def btnPressed_MOTION_DriftLeft(self, event):
        if self.speed.get() == 1:
            motionThread = threading.Thread(target=self.executeCommand, args = ('01010', ))
            motionThread.start()
        elif self.speed.get() == 2:
            motionThread = threading.Thread(target=self.executeCommand, args = ('01011', ))
            motionThread.start()

    def btnPressed_MOTION_DriftRight(self, event):
        if self.speed.get() == 1:
            motionThread = threading.Thread(target=self.executeCommand, args = ('01100', ))
            motionThread.start()
        elif self.speed.get() == 2:
            motionThread = threading.Thread(target=self.executeCommand, args = ('00110', ))
            motionThread.start()

    def btnReleased_MOTION_Stop(self, event):
        self.executeCommand('00000')

    def btnPressed_MOTION_WingUp(self, event):
        self.executeCommand('10010')

    def btnPressed_MOTION_WingHome(self, event):
        self.executeCommand('10011')

    def btnPressed_MOTION_WingDown(self, event):
        self.executeCommand('10100')

    def speak(self):
        self.voice.speak(self.TALK_txtSynthesis.get())

    def executeCommand(self, bitString):
        GPIO.output(self.C1, int(bitString[0]))
        GPIO.output(self.C2, int(bitString[1]))
        GPIO.output(self.C3, int(bitString[2]))
        GPIO.output(self.C4, int(bitString[3]))
        GPIO.output(self.C5, int(bitString[4]))
        time.sleep(0.1)

    def initializeGPIO(self):
        #Set Pin Mode to Board
        GPIO.setmode(GPIO.BOARD)

        #Initialize Control Pin Variables
        self.C1 = 29
        self.C2 = 31
        self.C3 = 33
        self.C4 = 35
        self.C5 = 37
        self.HeartLED = 12

        #Set Control Pins as Outputs
        GPIO.setup(self.C1, GPIO.OUT)
        GPIO.setup(self.C2, GPIO.OUT)
        GPIO.setup(self.C3, GPIO.OUT)
        GPIO.setup(self.C4, GPIO.OUT)
        GPIO.setup(self.C5, GPIO.OUT)
        GPIO.setup(self.HeartLED, GPIO.OUT)

	#Set Initial Pin State Low
        GPIO.output(self.C1, GPIO.LOW)
        GPIO.output(self.C2, GPIO.LOW)
        GPIO.output(self.C3, GPIO.LOW)
        GPIO.output(self.C4, GPIO.LOW)
        GPIO.output(self.C5, GPIO.LOW)
        GPIO.output(self.HeartLED, GPIO.LOW)

        #Initialize PWM
        self.heartPWM = GPIO.PWM(self.HeartLED, 2000)
        self.heartPWM.start(self.heartDutyCycle)

    #I2C I/O Functions
    def read_byte(self, adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr):
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a,b):
        return math.sqrt((a*a)+(b*b))

    def get_y_rotation(self, x,y,z):
        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)

    def get_x_rotation(self, x,y,z):
        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)

        

app = SkyeCortex(tk.Tk())
app.mainloop()


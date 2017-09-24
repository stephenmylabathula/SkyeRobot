import os
import sys
import time
import json
import signal
import pyvona
import RPi.GPIO as GPIO
from pygame import mixer
from urllib import request
import speech_recognition as sr
import cv2
import imutils
import requests
import operator
import numpy as np
from PIL import ImageTk, Image
from imutils.video import VideoStream


#Setup Video Feed From Cmaer
vs = VideoStream(usePiCamera=True).start()
time.sleep(2)

#Setup Face Cascade File
faceCascade = cv2.CascadeClassifier("HaarClassifier.xml")

#Setup Microsoft API Keys and URLs
_urlFace = 'https://api.projectoxford.ai/face/v1.0/detect'
_keyFace = "67e917dbf9ec40188a4945bb5e216138"
_urlOCR = 'https://api.projectoxford.ai/vision/v1.0/ocr'
_keyOCR = 'f51d40ca3bdf418bacecc515ddc35db1'
_maxNumRetries = 10

#Global Variable for Age and Gender
age = 0
gender = 'none'

#HTTP Request for Age and Gender Estimation
def processFaceRequest( json, data, headers, params ):
    retries = 0
    result = None

    while True:
        response = requests.request( 'post', _urlFace, json = json, data = data, headers = headers, params = params )
        if response.status_code == 429:
            print( "Message: %s" % ( response.json()['error']['message'] ) )
            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print( 'Error: failed after retrying!' )
                break
        elif response.status_code == 200 or response.status_code == 201:
            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['error']['message'] ) )
        break
    return result

#HTTP Request for OCR
def processOCRRequest( json, data, headers, params ):
    retries = 0
    result = None

    while True:
        response = requests.request( 'post', _urlOCR, json = json, data = data, headers = headers, params = params )
        if response.status_code == 429: 
            print( "Message: %s" % ( response.json()['error']['message'] ) )
            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break
        elif response.status_code == 200 or response.status_code == 201:
            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None 
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None 
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json()['error']['message'] ) )
        break
    return result

#Setup the speech recognizer and microphone
r = sr.Recognizer()
with sr.Microphone(device_index=2, sample_rate=48000) as source:
    print("Initializing Microphone...")
    r.adjust_for_ambient_noise(source, duration = 1)
    r.dynamic_energy_threshold = False
    r.dynamic_energy_adjustment_damping = 0.15
    r.dynamic_energy_adjustment_ratio = 1.5
    if r.energy_threshold < 400:
        r.energy_threshold = 420
    r.pause_threshold = 0.5

# Set GPIO Mode to Raw Pin Numbering
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
GPIO.setup(12, GPIO.OUT)

def HeartOn():
    GPIO.output(12, GPIO.LOW)

def HeartOff():
    GPIO.output(12, GPIO.HIGH)

#Set Initial Pin State Low
GPIO.output(C1, GPIO.LOW)
GPIO.output(C2, GPIO.LOW)
GPIO.output(C3, GPIO.LOW)
GPIO.output(C4, GPIO.LOW)
GPIO.output(C5, GPIO.LOW)

def EyesFlash():
    GPIO.output(C1, 1)
    GPIO.output(C2, 1)
    GPIO.output(C3, 0)
    GPIO.output(C4, 1)
    GPIO.output(C5, 0)
    time.sleep(5)

def EyesThinking():
    GPIO.output(C1, 1)
    GPIO.output(C2, 1)
    GPIO.output(C3, 1)
    GPIO.output(C4, 0)
    GPIO.output(C5, 1)
    time.sleep(5)

def EyesBlue():
    GPIO.output(C1, 1)
    GPIO.output(C2, 1)
    GPIO.output(C3, 0)
    GPIO.output(C4, 0)
    GPIO.output(C5, 1)
    time.sleep(2)

def LiftLeftWing():
    GPIO.output(C1, 1)
    GPIO.output(C2, 0)
    GPIO.output(C3, 0)
    GPIO.output(C4, 1)
    GPIO.output(C5, 0)
    time.sleep(1)

def DropLeftWing():
    GPIO.output(C1, 1)
    GPIO.output(C2, 0)
    GPIO.output(C3, 1)
    GPIO.output(C4, 0)
    GPIO.output(C5, 0)
    time.sleep(1)

def EyesBlink():
    GPIO.output(C1, 1)
    GPIO.output(C2, 1)
    GPIO.output(C3, 1)
    GPIO.output(C4, 0)
    GPIO.output(C5, 0)
    time.sleep(1)
    EyesBlue()

def EyesOff():
    GPIO.output(C1, 1)
    GPIO.output(C2, 1)
    GPIO.output(C3, 1)
    GPIO.output(C4, 1)
    GPIO.output(C5, 1)
    time.sleep(1)

#Let Eyes Flash For 5 seconds to make sure network connectivity exists
EyesFlash()

#Setup Ivona Voice
os.popen('sudo date -s "$(curl -sD - google.com | grep "^Date:" | cut -d" " -f3-6)Z"')
voice = pyvona.create_voice('GDNAJLXBSXZ5SF2J65LA', 'ZEPIRgVi/bppB7gq4VGlKDesbvJYir24LAdAhRAO')
voice.voice_name = "Salli"

#Set Eyes Blue
EyesBlue()

#Lift Left Wing
LiftLeftWing()

voice.speak("Hello. I'm ready!")
time.sleep(1)

#Drop Left Wing
DropLeftWing()

#Setup Microphone
with sr.Microphone(device_index=2, sample_rate=48000) as source:
    print("Initializing Microphone...")
    r.adjust_for_ambient_noise(source, duration = 1)
    r.dynamic_energy_threshold = False
    r.dynamic_energy_adjustment_damping = 0.15
    r.dynamic_energy_adjustment_ratio = 1.5
    if r.energy_threshold < 400:
        r.energy_threshold = 420
    r.pause_threshold = 0.5

def GuessFace():
    voice.speak("Please stand in front of me, and look into my eyes.")
    inSession = False

    #Set Eyes Black
    EyesOff()

    try:
        while not inSession:
            frame = vs.read()
            frame = imutils.resize(frame, width=320)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            if len(faces) > 0:
                p = os.path.sep.join(("/home/pi/Documents/SkyeRobot/Presentation/", "face.jpg"))
                cv2.imwrite(p, frame.copy())
                print("Stored Image")
                pathToFileInDisk = r'/home/pi/Documents/SkyeRobot/Presentation/face.jpg'
                with open( pathToFileInDisk, 'rb' ) as f:
                    data = f.read()

                params = { 'returnFaceAttributes': 'age,gender',
                           'returnFaceLandmarks': 'true'}

                headers = dict()
                headers['Ocp-Apim-Subscription-Key'] = _keyFace
                headers['Content-Type'] = 'application/octet-stream'
                jsondata = None
                result = processFaceRequest( jsondata, data, headers, params )

                data = json.loads(str(result[0]['faceAttributes']).replace("'",'"'))
                age = data.get('age')
                gender = data.get('gender')
                inSession = True
            
    except RuntimeError:
        print("RuntimeError")

    #Set Eyes Blue
    EyesBlue()
    voice.speak("Okay. According to my calculations, you are a, " + gender + ", about ," + str(int(age)) + ", years old.")

def ReadText():

    #Set Eyes Black
    EyesBlack()

    try:
        frame = vs.read()
        frame = imutils.resize(frame, width=320)
        p = os.path.sep.join(("/home/pi/Documents/SkyeRobot/Presentation/", "text.jpg"))
        cv2.imwrite(p, frame.copy())
            
    except RuntimeError:
        print("RuntimeError")


    # Load raw image file into memory
    pathToFileInDisk = r'/home/pi/Documents/SkyeRobot/Presentation/text.jpg'
    with open( pathToFileInDisk, 'rb' ) as f:
        data = f.read()
    
    # Computer Vision parameters
    params = { 'language' : 'en'} 

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _keyOCR
    headers['Content-Type'] = 'application/octet-stream'

    jsont = None
    data = processOCRRequest( jsont, data, headers, params )

    #Set Eyes Blue
    EyesBlue()

    for i in range(len(data.get("regions")[0].get("lines"))):
        for j in range(len(data.get("regions")[0].get("lines")[i].get("words"))):
            voice.speak(data.get("regions")[0].get("lines")[i].get("words")[j].get("text"))

def speechListen():
    try:
        audio = r.listen(source, timeout = 3)
        return audio
    except sr.WaitTimeoutError as e: 
        raise e

def timeHandler(signum, frame):
    print("Speech Exceeds Timeout Limit!")
    raise OverflowError("Speech Limit Exceeded")

def transcribe(audio):
    try:
        text = r.recognize_google(audio)
        print(text)
        os.popen("aplay SkyeProcessing.wav")
        EyesBlue()

        if ('read' in str(text).lower() and 'text' in str(text).lower()) or 'read this' in str(text).lower() or 'what does this say' in str(text).lower():
            voice.speak("Okay give me a second.")
            ReadText()
        elif 'guess my' in str(text).lower():
            GuessFace()
        elif 'bye' in str(text).lower():
            os.popen("aplay SkyeOff.wav")
            GPIO.cleanup()
            sys.exit(0)
        else:
            query_msg = "+".join(text.split())
            request_url = "https://ec2-54-201-211-179.us-west-2.compute.amazonaws.com/chat?apiKey=2309sdlsdlk3420923sdlksdlk2423l3490244dlf&msg=" + query_msg + "&user=aef57655-6967-472c-8c7e-c9c1f6193f09"
            skye_response_api = request.urlopen(request_url)
            skye_response_json = ""

            while True:
                line = bytes.decode((skye_response_api.readline()))
                if line != '':
                    skye_response_json += line
                else:
                    break
           
            data = json.loads(skye_response_json)
            msg = data.get("msg")
            voice.speak(msg)
        os.popen("aplay SkyeOn.wav")
    except sr.UnknownValueError:
        EyesBlink()
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

with sr.Microphone(device_index=2, sample_rate=48000) as source:
    while True:
        HeartOn()
        print("Start speaking...")
        print(r.energy_threshold)
        try:
            signal.signal(signal.SIGALRM, timeHandler)
            signal.alarm(10)
            audio = speechListen()
        except sr.WaitTimeoutError:
            HeartOff()
            print("Timeout...")
            print("Restarting...")
            EyesBlink()
            continue
        except OverflowError:
            HeartOff()
            continue
        HeartOff()
        signal.alarm(0)
        print("Stopped!")
        EyesThinking()
        transcribe(audio)


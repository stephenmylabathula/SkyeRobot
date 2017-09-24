import speech_recognition as sr
import os
import time
import signal
import sys
import pyvona
from urllib import request
import json
from pygame import mixer
import RPi.GPIO as GPIO


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

voice = pyvona.create_voice('GDNAJLXBSXZ5SF2J65LA', 'ZEPIRgVi/bppB7gq4VGlKDesbvJYir24LAdAhRAO')
voice.voice_name = "Salli"

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
GPIO.setup(12, GPIO.OUT)

#Set Initial Pin State Low
GPIO.output(C1, GPIO.LOW)
GPIO.output(C2, GPIO.LOW)
GPIO.output(C3, GPIO.LOW)
GPIO.output(C4, GPIO.LOW)
GPIO.output(C5, GPIO.LOW)
GPIO.output(12, GPIO.LOW)

GPIO.output(C1, 1)
GPIO.output(C2, 1)
GPIO.output(C3, 0)
GPIO.output(C4, 0)
GPIO.output(C5, 1)

time.sleep(1)

GPIO.output(C1, 1)
GPIO.output(C2, 0)
GPIO.output(C3, 0)
GPIO.output(C4, 1)
GPIO.output(C5, 0)

voice.speak("Hello everybody!")
voice.speak(" I'm Skye!")
time.sleep(0.5)
voice.speak("These two cool dudes had an amazing internship project!")
voice.speak("During these three months they made me super smart.")
time.sleep(1)
voice.speak("Okay. Bring it on. Stefen ask me a question.")

GPIO.output(C1, 1)
GPIO.output(C2, 0)
GPIO.output(C3, 1)
GPIO.output(C4, 0)
GPIO.output(C5, 0)

time.sleep(8)
voice.voice_name = "Joey"

GPIO.output(C1, 1)
GPIO.output(C2, 1)
GPIO.output(C3, 0)
GPIO.output(C4, 1)
GPIO.output(C5, 1)

time.sleep(1)

GPIO.output(C1, 1)
GPIO.output(C2, 0)
GPIO.output(C3, 0)
GPIO.output(C4, 0)
GPIO.output(C5, 1)

time.sleep(3)

voice.speak("No!")
time.sleep(1)
voice.speak("Artificial Intelligence will take over the world....!")

mixer.init()
mixer.music.load("sinister.mp3")
mixer.music.play()

time.sleep(3)

GPIO.output(C1, 0)
GPIO.output(C2, 1)
GPIO.output(C3, 1)
GPIO.output(C4, 1)
GPIO.output(C5, 0)

time.sleep(1)

GPIO.output(C1, 1)
GPIO.output(C2, 1)
GPIO.output(C3, 0)
GPIO.output(C4, 0)
GPIO.output(C5, 1)

time.sleep(2)
voice.voice_name = "Salli"

voice.speak("Can I help you with anything else?")

with sr.Microphone(device_index=2, sample_rate=48000) as source:
    print("Initializing Microphone...")
    r.adjust_for_ambient_noise(source, duration = 1)
    r.dynamic_energy_threshold = False
    r.dynamic_energy_adjustment_damping = 0.15
    r.dynamic_energy_adjustment_ratio = 1.5
    if r.energy_threshold < 400:
        r.energy_threshold = 420
    r.pause_threshold = 0.5

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
        if 'bye' in str(text).lower():
            os.popen("aplay SkyeOff.wav")
            GPIO.cleanup()
            sys.exit(0)
        os.popen("aplay SkyeOn.wav")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

with sr.Microphone(device_index=2, sample_rate=48000) as source:
    while True:
        print("Start speaking...")
        print(r.energy_threshold)
        try:
            signal.signal(signal.SIGALRM, timeHandler)
            signal.alarm(10)
            audio = speechListen()
        except sr.WaitTimeoutError:
            print("Timeout...")
            print("Restarting...")
            continue
        except OverflowError:
            continue
        signal.alarm(0)
        print("Stopped!")
        transcribe(audio)

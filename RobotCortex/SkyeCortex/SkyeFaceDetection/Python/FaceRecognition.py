import os
import cv2
import sys
import json
import time
import signal
import pyvona
import imutils
import requests
import operator
import numpy as np
from urllib import request
from PIL import ImageTk, Image
import speech_recognition as sr
from imutils.video import VideoStream

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


vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
faceCascade = cv2.CascadeClassifier("HaarClassifier.xml")
inSession = False
_url = 'https://api.projectoxford.ai/face/v1.0/detect'
_key = "67e917dbf9ec40188a4945bb5e216138"
_maxNumRetries = 10

age = 0
gender = 'none'

def processRequest( json, data, headers, params ):
    retries = 0
    result = None

    while True:
        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )
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
            p = os.path.sep.join(("/home/pi/Documents/SkyeRobotBeta/SkyeCortexBeta/SkyeFaceDetection/Python/", "face.jpg"))
            cv2.imwrite(p, frame.copy())
            print("Stored Image")
            pathToFileInDisk = r'/home/pi/Documents/SkyeRobotBeta/SkyeCortexBeta/SkyeFaceDetection/Python/face.jpg'
            with open( pathToFileInDisk, 'rb' ) as f:
                data = f.read()

            params = { 'returnFaceAttributes': 'age,gender',
                       'returnFaceLandmarks': 'true'}

            headers = dict()
            headers['Ocp-Apim-Subscription-Key'] = _key
            headers['Content-Type'] = 'application/octet-stream'
            jsondata = None
            result = processRequest( jsondata, data, headers, params )

            data = json.loads(str(result[0]['faceAttributes']).replace("'",'"'))
            age = data.get('age')
            gender = data.get('gender')
            inSession = True
            
except RuntimeError:
            print("RuntimeError")

voice = pyvona.create_voice('GDNAJLXBSXZ5SF2J65LA', 'ZEPIRgVi/bppB7gq4VGlKDesbvJYir24LAdAhRAO')
voice.voice_name = "Salli"
voice.speak("Hello! Welcome to Carefest. My name is Skye, and I am a personal assistant robot that wants to make your life healthier and happier. What's your name?")

with sr.Microphone(device_index=2, sample_rate=48000) as source:
    try:
        print("Start speaking...")
        print(r.energy_threshold)
        audio = r.listen(source, timeout = 3)
        global name
        name = r.recognize_google(audio).lower().replace("my name is", "").replace("i'm", "").replace("i am", "")
    except sr.WaitTimeoutError as e: 
        raise e

voice.speak("Nice to meet you on this warm and sunny day" + name)
voice.speak("Being a robot, I love to make guesses and learn about the world around me. Would you like me to guess your age and gender?")

with sr.Microphone(device_index=2, sample_rate=48000) as source:
    try:
        print("Start speaking...")
        print(r.energy_threshold)
        audio = r.listen(source, timeout = 3)
        global guess
        guess = r.recognize_google(audio)
    except sr.WaitTimeoutError as e: 
        raise e

if "yes" in guess or "okay" in guess or "sure" in guess or "yup" in guess:
    voice.speak("Okay. According to my calculations, " + name + ", you are a, " + gender + ", about ," + str(int(age)) + ", years old.")
    voice.speak("Was I close?")

    with sr.Microphone(device_index=2, sample_rate=48000) as source:
        try:
            print("Start speaking...")
            print(r.energy_threshold)
            audio = r.listen(source, timeout = 3)
            global close
            close = r.recognize_google(audio)
        except sr.WaitTimeoutError as e: 
            raise e

    if "yes" in close:
        voice.speak("Hooray!")
    elif "no" in close:
        voice.speak("Darn it. Maybe next time.")
elif "no" in guess:
    voice.speak("No worries.")


voice.speak("Have you had something to eat already?")
with sr.Microphone(device_index=2, sample_rate=48000) as source:
    try:
        print("Start speaking...")
        print(r.energy_threshold)
        audio = r.listen(source, timeout = 3)
        global eaten
        eaten = r.recognize_google(audio)
    except sr.WaitTimeoutError as e: 
        raise e
if "yes" in eaten or "okay" in eaten or "sure" in eaten or "yup" in eaten:
    voice.speak("What did you eat?")
    with sr.Microphone(device_index=2, sample_rate=48000) as source:
        try:
            print("Start speaking...")
            print(r.energy_threshold)
            audio = r.listen(source, timeout = 3)
            global food
            food = r.recognize_google(audio).lower().replace("i ate", "").replace("i had", "")
        except sr.WaitTimeoutError as e: 
            raise e
    voice.speak("So you ate " + food + ", which contains approximately 500 calories, which means you will have to walk about 1700 steps to burn it off.")
if "no" in eaten:
    voice.speak("Well then I would definitely recommend that you try out the Insalata Caprese Salad. It contains only 230 calories, which means you would only need to walk 800 steps to burn it off.")


voice.speak("A lot of people have been working to make me learn more about the world.")
voice.speak("I have already read an entire encyclopedia and have learned to answer questions regarding healthcare, diseases, nutrition.")
voice.speak("So if you would like to learn about brain aneurysms, find out if it's healthy to eat a taco, or know when the next full moon is. I can answer all those questions.")
voice.speak("And if you want to stop talking to me, just say goodbye anytime during the conversation, and I won't feel offended at all")

voice.speak("So tell me, what questions can I answer for you?")

def timeHandler(signum, frame):
    print("Speech Exceeds Timeout Limit!")
    raise OverflowError("Speech Limit Exceeded")


def speechListen():
    try:
        audio = r.listen(source, timeout = 3)
        return audio
    except sr.WaitTimeoutError as e: 
        raise e


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
        

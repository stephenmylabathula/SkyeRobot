#!/usr/bin/python3
import speech_recognition as sr
import os
import signal
import sys
import pyvona
from urllib import request
import json

r = sr.Recognizer()
skyeListening = False
voice = pyvona.create_voice('GDNAJLXBSXZ5SF2J65LA', 'ZEPIRgVi/bppB7gq4VGlKDesbvJYir24LAdAhRAO')
voice.voice_name = "Salli"

def timeHandler(signum, frame):
    print("Speech Exceeds Timeout Limit!")
    raise OverflowError("Speech Limit Exceeded")


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


def transcribe(audio):
    global skyeListening
    try:
        if skyeListening:
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
        else:
            text = r.recognize_google(audio, show_all=True)
            print("Google Speech Recognition thinks you said " + str(text))
            if "sky" in str(text).lower():
                os.popen("aplay SkyeOn.wav")
                skyeListening = True
            if 'bye' in str(text).lower():
                os.popen("aplay SkyeOff.wav")
                sys.exit(0)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

with sr.Microphone(device_index=2, sample_rate=48000) as source:
    voice.speak("Skye is ready.")
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

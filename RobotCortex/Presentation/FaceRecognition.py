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
from imutils.video import VideoStream


vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
faceCascade = cv2.CascadeClassifier("HaarClassifier.xml")
inSession = False
_url = 'https://api.projectoxford.ai/face/v1.0/detect'
_key = "67e917dbf9ec40188a4945bb5e216138"
_maxNumRetries = 10
voice = pyvona.create_voice('GDNAJLXBSXZ5SF2J65LA', 'ZEPIRgVi/bppB7gq4VGlKDesbvJYir24LAdAhRAO')
voice.voice_name = "Salli"

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

voice.speak("Please stand in front of me, and look into my eyes.")

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

voice.speak("Okay. According to my calculations, you are a, " + gender + ", about ," + str(int(age)) + ", years old.")

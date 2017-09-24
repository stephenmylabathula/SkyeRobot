from __future__ import print_function
import time 
import requests
import cv2
import operator
import numpy as np
import os
import sys
import json
import signal
import pyvona
import imutils
import operator
from urllib import request
from PIL import ImageTk, Image
from imutils.video import VideoStream


vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
voice = pyvona.create_voice('GDNAJLXBSXZ5SF2J65LA', 'ZEPIRgVi/bppB7gq4VGlKDesbvJYir24LAdAhRAO')
voice.voice_name = "Salli"


_url = 'https://api.projectoxford.ai/vision/v1.0/ocr'
_key = 'f51d40ca3bdf418bacecc515ddc35db1'
_maxNumRetries = 10

def processRequest( json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

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
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/octet-stream'

jsont = None

data = processRequest( jsont, data, headers, params )

for i in range(len(data.get("regions")[0].get("lines"))):
    for j in range(len(data.get("regions")[0].get("lines")[i].get("words"))):
        voice.speak(data.get("regions")[0].get("lines")[i].get("words")[j].get("text"))







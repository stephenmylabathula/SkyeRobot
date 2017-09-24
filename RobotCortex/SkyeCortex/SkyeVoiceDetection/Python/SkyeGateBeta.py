import sys
import talkey
from urllib import request
import speech_recognition as speech

r = speech.Recognizer()
tts = talkey.Talkey()

while(True):
    print("Say something: ")
    with speech.Microphone(device_index = 2) as source:
        r.energy_threshold = 1000
        print(r.energy_threshold)
        audio = r.listen(source)

    print("Recognizing...")

    try:
        query = r.recognize_google(audio)
    except:
        continue

    query_msg = "+".join(query.split())
    request_url = "https://ec2-54-201-211-179.us-west-2.compute.amazonaws.com/chat?apiKey=2309sdlsdlk3420923sdlksdlk2423l3490244dlf&msg=" + query_msg + "&user=aef57655-6967-472c-8c7e-c9c1f6193f09"
    skye_response_api = request.urlopen(request_url)
    skye_response_json = ""

    while True:
        line = bytes.decode((skye_response_api.readline()))
        if line != '':
            skye_response_json += line
        else:
            break
        
    print(skye_response_json)
    index1 = skye_response_json.find('"')
    index2 = skye_response_json.find('"', index1 + 1)
    skye_response_string = skye_response_json[index1 : index2]
    print(skye_response_string)
    tts.say(skye_response_string)

    if "bye" in query:
        sys.exit(0)

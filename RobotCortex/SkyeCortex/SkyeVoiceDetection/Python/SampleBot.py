import sys
import time
import talkey
import speech_recognition as speech


r = speech.Recognizer()
tts = talkey.Talkey()

while(True):
    print("Say something: ")
    with speech.Microphone(device_index = 2, sample_rate = 48000) as source:
        r.energy_threshold = 100 #500 works good
        r.pause_threshold = 0.5
#        r.adjust_for_ambient_noise(source, duration = 1)
        print(r.energy_threshold)
        audio = r.listen(source)

    print("Recognizing...")

    try:
        query = "hey sky"#r.recognize_google(audio)
    except:
        continue

    if "hey sky" in query or "hi sky" in query or "hello sky" in query:
        tts.say("Hi there! How may I help you.")
    
#    if "hello" in query or "hi" in query:
 #       tts.say("Hello!")

#    if "your name" in query:
 #       tts.say("My name is Sky!")

  #  if "bye" in query:
   #     tts.say("Goodbye!")
    #    sys.exit(0)

   # if "time" in query:
    #    rawHour = time.localtime(time.time()).tm_hour - 5
     #   minute = time.localtime(time.time()).tm_min
      #  meridiam = " Ay Em"
  #      if rawHour > 12:
   #         rawHour -= 12
    #        meridiam = " Pee Em"
     #   tts.say("The local time is " + str(rawHour) + " " + str(minute) + str(meridiam))
        
    

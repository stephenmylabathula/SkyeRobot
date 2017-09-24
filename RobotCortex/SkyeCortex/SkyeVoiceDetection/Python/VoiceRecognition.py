import speech_recognition as sr

r = sr.Recognizer()

for mic in sr.Microphone.list_microphone_names():
    print(mic)

with sr.Microphone(device_index=2, sample_rate=48000) as source:
    r.energy_threshold = 1000
    print(r.energy_threshold)
    audio = r.listen(source)

print("Recognizing...")
print(r.recognize_google(audio))

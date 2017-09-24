print("Loading components this may take several seconds...")

import cv2
import sys
import talkey

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)
tts = talkey.Talkey()
cap = cv2.VideoCapture(0)
seeingFaces = False

print("Camera Ready...")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret = cap.set(3, 320)
    ret = cap.set(4, 240)
    ret = cap.set(5, 30)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,#1.1
        minNeighbors=5,#5
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(faces) > 0 and seeingFaces == False:
        seeingFaces = True
        tts.say("Hello! My name is sky. How may I help you today?")
        #print('Found', len(faces), 'faces')
        print(faces[0])
    else:
        seeingFaces = False

#    Draw a rectangle around the faces
#    for (x, y, w, h) in faces:
 #       cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

#    Display the resulting frame
#    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()

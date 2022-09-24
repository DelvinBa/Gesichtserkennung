# This is a demo of running face recognition on a Raspberry Pi.
# This program will print out the names of anyone it recognizes to the console.

# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

from symbol import for_stmt
from time import sleep
import cv2
import os
import face_recognition
import picamera
import numpy as np
import json
import paho.mqtt.client as mqtt


client = mqtt.Client()
client.connect("172.16.2.5", 1883, 60)
client.publish("securedoor/face", 3)
    
print("signal geschickt")

        

# Get a reference to the Raspberry Pi camera.
# If this fails, make sure you have a camera connected to the RPi and that you
# enabled your camera in raspi-config and rebooted first.
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# Load a sample picture and learn how to recognize it.
print("Loading known face image(s)")
with open("faces.json") as json_file:
    data = json.load(json_file)
    
faces = data["faces"]
rectanglecolor = data["rectanglecolor"]
allFaces = []
for face in faces: 
    faceImage = face_recognition.load_image_file(face["img"])
    face_encoding = face_recognition.face_encodings(faceImage)[0]
    allFaces.append(face_encoding)
print("loading faces DONE")
# Initialize some variables
face_locations = []
face_encodings = []

while True:
    #print("Capturing image.")
    # Grab a single frame of video from the RPi camera as a numpy array
    camera.capture(output, format="bgr")

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(output)

    for location in face_locations:
        x = location[0]
        y = location[1]
        x2 = location[2]
        y2 = location[3]
        cv2.rectangle(output, (y, x), (y2, x2),
           color=(rectanglecolor["b"],rectanglecolor["g"],rectanglecolor["r"]), thickness=5)

    cv2.imshow("Kamera", output)
    if cv2.waitKey(1) == ord("q"):
        break

    #print(face_locations)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)
    
    if len(face_locations) == 0:
        client.publish("securedoor/face", 3)
        continue 

    # Loop over each face found in the frame to see if it's someone we know.
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(allFaces , face_encoding)
        name = "<Unknown Person>"

        authorized_face_detected = False
        unauthorized_face_detected = False
        for i in range(len(match)): 
            if match[i]:
                print("     " + faces[i]["name"] + " is authorized: " + str(faces[i]["authorized"]))
                if(faces[i]["authorized"] == True ) :
                    authorized_face_detected = True
                else:
                    unauthorized_face_detected = True

        if authorized_face_detected == True:
            client.publish("securedoor/face", 1)
        elif unauthorized_face_detected == True:
            client.publish("securedoor/face", 2)
        else:
            client.publish("securedoor/face", 0)

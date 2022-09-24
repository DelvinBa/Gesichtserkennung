import face_recognition
import cv2
import numpy as np
import os
import glob


from dataclasses import dataclass
@dataclass
class Person:
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0

def main():
    personen = [Person()]
    capture = cv2.VideoCapture(0)  # steuert die Kamera an
    # Orte wo Gesichter sich befinden
    current_dir = os.path.dirname(os.path.realpath(__file__))
    classifier_file = os.path.join(current_dir, "haarcascade_frontalface_default.xml")
    cascade = cv2.CascadeClassifier(classifier_file)

    while True:
        _, im = capture.read()
        # in scharz/weiß Bilder umwandeln
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(im_gray)
        for x, y, width, height in faces:
            cv2.rectangle(im, (x, y), (x + width, y + height),
                          color=(0, 0, 255), thickness=5)
            personen[0].x = 5

        cv2.imshow("Kamera", im)
        if cv2.waitKey(1) == ord("q"):
            break
    capture.realease()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

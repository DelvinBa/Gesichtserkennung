import cv2
import os

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
    cv2.imshow("Kamera", im)
    if cv2.waitKey(1) == ord("q"):
        break
capture.realease()
cv2.destroyAllWindows()

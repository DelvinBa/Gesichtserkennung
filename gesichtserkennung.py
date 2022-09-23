import cv2

capture = cv2.VideoCapture(0)  # steuert die Kamera an
# Orte wo Gesichter sich befinden
cascade = cv2.CascadeClassifier(
    r"C:\Users\jonas\Desktop\haarcascade_frontalface_default.xml")

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
print

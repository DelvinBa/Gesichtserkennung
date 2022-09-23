import cv2

capture = cv2.VideoCapture(0)  # steuert die Kamera an
# Orte wo Gesichter sich befinden
cascade = cv2.CascadeClassifier(
    "Users/menke/Desktop/opencv_data_haarcascades%20at%20master%20·%20opencv_opencv%20·%20GitHub.html")

while True:
    _, im = capture.read()
    # im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #in scharz/weiß Bilder umwandeln
   # faces = cascade.detectMultiScale(image_gray)
    # for x,y, width, height in faces:
    #   cv2.rectangle(image, (x,y), (x + width, y + height), color=(0, 0, 255), thickness=5)
    cv2.imshow("Kamera", im)
    if cv2.waitKey(1) == ord("q"):
        break
capture.realease()
cv2.destroyAllWindows()

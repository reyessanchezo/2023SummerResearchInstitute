# Importing OpenCV package
import cv2

cv2.namedWindow("Webcam")
vc = cv2.VideoCapture(0)  # turn on the camera
scale = 1
haar_cascade = cv2.CascadeClassifier('Haarcascade_frontalface_default.xml')
if vc.isOpened():  # try to get the first frame from webcam
    rval, frame = vc.read()
else:
    rval = False

while rval:
    # Converting image to grayscale
    gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Applying the face detection method on the grayscale image
    faces_rect = haar_cascade.detectMultiScale(gray_img, 1.1, 9)
    # Iterating through rectangles of detected faces
    for (x, y, w, h) in faces_rect:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (150, 150, 255), 2)
        cv2.putText(frame, "This is a person", [x, y - 10], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.imshow("Webcam", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break

cv2.destroyWindow("Webcam")
vc.release()

# just detecting human faces, need to recognize and store faces next. Find some way to track the face and do a pass/fail
# Try again using images from webcam - done

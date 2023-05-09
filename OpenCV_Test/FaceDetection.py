# Importing OpenCV package
import cv2

# Reading the image
scale = 0.4
img = cv2.imread('BigCrowd.jpg')
img = cv2.resize(img, None, fx=scale, fy=scale)
# Converting image to grayscale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Loading the required haar-cascade xml classifier file
haar_cascade = cv2.CascadeClassifier('Haarcascade_frontalface_default.xml')

# Applying the face detection method on the grayscale image
faces_rect = haar_cascade.detectMultiScale(gray_img, 1.1, 9)

# Iterating through rectangles of detected faces
for (x, y, w, h) in faces_rect:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)

cv2.imshow('Detected faces in white rectangles', img)

cv2.waitKey(0)

# just detecting human faces, need to recognize and store faces next. Find some way to track the face and do a pass/fail
# Try again using images from webcam

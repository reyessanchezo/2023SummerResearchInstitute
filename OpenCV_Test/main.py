# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

#import OpenCV module
import cv2
#os module for reading training data directories and paths
import os
import numpy as np
import colorsys

def hsl_to_bgr(h, s, l):
    r, g, b = tuple(round(i * 255) for i in colorsys.hls_to_rgb(h / 360.0, l / 100.0, s / 100.0))
    return (b, g, r)

#there is no label 0 in our training data so subject name for index/label 0 is empty
subjects = ["Oscar", "Ramiz", "Elvis"]

def detect_face(img):
    # convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # load OpenCV face detector, I am using LBP which is fast
    # there is also a more accurate but slow Haar classifier
    haar_cascade = cv2.CascadeClassifier('Haarcascade_frontalface_default.xml')

    # let's detect multiscale (some images may be closer to camera than others) images
    # result is a list of faces
    faces = haar_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);

    # if no faces are detected then return original img
    if (len(faces) == 0):
        return gray, (1, 2, 1, 2) # FIXME?

    # under the assumption that there will be only one face,
    # extract the face area
    (x, y, w, h) = faces[0]

    # return only the face part of the image
    return gray[y:y + w, x:x + h], faces[0]


# this function will read all persons' training images, detect face from each image
# and will return two lists of exactly same size, one list
# of faces and another list of labels for each face
def prepare_training_data(data_folder_path):
    # ------STEP-1--------
    # get the directories (one directory for each subject) in data folder
    dirs = os.listdir(data_folder_path)

    # list to hold all subject faces
    faces = []
    # list to hold labels for all subjects
    labels = []

    # let's go through each directory and read images within it
    for dir_name in dirs:

        # our subject directories start with letter 's' so
        # ignore any non-relevant directories if any
        if not dir_name.startswith("s"):
            continue;

        # ------STEP-2--------
        # extract label number of subject from dir_name
        # format of dir name = slabel
        # , so removing letter 's' from dir_name will give us label
        label = int(dir_name.replace("s", ""))

        # build path of directory containing images for current subject subject
        # sample subject_dir_path = "training-data/s1"
        subject_dir_path = data_folder_path + "/" + dir_name

        # get the images names that are inside the given subject directory
        subject_images_names = os.listdir(subject_dir_path)

        # ------STEP-3--------
        # go through each image name, read image,
        # detect face and add face to list of faces
        for image_name in subject_images_names:

            # ignore system files like .DS_Store
            if image_name.startswith("."):
                continue;

            # build image path
            # sample image path = training-data/s1/1.pgm
            image_path = subject_dir_path + "/" + image_name

            # read image
            image = cv2.imread(image_path)

            # display an image window to show the image
            cv2.imshow("Training on image...", cv2.resize(image, (200, 200)))
            #cv2.waitKey(2)
            # detect face
            face, rect = detect_face(image)

            # ------STEP-4--------
            # for the purpose of this tutorial
            # we will ignore faces that are not detected
            if face is not None:
                # add face to list of faces
                faces.append(face)
                # add label for this face
                labels.append(label)


    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

    return faces, labels

#let's first prepare our training data
#data will be in two lists of same size
#one list will contain all the faces
#and other list will contain respective labels for each face
print("Preparing data...")
faces, labels = prepare_training_data("training-data")
print("Data prepared")

#print total faces and labels
print("Total faces: ", len(faces))
print("Total labels: ", len(labels))

#create our LBPH face recognizer
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

#train our face recognizer of our training faces
face_recognizer.train(faces, np.array(labels))


# function to draw rectangle on image
# according to given (x, y) coordinates and
# given width and heigh
def draw_rectangle(img, rect, confidence):
    h = 120 * confidence / 100  # Map confidence from 0-100 to hue from red to green
    bgr = hsl_to_bgr(h, 100, 50)

    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x + w, y + h), bgr, 2)


# function to draw text on give image starting from
# passed (x, y) coordinates.
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)


# this function recognizes the person in image passed
# and draws a rectangle around detected face with name of the
# subject
def predict(test_img):
    # make a copy of the image as we don't want to change original image
    img = test_img.copy()
    # detect face from the image
    face, rect = detect_face(img)

    # predict the image using our face recognizer
    label, confidence = face_recognizer.predict(face)
    # get name of respective label returned by face recognizer
    label_text = subjects[label] + " " + str(round(confidence,3)) + "%"

    # draw a rectangle around face detected
    draw_rectangle(img, rect, confidence)
    # draw name of predicted person
    draw_text(img, label_text, rect[0], rect[1] - 5)

    return img

print("Predicting test images...")

#load test images
test_img1 = cv2.imread("test-data/test1.jpg")
test_img2 = cv2.imread("test-data/test2.jpg")
#test_img3 = cv2.imread("test-data/test3.jpg")

#perform a prediction
predicted_img1 = predict(test_img1)
predicted_img2 = predict(test_img2)
#predicted_img3 = predict(test_img3)
print("Prediction complete")

#display both images
#cv2.imshow(subjects[0], cv2.resize(predicted_img3, (400, 500)))
cv2.imshow(subjects[1], cv2.resize(predicted_img1, (400, 500)))
cv2.imshow(subjects[2], cv2.resize(predicted_img2, (400, 500)))
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
cv2.destroyAllWindows()

print("Opening webcam, please wait...")
cv2.namedWindow("Webcam")
vc = cv2.VideoCapture(0)  # turn on the camera


if vc.isOpened():  # try to get the first frame from webcam
    rval, frame = vc.read()
    frame = cv2.flip(frame, 1)
else:
    rval = False

while rval:
    # perform a prediction
    predicted_frame = predict(frame)
    cv2.imshow("Webcam", predicted_frame)
    rval, frame = vc.read()
    frame = cv2.flip(frame, 1)
    key = cv2.waitKey(50)
    if key == 27:  # exit on ESC
        break

cv2.destroyWindow("Webcam")
vc.release()

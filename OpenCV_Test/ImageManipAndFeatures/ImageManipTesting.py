# import the cv2 library
import cv2 as cv2
import numpy as np

Image = "Elevator.png"
scale = 0.5

# The function cv2.imread() is used to read an image.
img_orig = cv2.imread(Image, 1)
img_orig = cv2.resize(img_orig, None, fx=scale, fy=scale)
# The function cv2.imread() is used to read an image.
img_grayscale = cv2.imread(Image, 0)
img_grayscale = cv2.resize(img_grayscale, None, fx=scale, fy=scale)

#Add text in corner to caption the image
cv2.putText(img_orig, "This is text", [50, 50], cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2, cv2.LINE_AA)
cv2.putText(img_grayscale, "This is text", [50, 50], cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2, cv2.LINE_AA)

#Add some kind of filter - blur
img_blur = cv2.blur(img_grayscale,(5,5))
cv2.imshow('Blurred', img_blur)

#Edge finding
# Canny Edge Detection
edges = cv2.Canny(image=img_blur, threshold1=10, threshold2=10)
# Display Canny Edge Detection Image
cv2.imshow('Canny Edge Detection', edges)

# Shi-Tomasi corner detection function
# We are detecting only 100 best corners here
# You can change the number to get desired result.
corners = cv2.goodFeaturesToTrack(edges, 100, 0.005, 10)

#what are the features? Implementation
#goodFeaturesToTrack is a modified Harris edge detector that detects the strongest corners in an image.
#SIFT-Detects blobs and edges
#FAST-Detects corners and blobs quickly
#HARRIS-Base form of goodFeaturesToTrack, detects corners
# convert corners values to integer
# So that we will be able to draw circles on them
corners = np.intp(corners)

# draw red color circles on all corners
for i in corners:
    x, y = i.ravel()
    cv2.circle(img_orig, (x, y), 3, (255, 255, 255), 0)

# Display Corner Detection Image
cv2.imshow('Corner Detection - circled', img_orig)

# waitKey() waits for a key press to close the window and 0 specifies indefinite loop
cv2.waitKey(0)

# cv2.destroyAllWindows() simply destroys all the windows we created.
cv2.destroyAllWindows()
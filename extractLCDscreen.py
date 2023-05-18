# This will need to change so you pass in a file path and it
# outputs the square screen of the resistance meter

# Import the necessary packages
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2

# Load the example image
image = cv2.imread(r"C:\Users\Nicholas Lamanna\OneDrive - ATTAR\Nicholas Lamanna\OpenCV-DigitalScreenReader\images\full-RM.jpg")

# Pre-process the image by:
#    - resizing it, 
#    - converting it to graycale, 
#    - blurring it,
#    - and computing an edge map
image = imutils.resize(image, height=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 50, 200, 255)
cv2.imshow('Edged Image', edged)
cv2.waitKey(0)

# Find contours in the edge map, then sort them by their size in descending order
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
displayCnt = None
# loop over the contours
for c in cnts:
	# approximate the contour
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	# if the contour has four vertices, then we have found the thermostat display
	if len(approx) == 4:
		displayCnt = approx
		break
	
# Extract the thermostat display, apply a perspective transform to it
warped = four_point_transform(gray, displayCnt.reshape(4, 2))
output = four_point_transform(image, displayCnt.reshape(4, 2))
cv2.imshow('Output', output)
cv2.waitKey(0)
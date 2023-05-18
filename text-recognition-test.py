# Import required packages
import cv2
import pytesseract

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Read image from which text needs to be extracted
img = cv2.imread(r"C:\Users\Nicholas Lamanna\Desktop\OpenCV\no noise.jpg")

##### Preprocessing the image starts
# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('grayscale image', gray)
cv2.waitKey(0)

# Performing OTSU threshold
ret, thresh1 = cv2.threshold(gray, 140, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 
cv2.imshow('grayscale image', thresh1)
cv2.waitKey(0)

# Specify structure shape and kernel size.
# Kernel size increases or decreases the area
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect
# each word instead of a sentence.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))

# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
cv2.imshow('grayscale image', dilation)
cv2.waitKey(0)

# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Creating a copy of image
im2 = img.copy()

# A text file is created and flushed
file = open("recognized.txt", "w+")
file.write("")
file.close()

# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
for cnt in contours:
	x, y, w, h = cv2.boundingRect(cnt)
	
	# Drawing a rectangle on copied image
	rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
	
	# Cropping the text block for giving input to OCR
	cropped = im2[y:y + h, x:x + w]
	#cv2.imshow('grayscale image', cropped)
	#cv2.waitKey(0)		

	# Open the file in append mode
	file = open("recognized.txt", "a")
	
	# Apply OCR on the cropped image
	text = pytesseract.image_to_string(cropped)
	print(text)
	
	# Appending the text into file
	file.write(text)
	file.write("\n")
	
	# Close the file
	file.close

# import the necessary packages
import numpy as np
import argparse
import cv2
import time
import math
prev = [1,2]
font = cv2.FONT_HERSHEY_SIMPLEX
cap = cv2.VideoCapture(0)
#Set Width and Height 
# cap.set(3,1280)
# cap.set(4,720)

ret, frame = cap.read()
			
output = frame.copy()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
gray = cv2.GaussianBlur(gray,(5,5),0);
gray = cv2.medianBlur(gray,5)
	
gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,3.5)
	
kernel = np.ones((2,2),np.uint8)
gray = cv2.erode(gray,kernel,iterations = 1)
	# gray = erosion
	
gray = cv2.dilate(gray,kernel,iterations = 1)
	# gray = dilation

	
	# detect circles in the image
circles = cv2.HoughCircles(gray, 
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 40,
               param2 = 30, minRadius = 10, maxRadius = 30)
	
if circles is not None:
	circles = np.round(circles[0, :]).astype("int")
		
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle in the image
		# corresponding to the center of the circle
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
		
		prevx = x
		prevy = y
		prev = [prevx,prevy]



while(True):

	ret, frame = cap.read()
			
	output = frame.copy()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	gray = cv2.GaussianBlur(gray,(5,5),0);
	gray = cv2.medianBlur(gray,5)
	
	gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,3.5)
	
	kernel = np.ones((2,2),np.uint8)
	gray = cv2.erode(gray,kernel,iterations = 1)
	# gray = erosion
	
	gray = cv2.dilate(gray,kernel,iterations = 1)
	# gray = dilation

	
	# detect circles in the image
	circles = cv2.HoughCircles(gray, 
                   cv2.HOUGH_GRADIENT, 1, 20, param1 = 40,
               param2 = 30, minRadius = 10, maxRadius = 30)
	
	if circles is not None:
		circles = np.round(circles[0, :]).astype("int")
		
		for (x, y, r) in circles:
			# draw the circle in the output image, then draw a rectangle in the image
			# corresponding to the center of the circle
			cv2.circle(output, (x, y), r, (0, 255, 0), 4)
			cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
			coordi = [x,y]
			speed = math.dist(prev,coordi)/0.05
			prev = coordi
			cv2.putText(frame, 
                str(speed), 
                (50, 50), 
                font, 1, 
                (0, 255, 255), 
                2, 
                cv2.LINE_4)
			time.sleep(0.05)
			
			print ("Coordinates of centre: ")
			print(x,y)
			print ("Radius is: ")
			print (r)
			print("Speed: ")
			print(speed)

	cv2.imshow('gray',gray)
	cv2.imshow('frame',output)
	if cv2.waitKey(1) & 0xFF == ord('q'):
          break

cap.release()
cv2.destroyAllWindows()

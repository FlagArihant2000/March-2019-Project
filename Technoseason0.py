import numpy as np
import cv2 
cap = cv2.VideoCapture(0)
contour_sizes = 0
while True:
	ret,frame = cap.read()	
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	blur1 = cv2.GaussianBlur(hsv,(5,5),100)
	lower_color = np.array([25,100,100]) 
	upper_color = np.array([35,255,255]) 
	mask = cv2.inRange(blur1,lower_color,upper_color)

	im2,contours,hierarchy = cv2.findContours(mask,1,2)
	contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
	biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

	(x,y),radius = cv2.minEnclosingCircle(biggest_contour)
	center = (int(x), int(y))
	radius = int(radius)
	img = cv2.circle(frame, center, radius, (255,0,0), 2)
			
	M = cv2.moments(mask)
	cX = int(M["m10"]/M["m00"])
	cY = int(M["m01"]/M["m00"])
	cv2.circle(frame,(cX,cY),5,(0,0,255),-1)
	cv2.imshow('frame',frame)
	if cv2.waitKey(1) & 0xFF == 27:
		break

cap.release()
cv2.destroyAllWindows()

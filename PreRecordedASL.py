#importing libraries
import numpy as np
import cv2
import math 
from matplotlib import pyplot as plt

#capturing a pre-recorded video, followed by accessing fourcc code and the output is saved in the file output.avi with codec XVID
cap = cv2.VideoCapture('ASL.avi')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 25, (1920,1080))

#starts running every frame till the video clip is exhaused or till the user types 'q'
while (cap.isOpened()):
	try: # it is used to prevent any occurrence of error in the code 
		ret, img = cap.read() #Returns bool value of frames are found - True
		imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #conversion to grayscale
		blur = cv2.GaussianBlur(imgray,(5,5),0) # blurring of image (5*5)
		ret,thresh = cv2.threshold(blur ,100 ,255 ,cv2.THRESH_BINARY) #thresholding of image for pixel intensity > 100, then it is made to 255
		#finding the largest contours
		im2,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
		biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
		cnt = biggest_contour
		cv2.drawContours(img,contours,-1,(255,0,0),3) # drawing contours on the frames
		"""They return [start point,end point, farthest point, approx distance from farthest point"""
		hull = cv2.convexHull(cnt,returnPoints = False) # True returns coordinates of hull points
		defects = cv2.convexityDefects(cnt,hull)
                #finding the centroid of hand
		M = cv2.moments(thresh)
		cX = int(M["m10"]/M["m00"])
		cY = int(M["m01"]/M["m00"])
		cv2.circle(img,(cX,cY),5,(0,0,0),-1)
		# taking a reference defect
		a,b,c,d = defects[0,0]
		comp1 = tuple(cnt[a][0])
		comp2 = tuple(cnt[b][0])
		count_defects = 0
		counter = 0
		i = -1
		cv2.line(img,(0,350),(1800,350),3,1)
		ptlist = []
		theta = []
		for i in range(defects.shape[0]):
				#extracting defect points at all places
				p,q,r,s = defects[i,0]
				finger1 = tuple(cnt[p][0])
				finger2 = tuple(cnt[q][0])
				dist = math.sqrt((finger2[0] - comp2[0])**2 + (finger2[1] - comp2[1])**2)
				dist2 = math.sqrt((finger2[0] - cX)**2 + (finger2[1] - cY)**2)
				#cv2.circle(img,finger2,5,(255,255,255),-1)
				#sdist = math.sqrt((finger1[0] - cX)**2 + (cY - finger1[1])**2)
				#print(dist)
				comp2 = finger2
				if dist >= 70 and finger2[1] > 350 and dist2 > 340:
					ptlist = ptlist + [finger2]
					cv2.circle(img,finger2,5,(0,0,255),-1)	
					counter = counter + 1	
		i = 0
		# calculating the slopes between the centroid and the points found on fingertips and then finding the angle between the 2 fingertips with reference to the centroid of shape
		while i < (len(ptlist)-1):
			m1 = (ptlist[i][1] - cY)/(ptlist[i][0] - cX)
			m2 = (ptlist[i+1][1] - cY)/(ptlist[i+1][1] - cX)
			theta = theta + [math.atan(abs((m1 - m2)/(1.0 + m1*m2)))*(180/math.pi)]
			i = i + 1
		if counter !=3 and cY > 350:
			cv2.putText(img,"Number: "+str(counter),(1200,600), cv2.FONT_HERSHEY_SIMPLEX, 3,(0,0,0),2,cv2.LINE_AA)
		elif counter == 3:
			if sum(theta) > 90:
				cv2.putText(img,"Number: "+str(counter),(1200,600), cv2.FONT_HERSHEY_SIMPLEX, 3,(0,0,0),2,cv2.LINE_AA)
			elif sum(theta) < 55:
				cv2.putText(img,"Number: 6",(1200,600),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,0),2,cv2.LINE_AA)
			elif theta[0]/theta[1] > 2.5:
				cv2.putText(img,"Number: 7",(1200,600),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,0),2,cv2.LINE_AA)
			elif theta[0]/theta[1] < 2.5 and theta[0]/theta[1] > 1.65:
				cv2.putText(img,"Number: 9",(1200,600),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,0),2,cv2.LINE_AA)
			elif theta[0]/theta[1] < 1.65:
				cv2.putText(img,"Number: 8",(1200,600),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,0),2,cv2.LINE_AA)
		else:
			cv2.putText(img,"Number: 10",(1200,600),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,0),2,cv2.LINE_AA)
		out.write(img)
		cv2.imshow('frame',img)
		
		if cv2.waitKey(0.98) & 0xFF == ord('q'):
			break
	except:
		print("Done")
		cap.release()
		out.release()
		cv2.destroyAllWindows()
		


		
		

#cap.release()
#cv2.destroyAllWindows()
#plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
#plt.show()


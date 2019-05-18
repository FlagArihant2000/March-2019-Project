
#importing relevent libraries
import cv2
import numpy as np
import math
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID') # initializing fourcc codec
out = cv2.VideoWriter('output4.avi',fourcc, 20.0, (640,480)) # storing the output in output3.avi and will be stores frame by frame in out after doing image processing with
"""
Disclaimer: There is a chance that the program will not work properly for 7 and 8 as the calculated numbers on them are very close and vary as the hand position changes. This particular program is
hard coded and the best procedure would be by using Tensorflow to generalize the program for all types of hands and background.
"""
     
while(1):
        
    try:  #an error comes if it does not find anything in window as it cannot find contour of max area
          #therefore this try error statement
        #print(cap.get(3))
        #print(cap.get(4))
        ret, frame = cap.read()
        frame=cv2.flip(frame,1)
        kernel = np.ones((3,3),np.uint8)
        
        #define region of interest where the hand will be there
        roi=frame[100:300, 100:300]
        
        cv2.rectangle(frame,(100,100),(300,300),(0,255,0),0)   # drawing region of interest  
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV) # converting the color image to HSV type
        #cv2.circle(roi, (0,100), 3, [0,0,0], -1)
        
         
    # define range of skin color in HSV
        lower_skin = np.array([0,20,70], dtype=np.uint8)
        upper_skin = np.array([20,255,255], dtype=np.uint8)
        
     #extract skin colur imagw  
        mask = cv2.inRange(hsv, lower_skin, upper_skin) # this is kind of thesholding the part which is between the ranges of skin colour in hsv color system
        
   
        
        mask = cv2.dilate(mask,kernel,iterations = 5)  #the fingers are dilated enough to fill the dark spots within and also to find distinct points between the fingers later
        
    #blur the image
        mask = cv2.GaussianBlur(mask,(5,5),100) 
        
        
        
    #find contours
        _,contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
   #find contour of max area(hand)
        cnt = max(contours, key = lambda x: cv2.contourArea(x))
    #approx the contour a little for a proper display 
        epsilon = 0.0005*cv2.arcLength(cnt,True)
        approx= cv2.approxPolyDP(cnt,epsilon,True)
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.circle(roi,(cx,cy),3,[0,0,0],-1)
    #make convex hull around hand
        hull = cv2.convexHull(cnt)
        
     #define area of hull and area of hand
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)
      
    #find the percentage of area not covered by hand in convex hull
        arearatio=((areahull-areacnt)/areacnt)*100
    
     #find the defects in convex hull with respect to hand
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)
        
    # l = no. of defects
        l=0
        
    #code for finding no. of defects due to fingers
        ptlist = []
        ptlist2 = []
        for i in range(defects.shape[0]):
            s,e,f,d = defects[i,0]
            start = tuple(approx[s][0])
            end = tuple(approx[e][0])
            far = tuple(approx[f][0])
            #pt= (100,180)
            
            
            # find length of all sides of triangle
            a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
            b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
            c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
            s = (a+b+c)/2
            ar = math.sqrt(s*(s-a)*(s-b)*(s-c))
            
            #distance between point and convex hull
            d=(2*ar)/a
            
            # apply cosine rule here
            angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
            
        
            # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
            
            if angle <= 90 and d>30:
                l += 1
                cv2.circle(roi, far, 3, [255,0,0], -1)
                ptlist = ptlist + [start]
                ptlist2 = ptlist2 + [end]
            #draw lines around hand
            cv2.line(roi,start, end, [0,255,0], 2)
            
        l+=1
        #print corresponding gestures which are in their ranges
        
        
        
        
        

        font = cv2.FONT_HERSHEY_SIMPLEX
        
        if l==1:
            if areacnt<2000:
                cv2.putText(frame,'Put hand in the box',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            else:
                if arearatio<12:
                    cv2.putText(frame,'10',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                   
                else:
                    cv2.putText(frame,'1',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
                    
        elif l==2:
            cv2.putText(frame,'2',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
        elif l==3:
            ptlist = [ptlist[0],ptlist2[1]]
            distance = math.sqrt((ptlist[0][0] - ptlist[1][0])**2 + (ptlist[1][1] - ptlist[0][1])**2) 
            distance2 = math.sqrt((ptlist[1][0] - cx)**2 + (ptlist[1][1] - cy)**2)
            slope = (ptlist[0][1] - cy)/(ptlist[0][0] - cx)
            slope2 = (ptlist[1][1] - cy)/(ptlist[1][0] - cx)
            angle = math.atan((slope-slope2)/(1+(slope*slope2)))
            if(distance > 180):
                cv2.putText(frame,'3',(0,50),font,2,(0,0,255),3,cv2.LINE_AA)
            elif(distance < 125):
                cv2.putText(frame,'9',(0,50),font,2,(0,0,255),3,cv2.LINE_AA)
            else:
                #print(angle*180/3.1415)
                if abs(angle*180/3.1415) < 80:
                     
                     cv2.putText(frame,'8',(0,50),font,2,(0,0,255),3,cv2.LINE_AA)
                else:
                     
                     if(abs(slope) > 0.7):
                         cv2.putText(frame,'6',(0,50),font,2,(0,0,255),3,cv2.LINE_AA)
                     else:
                         cv2.putText(frame,'7',(0,50),font,2,(0,0,255),3,cv2.LINE_AA)       
                    
        elif l==4:
            cv2.putText(frame,'4',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
        elif l==5:
            cv2.putText(frame,'5',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
        elif l==6:
            cv2.putText(frame,'reposition',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
        else :
            cv2.putText(frame,'reposition',(10,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
            
        #show the windows
        out.write(frame)
        cv2.imshow('frame',frame)
    except:
        cv2.imshow('frame',frame)
        
    
    k = cv2.waitKey(5) & 0xFF
    if k == ord('q'):
        break

out.release()
cv2.destroyAllWindows()
cap.release() 

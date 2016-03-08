import numpy as np
import cv2
import time
import requests
import urllib
import urllib2
import sys

cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FPS, 10)


# face_cascade = cv2.CascadeClassifier("../haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

def eyes_closed(grayImage):
	# detected = eye_cascade.detectMultiScale(grayImage, )
	# print len(detected)
	return len(detected)==0

startTime = time.clock()

#Identify pupils. Based on beta 1
# https://gist.github.com/edfungus/67c14af0d5afaae5b18c

w = 640
h = 480

eyes = cv2.CascadeClassifier('haarcascade_eye.xml')


while(1):
    ret, frame = cap.read()
    if ret==True:
	
		#downsample
		#frameD = cv2.pyrDown(cv2.pyrDown(frame))
		#frameDBW = cv2.cvtColor(frameD,cv2.COLOR_RGB2GRAY)
	

		frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
		# print frame.shape
		frame = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
		detected = eyes.detectMultiScale(frame, minNeighbors=5,scaleFactor=1.1, minSize=(10,10))
	
		#faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		#detected2 = faces.detectMultiScale(frameDBW, 1.3, 5)
		
		pupilFrame = frame
		pupilO = frame
		windowClose = np.ones((5,5),np.uint8)
		windowOpen = np.ones((2,2),np.uint8)
		windowErode = np.ones((2,2),np.uint8)

		#draw square
		for (x,y,w,h) in detected:
			cv2.rectangle(frame, (x,y), ((x+w),(y+h)), (0,0,255),1)	
			cv2.line(frame, (x,y), ((x+w,y+h)), (0,0,255),1)
			cv2.line(frame, (x+w,y), ((x,y+h)), (0,0,255),1)
			pupilFrame = cv2.equalizeHist(frame[y+(h*.25):(y+h), x:(x+w)])
			pupilO = pupilFrame
			ret, pupilFrame = cv2.threshold(pupilFrame,55,255,cv2.THRESH_BINARY)		#50 ..nothin 70 is better
			pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_CLOSE, windowClose)
			pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_ERODE, windowErode)
			pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_OPEN, windowOpen)

			#so above we do image processing to get the pupil..
			#now we find the biggest blob and get the centriod
			
			threshold = cv2.inRange(pupilFrame,250,255)		#get the blobs
			contours, hierarchy = cv2.findContours(threshold,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
			
			#if there are 3 or more blobs, delete the biggest and delete the left most for the right eye
			#if there are 2 blob, take the second largest
			#if there are 1 or less blobs, do nothing
			
			if len(contours) >= 2:
				#find biggest blob
				maxArea = 0
				MAindex = 0			#to get the unwanted frame 
				distanceX = []		#delete the left most (for right eye)
				currentIndex = 0 
				for cnt in contours:
					area = cv2.contourArea(cnt)
					center = cv2.moments(cnt)
					if (center['m00']!=0):
						cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
					else:
						cx=0
						cy=0
					distanceX.append(cx)	
					if area > maxArea:
						maxArea = area
						MAindex = currentIndex
					currentIndex = currentIndex + 1
		
				del contours[MAindex]		#remove the picture frame contour
				del distanceX[MAindex]
			
			eye = 'right'

			if len(contours) >= 2:		#delete the left most blob for right eye
				if eye == 'right':
					edgeOfEye = distanceX.index(min(distanceX))
				else:
					edgeOfEye = distanceX.index(max(distanceX))	
				del contours[edgeOfEye]
				del distanceX[edgeOfEye]

			if len(contours) >= 1:		#get largest blob
				maxArea = 0
				for cnt in contours:
					area = cv2.contourArea(cnt)
					if area > maxArea:
						maxArea = area
						largeBlob = cnt
					
			if len(largeBlob) > 0:	
				center = cv2.moments(largeBlob)
				if (center['m00']!=0):
					cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
				else:
					cx=0
					cy=0
				# cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
				cv2.circle(pupilO,(cx,cy),5,255,-1)

		
		if (len(detected)==0):
			print "Blinking!"
	
		#show picture
		cv2.imshow('frame',pupilO)
		# cv2.imshow('frame2',pupilFrame)
		# time.sleep(1)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	#else:
		#break

# Release everything if job is finished
cap.release()
cv2.destroyAllWindows()
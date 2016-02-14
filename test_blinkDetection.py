import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FPS,30)


eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
handCascade = cv2.CascadeClassifier("haarcascade_hand.xml")
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

blinkBool = False
blinkCount = 0
flag = False

overallTime = time.clock()
start = 0

blinkFrequency = 0.0

while(True):
	ret,img = cap.read()
	blinkFrequency = 60*blinkCount/((time.clock() - overallTime))
	# while(True):
		# Capture frame-by-frame
	# ret, img = cap.read()
	# img = cv2.imread('family.jpg')
	img = cv2.resize(img,(0,0),fx=0.4,fy=0.4)
	# Our operations on the frame come here
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


	faces = face_cascade.detectMultiScale(gray, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

	flag = False

	for (x,y,w,h) in faces:
	    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
	    roi_gray = gray[y:y+h, x:x+w]
	    roi_color = img[y:y+h, x:x+w]
	    eyes = eye_cascade.detectMultiScale(roi_gray)
	    for (ex,ey,ew,eh) in eyes:
	        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
	    if len(eyes)==0:
	    	flag = True
	    #limit to 1
	    break


	if (time.clock() - start) > 0.4:
		if (flag==False):
			blinkBool = False
	#now, if flag is true, then figure out blinking
	if (flag==True):
		if (blinkBool==False):
			#start timer
			start = time.clock()
			blinkBool = True
			blinkCount+=1
			print "Detect blink, total:",blinkCount
			print "Blink Frequency: ",blinkFrequency," in ",(time.clock()-overallTime)," sec"
		else:
			print "detect blink but disabled"
		#get the time spent

		#if less than 20 ms, do nothing



	# print "Found ",len(eyes)," eyes!"
	# print "Found ",len(eyes)," eyes!"
	# print "Found ",len(faces)," faces!"
	# Display the resulting frame
	cv2.imshow('Video',img)
	if (blinkCount==50):
		break
	if cv2.waitKey(1) & 0xFF == ord('q'):
	    break
# time.sleep(1)
# cv2.waitKey(0)	

# When everything done, release the capture
# cap.release()
cv2.destroyAllWindows()

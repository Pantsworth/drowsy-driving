from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
time.sleep(0.2)

eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

blinkBool = False
blinkCount = 0
flag = False

overallTime = time.clock()
start = 0
blinkFrequency = 0.00
width=500
height=500

camera.resolution=(width,height)
camera.framerate = 2
rawCapture = PiRGBArray(camera, size=(width,height))

rawCapture.truncate(0)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #grab the frame
    image = frame.array
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #show the frame
   

    faces = face_cascade.detectMultiScale(gray, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))
    flag = False
    print "Detected ",len(faces)," faces"
    fx=0
    fy=0
    fw=0
    fh=0
    for (x,y,w,h) in faces:
        cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_gray,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        print "Detected ",len(eyes),"eyes"
        #cv2.imshow("Frame",gray)    
        break
    cv2.imshow("Frame",gray)
        
    
    
    key = cv2.waitKey(1)&0xFF
    #clear stream
    rawCapture.truncate(0)
    #quit on 'q'
    if key==ord("q"):
        break
    

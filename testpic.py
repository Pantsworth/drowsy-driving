from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera = PiCamera()
time.sleep(0.2)

camera.resolution=(640,800)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,800))

rawCapture.truncate(0)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #grab the frame
    image = frame.array

    #show the frame
    cv2.imshow("Frame",image)
    key = cv2.waitKey(1)&0xFF

    #clear stream
    rawCapture.truncate(0)

    #quit on 'q'
    if key==ord("q"):
        break
    

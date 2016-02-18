import numpy as np
import cv2
import time
from matplotlib import pyplot as plt


cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FPS, 20)

eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
handCascade = cv2.CascadeClassifier("haarcascade_hand.xml")
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")

blinkBool = False
blinkCount = 0
flag = False

overallTime = time.clock()
start = 0

blinkFrequency = 0.0

while (True):
    ret, img = cap.read()
    blinkFrequency = 60 * blinkCount / ((time.clock() - overallTime))
    # while(True):
    # Capture frame-by-frame
    # ret, img = cap.read()
    # img = cv2.imread('family.jpg')
    img = cv2.resize(img, (0, 0), fx=0.4, fy=0.4)
    # Our operations on the frame come here
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # faces = face_cascade.detectMultiScale(gray, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20, 20))

    # flag = False

    # for (x, y, w, h) in faces:
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #     roi_gray = gray[y:y + (3*h/4), x:x + w]
    #     roi_color = img[y:y + (3*h/4), x:x + w]
    #     eyes = eye_cascade.detectMultiScale(roi_gray)
    #     for (ex, ey, ew, eh) in eyes:
    #         eye_img = roi_gray[ey:ey+eh, ex:ex+ew]
    #         cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    #         # hist = cv2.calcHist(eye_img,[0],None,[256],[0,256])
    #         circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100)
    #         if (circles):
    #             print "Detected ",len(circles),"circles"
    #             circles = np.round(circles[0, :]).astype("int")
    #             for (x,y,r) in circles:
    #                 cv2.circle(output,(x,y),r,(0,0,255),4)
    #         # plt.hist(eye_img.ravel(),256,[0,256]); plt.show()
    #         cv2.imshow
    #     if len(eyes) == 0:
    #         flag = True
    #         # limit to 1

    #     roi_gray_mouth = gray[(y+h/2):y+h, x:x + w]
    #     roi_color_mouth = img[(y+h/2):y+h, x:x + w]

    #     mouth = mouth_cascade.detectMultiScale(roi_gray_mouth)

    #     for (mx, my, mw, mh) in mouth:
    #         cv2.rectangle(roi_color_mouth, (mx, my), (mx + mw, my + mh), (255, 0, 255), 2)
    #     break

    # if (time.clock() - start) > 0.4:
    #     if (flag == False):
    #         blinkBool = False
    #     # now, if flag is true, then figure out blinking
    # if (flag == True):
    #     if (blinkBool == False):
    #         # start timer
    #         start = time.clock()
    #         blinkBool = True
    #         blinkCount += 1
    #         print "Detect blink, total:", blinkCount
    #         print "Blink Frequency: ", blinkFrequency, " in ", (time.clock() - overallTime), " sec"
    #     else:
    #         print "detect blink but disabled"
        # get the time spent

        # if less than 20 ms, do nothing

    # print "Found ",len(eyes)," eyes!"
    # print "Found ",len(eyes)," eyes!"
    # print "Found ",len(faces)," faces!"
    # Display the resulting frame

    circles = cv2.HoughCircles(gray,cv2.cv.CV_HOUGH_GRADIENT,1,120,
                            param1=50,param2=40,minRadius=50,maxRadius=100)
    # circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 75)
    if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(gray, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(gray, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        # show the output image
    cv2.imshow("output", gray)
    # cv2.waitKey(0)
    # cv2.imshow('Video', img)
    if (blinkCount == 50):
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # time.sleep(1)
# cv2.waitKey(0)	

# When everything done, release the capture
# cap.release()
cv2.destroyAllWindows()

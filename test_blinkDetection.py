import numpy as np
import cv2
import time
# from matplotlib import pyplot as plt


cap = cv2.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FPS, 20)

eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
handCascade = cv2.CascadeClassifier("haarcascade_hand.xml")
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")

# blinking vars
blink_flag = False
blink_bool = False
blink_count = 0
blink_start = 0
blink_frequency = 0.0


# yawning vars
yawn_flag = False
yawn_flag2 = False
yawn_bool = False
yawn_count = 0
yawn_frequency = 0.0
yawn_start = 0


overallTime = time.clock()

while (True):
    ret, img = cap.read()
    blink_frequency = 60 * blink_count / ((time.clock() - overallTime))
    # while(True):
    # Capture frame-by-frame
    # ret, img = cap.read()
    # img = cv2.imread('family.jpg')
    img = cv2.resize(img, (0, 0), fx=0.4, fy=0.4)
    # Our operations on the frame come here
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20, 20))

    blink_flag = False

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + (3*h/4), x:x + w]
        roi_color = img[y:y + (3*h/4), x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        eyes_detected = 0
        for (ex, ey, ew, eh) in eyes:
            eyes_detected += 1
            eye_img = roi_gray[ey:ey+eh, ex:ex+ew]
            eye_img_color = roi_color[ey:ey+eh, ex:ex+ew]
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
            # hist = cv2.calcHist(eye_img,[0],None,[256],[0,256])
            circles = cv2.HoughCircles(eye_img,cv2.cv.CV_HOUGH_GRADIENT,1,120,
                            param1=50,param2=30,minRadius=5,maxRadius=30)
            # circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 75)
            if circles is not None:
                # print len(circles) ,"circles found on 1 eye"
            # convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")

                # loop over the (x, y) coordinates and radius of the circles
                for (x, y, r) in circles:
                    # draw the circle in the output image, then draw a rectangle
                    # corresponding to the center of the circle
                    cv2.circle(eye_img_color, (x, y), r, (0, 0, 255), 4)
                    # cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            if (eyes_detected==2):
                break
        if len(eyes) == 0:
            blink_flag = True
            # limit to 1

        roi_gray_mouth = gray[(y+h/2):y+h, x:x + w]
        roi_color_mouth = img[(y+h/2):y+h, x:x + w]

        mouth = mouth_cascade.detectMultiScale(roi_gray_mouth,1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20, 20))

        for (mx, my, mw, mh) in mouth:
            mouth_detected = True
            cv2.rectangle(roi_color_mouth, (mx, my), (mx + mw, my + mh), (255, 0, 255), 2)
            roi_gray_mouth = gray[my:my+mh*2, mx:mx + 2*mw]
            circles = cv2.HoughCircles(roi_gray_mouth,cv2.cv.CV_HOUGH_GRADIENT,1,120,
                    param1=50,param2=20,minRadius=10,maxRadius=300)
            if circles is not None:
                print len(circles) ,"circles found on 1 mouth"
            # convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")

                # loop over the (x, y) coordinates and radius of the circles
                for (x, y, r) in circles:
                    # draw the circle in the output image, then draw a rectangle
                    # corresponding to the center of the circle
                    cv2.circle(roi_color_mouth, (x, y), r, (0, 0, 255), 4)
                    # cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            if mouth_detected:
                break

        if len(mouth) == 0 and yawn_flag2:
            yawn_flag = True

        if len(mouth) == 0:
            yawn_flag2 = True

        else:
            yawn_flag = False
            yawn_flag2 = False


    if (time.clock() - blink_start) > 0.4:
        if (blink_flag == False):
            blink_bool = False

    if (time.clock() - yawn_start) > 3.0:
        if yawn_flag == False:
            yawn_bool = False

        # now, if flag is true, then figure out blinking
    if (blink_flag == True):
        if (blink_bool == False):
            # start timer
            blink_start = time.clock()
            blink_bool = True
            blink_count += 1
            print "Detect blink, total:", blink_count
            print "Blink Frequency: ", blink_frequency, " in ", (time.clock() - overallTime), " sec"
        # else:
        #     print "detect blink but disabled"
        # get the time spent

    if yawn_flag:
        # print "Yawn Flag:", yawn_flag, "Yawn Bool: ", yawn_bool
        if not yawn_bool:
            yawn_start = time.clock()
            yawn_bool = True
            yawn_count += 1
            print "Detect yawn, total:", yawn_count
            print "Yawn Frequency: ", yawn_frequency, " in ", (time.clock() - overallTime), " sec"

            # print "detected yawn but disabled"

        # if less than 20 ms, do nothing

    # print "Found ",len(eyes)," eyes!"
    # print "Found ",len(eyes)," eyes!"
    # print "Found ",len(faces)," faces!"
    # Display the resulting frame
    cv2.imshow('Video', img)
    if (blink_count == 50):
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # time.sleep(1)
# cv2.waitKey(0)	

# When everything done, release the capture
# cap.release()
cv2.destroyAllWindows()

import numpy as np
import cv2
import time
import requests
import urllib
import urllib2
import sys
import datetime


def test2_blink():
    file = open('not_sleepy1.csv','w')
    file.write("Blink_Ratio,Blink_Length\n")
    # from matplotlib import pyplot as plt


    def getRate(timeArray):
        now = time.clock()
        only_past_minute = [x for x in timeArray if x > (now-60)]
        print only_past_minute

        return len(only_past_minute)


    cap = cv2.VideoCapture(0)
    cap.set(cv2.cv.CV_CAP_PROP_FPS, 20)

    eyes = cv2.CascadeClassifier("haarcascade_eye.xml")
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    mouth_cascade = cv2.CascadeClassifier("haarcascade_mcs_mouth.xml")

    # blinking vars
    blink_flag = False
    blink_bool = False
    blink_count = 0
    blink_start = 0
    blink_frequency = 0.0
    eyes_flag2 = 0


    # yawning vars
    yawn_flag = False
    yawn_flag2 = 0
    yawn_bool = False
    yawn_count = 0
    yawn_frequency = 0.0
    yawn_start = 0


    overallTime = time.clock()
    timeToSend = time.clock()
    sent = False
    recorded_time_blink=False

    blinkArr = []
    blinkLengthArr = []
    lastBlink = time.clock() #set to start at 0

    yawnTimes = []
    txt = ""
    fps = FPS().start()
    num_frames = 300


    while (fps._numFrames < num_frames):
        # update the FPS counter
        print(fps._numFrames)
        fps.update()

        ret, img = cap.read()
        img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
        # Our operations on the frame come here
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # faces = face_cascade.detectMultiScale(gray, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20, 20))

        blink_flag = False

        frame = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

        # print frame.shape

        faces = face_cascade.detectMultiScale(gray, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, minSize=(50, 50))
        for (x, y, w, h) in faces:

            eye_frame = gray[(y+h/5):(y+h/2), x:x+w]           # take a zorro mask subset

            detected = eyes.detectMultiScale(eye_frame, minNeighbors=4, scaleFactor=1.05, minSize=(7, 7))
            if len(detected) == 0:
                if eyes_flag2 > 0:
                    blink_flag = True
                    eyes_flag2 = 0
                else:
                    eyes_flag2 += 1
            else:
                eyes_flag2 = 0
                if blink_bool and recorded_time_blink == False:
                    # opened eyes, so record the time they were closed
                    timeSpent = (time.clock() - blink_start)
                    print "Blink was:",timeSpent," seconds long"

                    if len(blinkLengthArr) < 10:
                        blinkLengthArr.append(timeSpent)

                    else:
                        blinkLengthArr = blinkLengthArr[1:]
                        blinkLengthArr.append(timeSpent)
                    recorded_time_blink = True

                    # display average blinking time
                    last_minute_blinking = blinkLengthArr
                    print last_minute_blinking
                    blink_length_avg = -1

                    if not(last_minute_blinking == []):
                        blink_length_avg = sum(last_minute_blinking)/(float(len(last_minute_blinking)))
                        print "Average blinking time is ", blink_length_avg
                blink_flag = False

            # cv2.imshow("eyes",eye_frame)

            roi_gray_mouth = gray[(y+h/2):y+h, x:x + w]
            roi_color_mouth = img[(y+h/2):y+h, x:x + w]
            cv2.imshow("mouth", roi_gray_mouth)

            mouth = mouth_cascade.detectMultiScale(roi_gray_mouth,1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20, 20))
            # print "Length:",len(mouth)

            for (mx, my, mw, mh) in mouth:
                # print "finding mouth"
                mouth_detected = True
                cv2.rectangle(roi_color_mouth, (mx, my), (mx + mw, my + mh), (255, 0, 255), 2)
                roi_gray_mouth = gray[my:my+mh*2, mx:mx + 2*mw]

                if mouth_detected:
                    break

            if len(mouth) == 0:
                if yawn_flag2 > 5:
                    yawn_flag = True
                    yawn_flag2 = 0
                else:
                    yawn_flag2 += 1
            else:
                yawn_flag = False
                yawn_flag2 = 0

            break


        if (time.clock() - blink_start) > 1:
            if (blink_flag == False):
                blink_bool = False
                recorded_time_blink = False

        if (time.clock() - yawn_start) > 5.0:
            if yawn_flag == False:
                yawn_bool = False

            # now, if flag is true, then figure out blinking
        if (blink_flag == True):
            if (blink_bool == False):
                # start timer
                blink_start = time.clock()
                blink_bool = True
                blink_count += 1

                #time - lastBlink = time since last blink
                if (len(blinkArr)<50):
                    blinkArr.append(time.clock())
                else:
                    blinkArr = blinkArr[1:]
                    blinkArr.append(time.clock())
                # print "Blink Array: ",blinkArr
                blinkRatio = getRate(blinkArr)
                print "Blink Ratio: ",blinkRatio, "blinks per minute"

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


            # if less than 20 ms, do nothing
        timeElapsed = int(time.clock() - timeToSend)
        # print "Elapsed time:",timeElapsed
        if (timeElapsed>0 and (timeElapsed%30==0) and sent==False):
            print "\n\n\n\n ----- SAVING DATA ------- \n"
            # payload = {'yawnRate':yawn_frequency , 'blinkRate':blink_frequency}
            # url = "https://mhealthhelloworld-bpeynetti.c9users.io/insert.php"
            # r = requests.post(url,data=payload)
            txt = str(blinkRatio)+','+str(blink_length_avg)+'\n'
            file.write(txt)
            sent = True
        if (timeElapsed%30==1):
            sent = False


        cv2.imshow('Video', img)
        if (blink_count == 200):
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # time.sleep(1)

    print "WRITING DATA"


    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    file.write(txt)
    file.close()
    # When everything done, release the capture
    # cap.release()
    cv2.destroyAllWindows()


class FPS:
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # start the timer
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()


if __name__ == '__main__':
    test2_blink()
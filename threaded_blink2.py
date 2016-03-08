from __future__ import print_function
import datetime
from threading import Thread
import cv2
# import the necessary packages
# from imutils.video import WebcamVideoStream
# from imutils.video import FPS
import argparse
import imutils
import cv2
import numpy as np
import time


# picamera imports
# from picamera.array import PiRGBArray
# from picamera import PiCamera
# import time


def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()

    ap.add_argument("-n", "--num-frames", type=int, default=100,
                    help="# of frames to loop over for FPS test")

    ap.add_argument("-d", "--display", type=int, default=-1,
                    help="Whether or not frames should be displayed")
    args = vars(ap.parse_args())

    num_frames = 800
    display = False
    unthreaded = False
    pivideo = False
    faces = cv2.CascadeClassifier('haarcascade_eye.xml')


    if (unthreaded):
        # grab a pointer to the video stream and initialize the FPS counter
        print("[INFO] sampling frames from webcam...")
        stream = cv2.VideoCapture(0)
        fps = FPS().start()

        # loop over some frames
        while fps._numFrames < num_frames:
            # grab the frame from the stream and resize it to have a maximum
            # width of 400 pixels
            (grabbed, frame) = stream.read()
            frame = imutils.resize(frame, width=400)
            detectPupil(frame, faces)

            # check to see if the frame should be displayed to our screen
            if display:
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF


            # update the FPS counter
            fps.update()

        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        # do a bit of cleanup
        stream.release()
        cv2.destroyAllWindows()

    else:
        # created a *threaded* video stream, allow the camera sensor to warmup,
        # and start the FPS counter
        print("[INFO] sampling THREADED frames from webcam...")
        if pivideo:
            pass
            # vs = PiVideoStream(src=1).start()
        else:
            vs = WebcamVideoStream(src=0).start()
        fps = FPS().start()

        # loop over some frames...this time using the threaded stream
        while fps._numFrames < num_frames:
            # grab the frame from the threaded video stream and resize it
            # to have a maximum width of 400 pixels
            frame = vs.read()
            frame = imutils.resize(frame, width=640)
            detectPupil(frame, faces)

            # check to see if the frame should be displayed to our screen
            if display:
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF

            print(fps._numFrames)
            # update the FPS counter
            fps.update()

        # stop the timer and display FPS information
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

        # do a bit of cleanup
        cv2.destroyAllWindows()
        vs.stop()

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


class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.cv.CV_CAP_PROP_FPS, 20)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


def detectPupil(frame, faces):
        # gotta define largeBlob to keep things good
        largeBlob = []
        frame = frame
        ret = True

        if ret:
            # downsample
            # frameD = cv2.pyrDown(cv2.pyrDown(frame))
            # frameDBW = cv2.cvtColor(frameD,cv2.COLOR_RGB2GRAY)

            # detect face
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            detected = faces.detectMultiScale(frame, 1.3, 5)

            # faces = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            # detected2 = faces.detectMultiScale(frameDBW, 1.3, 5)

            pupilFrame = frame
            pupilO = frame
            windowClose = np.ones((5,5),np.uint8)
            windowOpen = np.ones((2,2),np.uint8)
            windowErode = np.ones((2,2),np.uint8)

            # draw square
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

                # so above we do image processing to get the pupil..
                # now we find the biggest blob and get the centriod

                threshold = cv2.inRange(pupilFrame,250,255)		# get the blobs
                contours, hierarchy = cv2.findContours(threshold,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

                # if there are 3 or more blobs, delete the biggest and delete the left most for the right eye
                # if there are 2 blob, take the second largest
                # if there are 1 or less blobs, do nothing

                if len(contours) >= 2:
                    # find biggest blob
                    maxArea = 0
                    MAindex = 0			# to get the unwanted frame
                    distanceX = []		# delete the left most (for right eye)
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

                    del contours[MAindex]		# remove the picture frame contour
                    del distanceX[MAindex]

                eye = 'right'

                if len(contours) >= 2:		# delete the left most blob for right eye
                    if eye == 'right':
                        edgeOfEye = distanceX.index(min(distanceX))
                    else:
                        edgeOfEye = distanceX.index(max(distanceX))
                    del contours[edgeOfEye]
                    del distanceX[edgeOfEye]

                if len(contours) >= 1:		# get largest blob
                    maxArea = 0
                    for cnt in contours:
                        area = cv2.contourArea(cnt)
                        if area > maxArea:
                            maxArea = area
                            largeBlob = cnt

                if len(largeBlob) > 0:
                    center = cv2.moments(largeBlob)
                    if (center['m00']!=0):
                        cx, cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
                    else:
                        cx = 0
                        cy = 0
                    # cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
                    cv2.circle(pupilO, (cx, cy),5,255,-1)

            if len(detected) == 0:
                print("Blinking!")

            # show picture
            # cv2.imshow('frame',pupilO)
            # cv2.imshow('frame2',pupilFrame)
            # time.sleep(1)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        return pupilO


def blink2_thread():
    file = open('not_sleepy1.csv','w')
    file.write("Blink_Ratio,Blink_Length\n")


    def getRate(timeArray):
        now = time.clock()
        only_past_minute = [x for x in timeArray if x > (now-60)]
        print(only_past_minute)
        return len(only_past_minute)


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
    blinkRatio = ''

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


    # ************************ NEW STUFF *****************
    num_frames = 300
    display = False
    unthreaded = False
    pivideo = False

    print("[INFO] sampling THREADED frames from webcam...")
    vs = WebcamVideoStream(src=0).start()
    fps = FPS().start()


    while (fps._numFrames < num_frames):
        frame_read = vs.read()

        img = cv2.resize(frame_read, (0, 0), fx=0.5, fy=0.5)
        # check to see if the frame should be displayed to our screen
        if display:
            cv2.imshow("Frame", img)
            key = cv2.waitKey(1) & 0xFF

        print(fps._numFrames)
        fps.update()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blink_flag = False

        faces = face_cascade.detectMultiScale(gray, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, minSize=(50, 50))
        for (x, y, w, h) in faces:

            eye_frame = gray[(y+h/5):(y+h/2), x:x+w]           # take a zorro mask subframe

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
                    print("Blink was:",timeSpent," seconds long")

                    if len(blinkLengthArr) < 10:
                        blinkLengthArr.append(timeSpent)

                    else:
                        blinkLengthArr = blinkLengthArr[1:]
                        blinkLengthArr.append(timeSpent)
                    recorded_time_blink = True

                    # display average blinking time
                    last_minute_blinking = blinkLengthArr
                    print(last_minute_blinking)
                    blink_length_avg = -1

                    if not(last_minute_blinking == []):
                        blink_length_avg = sum(last_minute_blinking)/(float(len(last_minute_blinking)))
                        print("Average blinking time is ", blink_length_avg)
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
                print("Blink Ratio: ",blinkRatio, "blinks per minute")

            # else:
            #     print "detect blink but disabled"
            # get the time spent

        if yawn_flag:
            # print "Yawn Flag:", yawn_flag, "Yawn Bool: ", yawn_bool
            if not yawn_bool:
                yawn_start = time.clock()
                yawn_bool = True
                yawn_count += 1
                print("Detect yawn, total:", yawn_count)
                print("Yawn Frequency: ", yawn_frequency, " in ", (time.clock() - overallTime), " sec")


            # if less than 20 ms, do nothing
        timeElapsed = int(time.clock() - timeToSend)
        # print "Elapsed time:",timeElapsed

        if (timeElapsed>0 and (timeElapsed%30==0) and sent==False):
            print("\n\n\n\n ----- SAVING DATA ------- \n")
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


    print("WRITING DATA")

    file.write(txt)
    file.close()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    vs.stop()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    blink2_thread()

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

#
# class VideoStream:
#     def __init__(self, src=0, usePiCamera=False, resolution=(320, 240),
#                  framerate=32):
#         # check to see if the picamera module should be used
#         if usePiCamera:
#             # only import the picamera packages unless we are
#             # explicity told to do so -- this helps remove the
#             # requirement of `picamera[array]` from desktops or
#             # laptops that still want to use the `imutils` package
#
#             # initialize the picamera stream and allow the camera
#             # sensor to warmup
#             self.stream = PiVideoStream(resolution=resolution,
#                                         framerate=framerate)
#
#         # otherwise, we are using OpenCV so initialize the webcam
#         # stream
#         else:
#             self.stream = WebcamVideoStream(src=src)
#
#         def start(self):
#             # start the threaded video stream
#             return self.stream.start()
#
#         def update(self):
#             # grab the next frame from the stream
#             self.stream.update()
#
#         def read(self):
#             # return the current frame
#             return self.stream.read()
#
#         def stop(self):
#             # stop the thread and release any resources
#             self.stream.stop()
#
#
# class PiVideoStream:
#     def __init__(self, resolution=(640, 480), framerate=24):
#         # initialize the camera and stream
#         self.camera = PiCamera()
#         self.camera.resolution = resolution
#         self.camera.framerate = framerate
#         self.rawCapture = PiRGBArray(self.camera, size=resolution)
#         self.stream = self.camera.capture_continuous(self.rawCapture,
#                                                      format="bgr", use_video_port=True)
#
#         # initialize the frame and the variable used to indicate
#         # if the thread should be stopped
#         self.frame = None
#         self.stopped = False
#
#     def start(self):
#         # start the thread to read frames from the video stream
#         Thread(target=self.update, args=()).start()
#         return self
#
#     def update(self):
#         # keep looping infinitely until the thread is stopped
#         for f in self.stream:
#             # grab the frame from the stream and clear the stream in
#             # preparation for the next frame
#             self.frame = f.array
#             self.rawCapture.truncate(0)
#
#             # if the thread indicator variable is set, stop the thread
#             # and resource camera resources
#             if self.stopped:
#                 self.stream.close()
#                 self.rawCapture.close()
#                 self.camera.close()
#                 return
#
#     def read(self):
#             # return the frame most recently read
#             return self.frame
#
#     def stop(self):
#         # indicate that the thread should be stopped
#         self.stopped = True
#
#
#
# def picamera_fps_test():
#             # created a *threaded *video stream, allow the camera sensor to warmup,
#     # and start the FPS counter
#     print("[INFO] sampling THREADED frames from `picamera` module...")
#     vs = PiVideoStream().start()
#     time.sleep(2.0)
#     fps = FPS().start()
#
#     num_frames = 800
#     display_bool = False
#
#     # loop over some frames...this time using the threaded stream
#     while fps._numFrames < num_frames:
#         # grab the frame from the threaded video stream and resize it
#         # to have a maximum width of 400 pixels
#         frame = vs.read()
#         frame = imutils.resize(frame, width=400)
#
#         # check to see if the frame should be displayed to our screen
#         if display_bool:
#             cv2.imshow("Frame", frame)
#             key = cv2.waitKey(1) & 0xFF
#
#         # update the FPS counter
#         fps.update()
#
#     # stop the timer and display FPS information
#     fps.stop()
#     print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
#     print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
#
#     # do a bit of cleanup
#     cv2.destroyAllWindows()
#     vs.stop()
#


if __name__ == '__main__':
    main()

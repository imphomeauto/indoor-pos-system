
# import the necessary packages
from collections import deque
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "yellow object"
# (or "ball") in the HSV color space, then initialize the
# list of tracked points
colorLower = (169, 100, 100)
colorUpper = (189, 255, 255)
pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
 
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break
	
	cv2.circle(frame, (15,15), 8, (0, 255, 0), -1)
	cv2.circle(frame, (625,15), 8, (0, 255, 0), -1)
	cv2.circle(frame, (15,465), 8, (0, 255, 0), -1)
	cv2.circle(frame, (625,465), 8, (0, 255, 0), -1)

	cv2.circle(frame, (280,15), 8, (0, 255, 0), -1)
	cv2.circle(frame, (15,210), 8, (0, 255, 0), -1)
	cv2.circle(frame, (625,210), 8, (0, 255, 0), -1)
	cv2.circle(frame, (280,210), 8, (0, 255, 0), -1)

	cv2.circle(frame, (130,210), 8, (0, 255, 0), -1)
	cv2.circle(frame, (440,210), 8, (0, 255, 0), -1)

	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
 
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

	print(center)
 	
	# update the points queue
	pts.appendleft(center)

	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()


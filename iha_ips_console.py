# import the necessary packages
from collections import deque
import numpy as np
import argparse
import cv2
import os
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

thex = -1
they = -1

class Pos(threading.Thread):	
	def __init__(self):
		threading.Thread.__init__(self)
		print('started thread')
				
	def run(self):
		global thex
		global they
		ap = argparse.ArgumentParser()
		ap.add_argument("-v", "--video", help="path to the (optional) video file")
		ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
		args = vars(ap.parse_args())
		colorLower = (164, 100, 100)
		colorUpper = (184, 255, 255)
		pts = deque(maxlen=args["buffer"])
		camera = cv2.VideoCapture(0)
		while True:
			(grabbed, frame) = camera.read()
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			mask = cv2.inRange(hsv, colorLower, colorUpper)
			mask = cv2.erode(mask, None, iterations=2)
			mask = cv2.dilate(mask, None, iterations=2)
			cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
			thex = -1
			they = -1
			if len(cnts) > 0:
				c = max(cnts, key=cv2.contourArea)
				((x, y), radius) = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
				thex = int(M["m10"] / M["m00"])
				they = int(M["m01"] / M["m00"])
			#print(thex,they)
						
class MyHTTPServer(HTTPServer):
	def __init__(self, *args, **kwargs):
		HTTPServer.__init__(self, *args, **kwargs)
		self.pos = Pos()
		self.pos.start()

class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		output = "{x:" + str(thex) + ",y:" + str(they) + "}"
		self.wfile.write(output.encode())
		return

if __name__ == '__main__':
	os.system("sudo modprobe bcm2835-v4l2")
	server = MyHTTPServer(('', 8000), RequestHandler)
	print('Starting server at port 8000')
	server.serve_forever()
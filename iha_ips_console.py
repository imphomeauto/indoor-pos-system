# import the necessary packages
from collections import deque
import numpy as np
import argparse
import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

class Pos():
	thex = -1
	they = -1
	
	def __init__(self):
		self.thex = -1
		self.they = -1
		self.method_1()
		
	def method_1(self):
		
		def run(self):
			Thread(target = pos, args = (self,)).start()

		def pos(self):
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
				print(thex,they)
				
		run(self)

class RequestHandler(BaseHTTPRequestHandler):

	def __init__(self, request, client_address, server):
		self.pos = Pos()
		print('Starting positioning')
		BaseHTTPRequestHandler.__init__(self, request, client_address, server)
		
	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		output = "{x:" + str(self.pos.thex) + ",y:" + str(self.pos.they) + "}"
		self.wfile.write(output.encode())
		return

if __name__ == '__main__':
	Pos()
	server = HTTPServer(('', 8000), RequestHandler)
	print('Starting server at port 8000')
	server.serve_forever()
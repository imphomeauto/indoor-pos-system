# import the necessary packages
import cv2
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

rX = -1
rY = -1

class Pos(threading.Thread):	
	def __init__(self):
		threading.Thread.__init__(self)
		print('started thread')
				
	def run(self):
		global rX
		global rY
		colorLower = (164, 100, 100)
		colorUpper = (184, 255, 255)
		camera = cv2.VideoCapture(0)
		while True:
			(grabbed, frame) = camera.read()
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			robotMask = cv2.inRange(hsv, colorLower, colorUpper)
			robotMask = cv2.erode(robotMask, None, iterations=2)
			robotMask = cv2.dilate(robotMask, None, iterations=2)
			robotCenter = cv2.findContours(robotMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
			rX = -1
			rY = -1
			if len(robotCenter) > 0:
				rM = cv2.moments(max(robotCenter, key=cv2.contourArea))
				rX = round(rM["m10"] / rM["m00"] / 10)
				rY = round(rM["m01"] / rM["m00"] / 10)
						
class MyHTTPServer(HTTPServer):
	def __init__(self, *args, **kwargs):
		HTTPServer.__init__(self, *args, **kwargs)
		self.pos = Pos()
		self.pos.start()

class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','application/json')
		self.send_header('Access-Control-Allow-Origin','*')
		self.end_headers()
		output = "{x:" + str(rX) + ",y:" + str(rY) + "}"
		self.wfile.write(output.encode())
		return

if __name__ == '__main__':
	os.system("sudo modprobe bcm2835-v4l2")
	server = MyHTTPServer(('', 8000), RequestHandler)
	print('Starting server at port 8000')
	server.serve_forever()
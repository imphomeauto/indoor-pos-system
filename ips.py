# import the necessary packages
import cv2
import os
import socket
from time import sleep
from threading import Thread

rX = -1
rY = -1

# ouput: 02,11

def server():
	# create TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('ips.local', 8000)
	sock.bind(server_address)
	sock.listen(1)
	while True: 
		connection, client_address = sock.accept()
		try:
			while True:
				message = ('%02d' % rX) + ',' + ('%02d' % rY)
				connection.sendall( message.encode() )
				sleep(.01)
				
		finally:
			# Clean up the connection
			connection.close()

class Pos(Thread):	
	def __init__(self):
		Thread.__init__(self)
		print('started thread')
				
	def run(self):
		global rX
		global rY
		count = 0
		#robotColorLower = (-6, 100, 100) # orange
		#robotColorUpper = (14, 255, 255) # orange
		robotColorLower = (71, 100, 100) # green
		robotColorUpper = (91, 255, 255) # green
		camera = cv2.VideoCapture(0)
		camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
		camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
		#camera.set(cv2.CAP_PROP_FPS, 40)
		while True:
			(grabbed, frame) = camera.read()
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			robotMask = cv2.inRange(hsv, robotColorLower, robotColorUpper)
			robotMask = cv2.erode(robotMask, None, iterations=2)
			robotMask = cv2.dilate(robotMask, None, iterations=2)
			robotCenter = cv2.findContours(robotMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
			rX = -1
			rY = -1
			if len(robotCenter) > 0:
				count = count + 1;
				rM = cv2.moments(max(robotCenter, key=cv2.contourArea))
				rX = round(rM["m10"] / rM["m00"] / 25)
				rY = round(rM["m01"] / rM["m00"] / 25)
				print('%s,%s - %s' % (rX, rY, count))

if __name__ == '__main__':
	os.system("sudo modprobe bcm2835-v4l2")
	pos = Pos()
	pos.start()
	server()

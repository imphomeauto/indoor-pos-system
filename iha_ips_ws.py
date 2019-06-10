# import the necessary packages
import cv2
import os
import socket
from time import sleep
import threading

rX = -1
rY = -1

# ouput: 010,011

def server():
	# create TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# retrieve local hostname
	server_address = ('ips.local', 8000)
	sock.bind(server_address)
	sock.listen(1)
	while True: 
		connection, client_address = sock.accept()
		try:
			while True:
				message = ('%02d' % rX) + ',' + ('%02d' % rY)
				connection.sendall( message.encode() )
				sleep(.04)
				
		finally:
			# Clean up the connection
			connection.close()

class Pos(threading.Thread):	
	def __init__(self):
		threading.Thread.__init__(self)
		print('started thread')
				
	def run(self):
		global rX
		global rY
		robotColorLower = (146, 100, 100) # red
		robotColorUpper = (166, 255, 255) # red
		camera = cv2.VideoCapture(0)
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
				rM = cv2.moments(max(robotCenter, key=cv2.contourArea))
				rX = round(rM["m10"] / rM["m00"] / 25)
				rY = round(rM["m01"] / rM["m00"] / 25)
				print('x: %s - y: %s' % (rX, rY))

if __name__ == '__main__':
	os.system("sudo modprobe bcm2835-v4l2")
	pos = Pos()
	pos.start()
	server()

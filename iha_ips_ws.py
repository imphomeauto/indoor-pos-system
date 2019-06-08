# import the necessary packages
import cv2
import os
import socket
from time import sleep
import threading

rX = -1
rY = -1
dir = '-'

# ouput { x: 10, y: 11, dir: "R" }

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
				message = ('%03d' % rX) + ',' + ('%03d' % rY) + ',' + dir
				connection.sendall( message.encode() )
				sleep(.05)
				
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
		global dir
		robotColorLower = (154, 100, 100) # red
		robotColorUpper = (174, 255, 255) # red
		dirColorLower = (90, 100, 100) # cyan
		dirColorUpper = (110, 255, 255) # cyan
		camera = cv2.VideoCapture(0)
		while True:
			(grabbed, frame) = camera.read()
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			robotMask = cv2.inRange(hsv, robotColorLower, robotColorUpper)
			robotMask = cv2.erode(robotMask, None, iterations=2)
			robotMask = cv2.dilate(robotMask, None, iterations=2)
			robotCenter = cv2.findContours(robotMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
			dirMask = cv2.inRange(hsv, dirColorLower, dirColorUpper)
			dirMask = cv2.erode(dirMask, None, iterations=2)
			dirMask = cv2.dilate(dirMask, None, iterations=2)
			dirCenter = cv2.findContours(dirMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
			rX = -1
			rY = -1
			dir = '-'
			if len(robotCenter) > 0:
				rM = cv2.moments(max(robotCenter, key=cv2.contourArea))
				rX = round(rM["m10"] / rM["m00"] / 10)
				rY = round(rM["m01"] / rM["m00"] / 10)
			if len(dirCenter) > 0 :
				dM = cv2.moments(max(dirCenter, key=cv2.contourArea))
				if round(dM["m10"] / dM["m00"] / 10 - 2) > rX :
					dir = 'R'
				elif round(dM["m10"] / dM["m00"] / 10 + 2) < rX :
					dir = 'L'
				elif round(dM["m01"] / dM["m00"] / 10 - 2) > rY :
					dir = 'D'
				elif round(dM["m01"] / dM["m00"] / 10 + 2) < rY :
					dir = 'U'

if __name__ == '__main__':
	os.system("sudo modprobe bcm2835-v4l2")
	pos = Pos()
	pos.start()
	server()

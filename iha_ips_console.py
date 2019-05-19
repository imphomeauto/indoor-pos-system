# import the necessary packages
import cv2
import os

class Pos():	
	def __init__(self):
		self.run()
		print('started')
				
	def run(self):
		robotColorLower = (169, 100, 100) # red
		robotColorUpper = (189, 255, 255) # red
		dirColorLower = (84, 100, 100) # cyan
		dirColorUpper = (106, 255, 255) # cyan
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
			dX = -1
			dY = -1
			dir = 'R'
			if len(robotCenter) > 0 :
				rM = cv2.moments(max(robotCenter, key=cv2.contourArea))
				rX = round(rM["m10"] / rM["m00"] / 10)
				rY = round(rM["m01"] / rM["m00"] / 10)
			if len(dirCenter) > 0 :
				dM = cv2.moments(max(dirCenter, key=cv2.contourArea))
				dX = round(dM["m10"] / dM["m00"] / 10)
				dY = round(dM["m01"] / dM["m00"] / 10)
				if round(dM["m10"] / dM["m00"] / 10 - 2) > rX :
					dir = 'R'
				elif round(dM["m10"] / dM["m00"] / 10 + 2) < rX :
					dir = 'L'
				elif round(dM["m01"] / dM["m00"] / 10 - 2) > rY :
					dir = 'D'
				elif round(dM["m01"] / dM["m00"] / 10 + 2) < rY :
					dir = 'U'
			print(rX,rY,dX,dY,dir)

if __name__ == '__main__':
	os.system("sudo modprobe bcm2835-v4l2")
	Pos()
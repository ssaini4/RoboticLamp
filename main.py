# **********************************************
# * Robotic Lamp
# * 26 March 2017
# * Saksham Saini, James Jia and Dhruv Diddi
# **********************************************

import cv2
import numpy as np
import math
from imutils.video import VideoStream
import imutils
import argparse
import time
import HandDetection
import glob
# ------------------------ BEGIN ------------------------ #
#Construct the arguent parser and parse the arguments for the camera input to be used
ap = argparse.ArgumentParser()
ap.add_argument("-p","--picamera", type=int, default=1, help="whether or not the Raspberry Pi should be used")
args = vars(ap.parse_args())

#This code is used to setup the camera
camera = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)
capture_done=0
bg_captured=0

keypoints = HandDetection.getKeypoints()

while True:
	img = camera.read()
	HandDetection.getMatch(img,keypoints)
	cv2.imshow('input',img)
	k = cv2.waitKey(10)
	if k == 27:
		break
'''
path = '/home/pi/Desktop/RoboticLamp/Images/*.jpg'
j=0

for i in glob.glob(path):
	img = cv2.imread(i,0 )
	cv2.imshow('input',img)
	drawing = HandDetection.getDrawing(img)
	cv2.imshow('output', drawing)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	#cv2.imwrite('/home/pi/Desktop/RoboticLamp/Features/' +str(j)+'.jpg' , drawing);
	j+=1
print 'hi'
'''

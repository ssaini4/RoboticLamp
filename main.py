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

from neopixel import *
import RecognitionMode as RecogMode
import Colors
import Symbols

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

frameNumber = 0
gestureCounter = np.zeros(10)
gestureList = np.zeros(4)
gestureListCounter = 0

# LED Logic
LED_COUNT      = 64      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 50		 # Start Brightness
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
PIXEL_COLOR    = None

matrix = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
matrix.begin()
RM = RecogMode.RecognitionMode(matrix)

while True:
	RM.enterRecognitionEntrance(average = True)

	img = camera.read()

	if frameNumber<10:
		detectedGesture = HandDetection.getMatch(img,keypoints)
		if "One" in detectedGesture:
			gestureCounter[1] += 1
			print 'One'
		elif "Two" in detectedGesture:
			gestureCounter[2] += 1
			print 'Two'

		elif "Five" in detectedGesture:
			gestureCounter[3] += 1
			print 'Five'
		frameNumber += 1
	else:

		'''
		This is where you need to make changes
		'''
		gesture = np.argmax(gestureCounter)
		print 'Max gesture: ' + str(gesture)
		gestureList[gestureListCounter] = gesture
		if len(set(gestureList)) == 1:
			print 'executing gesture...' + str(gesture)
			#Execute the gesture based on the gesture NUmber here
			
			print "it works!"
			return

		else:
			maxElement = max(gestureList)
			maxElementCount = gestureList.tolist().count(maxElement)
			print 'gesture Recognised..' + str(25*maxElementCount) +'%'	
			#Status of gesture recognition here
			curSymbol = None
			curCount = None

			if maxElement == 1:
				newSymbol = Symbols.S_1
			elif maxElement == 2:
				newSymbol = Symbols.S_2
			else
				newSymbol = Symbols.S_5

			if newSymbol != curSymbol:
				curSymbol = newSymbol
				curCount = maxElementCount
				RM.displaySymbol(Symbols.processSymbol(curSymbol), maxElementCount)
			else:
				if maxElementCount > curCount:
					RM.downLevel()
				elif maxElementCount < curCount:
					RM.upLevel()
				else:
					print "same level, no change"

				curCount = maxElementCount


		gestureListCounter += 1
		gestureListCounter %= 5
			
		gestureCounter = np.zeros(10)
		frameNumber = 0

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

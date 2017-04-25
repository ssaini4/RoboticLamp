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

import pexpect
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


frameNumber = 0
gestureCounter = np.zeros(10)
detectedGesture = np.zeros(4)
gestureList = np.zeros(4)
gestureListCounter = 0

#Start subprocess
led = pexpect.spawn('sudo PYTHONPATH=".build/lib.linux-armv6l-2.7" python LEDLogic.py')
print "initializing LEDs"
time.sleep(9)
print "entering recognition mode"
scrub = "RM.enterRecognitionMode(average = True)\n"
led.send(scrub)


#Get the classifiers
palm = cv2.CascadeClassifier('../haar/palm.xml')
fist = cv2.CascadeClassifier('../haar/fist.xml')
hand = cv2.CascadeClassifier('../haar/hand.xml')
swag = cv2.CascadeClassifier('../haar/cascade.xml')
smile = cv2.CascadeClassifier('../haar/smile.xml')
one = cv2.CascadeClassifier('../haar/one.xml')

def detectFeature(model, img):
	return model.detectMultiScale(gray,1.3,5)



while True:
	gray = camera.read()
	cv2.imshow('input',gray)
	gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
	
	isPalm = detectFeature(palm,gray)
	isFist = detectFeature(fist,gray)
	isOne = detectFeature(one, gray)
	isSwag = detectFeature(swag,gray)
	if len(isPalm) == 2:
		detectedGesture[0] = 1
		print 'Two Hands up'
	elif len(isPalm) == 1:
		detectedGesture[1]= 1
		print "One Hand up"
	if len(isFist) == 2:
		detectedGesture[2] = 1
		print 'Two Fist detected'
	elif len(isFist) == 1:
		detectedGesture[3] = 1
		print 'one fist detected'
	
	for (hx,hy,hw,hh) in isPalm:
		cv2.rectangle(gray,(hx,hy),(hx+hw,hy+hh),(0,255,0),2)
	for (hx,hy,hw,hh) in isFist:
		cv2.rectangle(gray,(hx,hy),(hx+hw,hy+hh),(0,255,0),2)
	#for (hx,hy,hw,hh) in isSwag:
	#	cv2.rectangle(gray,(hx,hy),(hx+hw,hy+hh),(0,255,0),2)
	

	if (led.stdout.closed):
                print (led.stdout)


	if frameNumber<10:
		if detectedGesture[0] == 1:
			gestureCounter[0] += 1
			print 'One'
		if detectedGesture[1] == 1:
			gestureCounter[1] += 1
			print 'Two'
		if detectedGesture[2] == 1:
			gestureCounter[2] += 1
			print 'Three'
		if detectedGesture[3] == 1:
			gestureCounter[3] += 1
			print "Four"
		frameNumber += 1
	else:

	
		#This is where you need to make changes
	
		gesture = np.argmax(gestureCounter)
		gestureList[gestureListCounter] = gesture
		if len(set(gestureList)) == 1:
			print 'executing gesture...' + str(gesture)
			#Execute the gesture based on the gesture NUmber here
			
			print "it works!"

		else:
			maxElement = max(gestureList)
			maxElementCount = gestureList.tolist().count(maxElement)
			print 'gesture Recognised..' + str(25*maxElementCount) +'%'	
			#Status of gesture recognition here
			curSymbol = None
			curCount = None

			if maxElement == 0:
				#Brightness Up
				newSymbol = "Symbols.S_1"
			elif maxElement == 1:
				#Brightness Down
				newSymbol = "Symbols.S_2"
			elif maxElement == 2:
				#Clock
				newSymbol = "Symbols.S_5"
			elif maxElement == 3:
				#Motors
				newSymbol = "Symbols.S_4"
				
			if newSymbol != curSymbol:
				curSymbol = newSymbol
				curCount = maxElementCount
				inputStr = "RM.displaySymbol(Symbols.processSymbol(" + curSymbol + ")," + str(maxElementCount) + ")\n"
				print inputStr
				led.send(inputStr)
			else:
				if maxElementCount > curCount:
					led.send("RM.downLevel()\n")
				elif maxElementCount < curCount:
					led.send("RM.upLevel()\n")
				else:
					print "same level, no change"

				curCount = maxElementCount


		gestureListCounter += 1
		gestureListCounter %= 4
			
		gestureCounter = np.zeros(10)
		frameNumber = 0
	detectedGesture = np.zeros(4)

	
	cv2.imshow('img',gray)
	k = cv2.waitKey(10)
	if k == 27:
		break

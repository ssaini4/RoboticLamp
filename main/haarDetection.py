# **********************************************
# * Robotic Lamp
# * 26 March 2017
# * Saksham Saini, James Jia and Dhruv Diddi
# **********************************************

import cv2
import sys
sys.path.append('/home/pi/Desktop/RoboticLamp/main/Adafruit_Python_PCA9685/Adafruit_PCA9685')
import numpy as np
import math
from imutils.video import VideoStream
import imutils
import argparse
import time
import HandDetection
import glob
import pexpect
import shlex
import subprocess
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
detectedGesture = np.zeros(5)
gestureList = np.zeros(5)
gestureListCounter = 0

#Start subprocess
led = pexpect.spawn('sudo PYTHONPATH=".build/lib.linux-armv6l-2.7" python LEDLogic.py')
print "initializing LEDs"
time.sleep(5)
print "entering recognition mode"
scrub = "RM.enterRecognitionMode(average = True)\n"
led.send(scrub)


#Get the classifiers
palm = cv2.CascadeClassifier('../haar/palm.xml')
fist = cv2.CascadeClassifier('../haar/fist.xml')
hand = cv2.CascadeClassifier('../haar/hand.xml')
swag = cv2.CascadeClassifier('../haar/banana_classifier.xml')
smile = cv2.CascadeClassifier('../haar/smile.xml')
one = cv2.CascadeClassifier('../haar/new.xml')

def detectFeature(model, img):
	return model.detectMultiScale(gray,1.3,5)

brightUpBool = False
brightDownBool = False
clockBool = False
rotatorBool = False

while True:
	gray = camera.read()
	cv2.imshow('input',gray)
	gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
	gray = cv2.flip(gray,0)
	isPalm = detectFeature(palm,gray)
	isFist = detectFeature(fist,gray)
	isOne = detectFeature(one, gray)
	isSwag = detectFeature(swag,gray)
	if len(isSwag) == 1:
		detectedGesture[0] = 1
		print 'Swag up'
	elif len(isPalm) == 1:
		detectedGesture[1]= 1
		print "One Hand up"
	if len(isOne) == 1:
		detectedGesture[2] = 1
		print 'One detected'
	elif len(isFist) == 1:
		detectedGesture[3] = 1
		print 'one fist detected'
	else:
		detectedGesture[4] = 1
	
	for (hx,hy,hw,hh) in isPalm:
		cv2.rectangle(gray,(hx,hy),(hx+hw,hy+hh),(0,255,0),2)
	for (hx,hy,hw,hh) in isFist:
		cv2.rectangle(gray,(hx,hy),(hx+hw,hy+hh),(0,255,0),2)
	for (hx,hy,hw,hh) in isSwag:
		cv2.rectangle(gray,(hx,hy),(hx+hw,hy+hh),(0,255,0),2)
	

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
		if detectedGesture[4] == 1:
			gestureCounter[4] += 1
			print "no gesture"
		frameNumber += 1
	else:
		#This is where you need to make changes
		
		realGestures = gestureCounter[0:4] # non-empty gestures
		if max(realGestures) >= 2:
			#Gesture recognized
			gesture = np.argmax(realGestures)
		else:
			gesture = 4
		
		#gestureList[gestureListCounter] = gesture
		
		# This does EXIT commands: entered command but no gesture detected
		if (brightUpBool or brightDownBool or clockBool or rotatorBool) and gesture == 4:
			print "EXIT"
			
			print "up = " + str(brightUpBool)
			print "down = " + str(brightDownBool)
			
			print str(gesture)
			
			time.sleep(5)
			if brightUpBool:
				print "Exiting Brightness!"
				inputStr = "BC.exitControlMode()\n"
				brightUpBool = False
				
			elif brightDownBool:
				print "Exiting Brightness!"
				inputStr = "BC.exitControlMode()\n"
				brightDownBool = False
				
			elif clockBool:
				print "Exiting Time!"
				inputStr = "CLK.exitLEDClock()\n"
				clockBool = False
				
			elif rotatorBool:
				print "Exiting Rotating Color!"
				inputStr = "ROT.exitColorRotator()\n"
				rotatorBool = False
				
			else:
				pass
				#Incorrect gesture found
				#pretend nothing happened i guess
				
			led.send(inputStr)
		
		# This does ACTION commands entered command and gesture still detected
		elif (brightUpBool or brightDownBool or clockBool or rotatorBool) and gesture != 4:
			
			if brightUpBool and gesture == 0:
				print "Increasing Brightness!"
				inputStr = "BC.upLevel()\n"
				
			elif brightDownBool and gesture == 1:
				print "Decreasing Brightness!"
				inputStr = "BC.downLevel()\n"
				
			elif clockBool and gesture == 2:
				print "Showing Time for 2 seconds!"
				inputStr = "CLK.showTime()\n"
				
			elif rotatorBool and gesture == 3:
				print "Rotating Color!"
				inputStr = "ROT.nextColor()\n"
			else:
				pass
				#Incorrect gesture found
				#pretend nothing happened i guess
			
			led.send(inputStr)
			
		# This does ENTER commands
		else:

			print 'gesture Recognised..'	
			#Status of gesture recognition here
			curSymbol = None
			curCount = None
			noLock = False

			if gesture == 0:
				#Brightness Up
				print "Entering Brightness Control - up"
				inputStr = "BC.enterControlMode()\n"
				brightUpBool = True
				#newSymbol = "Symbols.SYMBOL_B"
			
			elif gesture == 1:
				#Brightness Down
				print "Entering Brightness Control - down"
				inputStr = "BC.enterControlMode()\n"
				brightDownBool = True
			
			elif gesture == 2:
				#Clock
				print "Entering Clock"
				newSymbol = "Symbols.SYMBOL_T"
				inputStr = "CLK.enterLEDClock()\n"
				clockBool = True
				
			elif gesture == 3:
				#Color Rotation
				print "Entering Color Rotation"
				newSymbol = "Symbols.SYMBOL_C"
				inputStr = "ROT.enterColorRotator()\n"
				rotatorBool = True
				
				#Motor command
				proc = subprocess.Popen(shlex.split('sudo python simpletest.py'))
				proc.communicate()
			
			elif gesture == 4:
				noLock = True
				newSymbol = "derp"
				inputStr = "RM.noLock()\n"
				
			led.send(inputStr)

		gestureListCounter += 1
		gestureListCounter %= 4
			
		gestureCounter = np.zeros(10)
		frameNumber = 0
	detectedGesture = np.zeros(5)

	
	cv2.imshow('img',gray)
	k = cv2.waitKey(10)
	if k == 27:
		break

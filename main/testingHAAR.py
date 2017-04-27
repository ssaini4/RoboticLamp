import math
import numpy as np
import imutils
import argparse
import time
import HandDetection
import cv2
import sys

camera = cv2.VideoCapture(0)
time.sleep(2.0)

capture_done=0
bg_captured=0


frameNumber = 0
gestureCounter = np.zeros(10)
detectedGesture = np.zeros(5)
gestureList = np.zeros(5)
gestureListCounter = 0

palm = cv2.CascadeClassifier('../haar/palm.xml')
fist = cv2.CascadeClassifier('../haar/fist.xml')
hand = cv2.CascadeClassifier('../haar/hand.xml')
swag = cv2.CascadeClassifier('../haar/cascadenewnewnew.xml')
smile = cv2.CascadeClassifier('../haar/smile.xml')
one = cv2.CascadeClassifier('../haar/new.xml')

def detectFeature(model, img):
	return model.detectMultiScale(gray,1.3,5)

brightUpBool = False
brightDownBool = False
clockBool = False
rotatorBool = False

while camera.isOpened():
	_,gray = camera.read()
	cv2.imshow('input',gray)
                        #displaying the frames
	gray = cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(5,5),0)
	ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	#gray = cv2.flip(gray,0)
	isPalm = detectFeature(hand,thresh1)
	isFist = detectFeature(fist,thresh1)
	isOne = detectFeature(one, thresh1)
	isSwag = detectFeature(swag,thresh1)
	isSmile = detectFeature(smile,gray)
	cv2.imshow('thresh',thresh1)

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
	elif len(isSmile) == 1:
		print 'smile!'
	else:
		detectedGesture[4] = 1
	
	for (hx,hy,hw,hh) in isPalm:
		pass
		#cv2.rectangle(gray,(hx,hy),(hx+hw,hy+hh),(0,255,0),2)
	for (hx,hy,hw,hh) in isFist:
		
		cv2.rectangle(gray,(hx,hy),(hx+hw,hy+hh),(0,255,0),2)
	for (hx,hy,hw,hh) in isSwag:
		
		cv2.rectangle(gray,(hx,hy),(hx+hw,hy+hh),(0,255,0),2)

	cv2.imshow('img',gray)
	k = cv2.waitKey(1)
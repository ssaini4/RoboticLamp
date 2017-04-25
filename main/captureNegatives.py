import cv2
import numpy as np
import math
from imutils.video import VideoStream
import imutils
import argparse
import time
#Construct the arguent parser and parse the arguments for the camera input to be used
ap = argparse.ArgumentParser()
ap.add_argument("-p","--picamera", type=int, default=1, help="whether or not the Raspberry Pi should be used")
args = vars(ap.parse_args())

#This code is used to setup the camera


i=0
while True:
	gray = camera.read()
	cv2.imshow('input',gray)
	cv2.imwrite('./negatives/'+str(i)+'.jpg',gray)
	i+=1

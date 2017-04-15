import cv2
import numpy as np
import math
from imutils.video import VideoStream
import imutils
import argparse
import time
import glob
def getDrawing(img):
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	'''
	gray=img
	orb = cv2.ORB()
	kp = orb.detect(gray, None)
	kp, des = orb.compute(gray,kp)
	
	gray = cv2.drawKeypoints(img, kp, None,color=(255,255,255),flags=0)
	gray = cv2.cvtColor(gray,cv2.COLOR_BGR2GRAY)
	'''
	blur = cv2.GaussianBlur(gray,(5,5),0)
	ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

	contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	drawing = np.zeros(img.shape,np.uint8)

	max_area=0

	for i in range(len(contours)):
		cnt=contours[i]
		area = cv2.contourArea(cnt)
		if(area>max_area):
			max_area=area
			ci=i
	cnt=contours[ci]
	hull = cv2.convexHull(cnt)
	moments = cv2.moments(cnt)
	if moments['m00']!=0:
		cx = int(moments['m10']/moments['m00']) # cx = M10/M00
		cy = int(moments['m01']/moments['m00']) # cy = M01/M00

	centr=(cx,cy)       
	cv2.circle(img,centr,5,[0,0,255],2)       
	cv2.drawContours(drawing,[cnt],0,(0,255,0),2) 
	cv2.drawContours(drawing,[hull],0,(0,0,255),2) 
		  
	cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
	hull = cv2.convexHull(cnt,returnPoints = False)
	
	if(1):
	   defects = cv2.convexityDefects(cnt,hull)
	   mind=0
	   maxd=0
	   if defects is not None:   
		   for i in range(defects.shape[0]):
				s,e,f,d = defects[i,0]
				start = tuple(cnt[s][0])
				end = tuple(cnt[e][0])
				far = tuple(cnt[f][0])
				
				if far==2:
					print 'One finger'
				elif far ==3:
					print 'Two fingers'
				elif far >=4:
					print 'four finger'
				dist = cv2.pointPolygonTest(cnt,centr,True)
				
				print start,end, far,dist
				cv2.line(img,start,end,[0,255,0],2)
				
				cv2.circle(img,far,5,[0,0,255],-1)
	   i=0
	return drawing
	
def getMatch(gray):
	orb = cv2.ORB()
	kp = orb.detect(gray, None)
	kp, des = orb.compute(gray,kp)
	path = '/home/pi/Desktop/RoboticLamp/Images/*.jpg'
	j=0
	
	FLANN_INDEX_KDTREE = 0
	index_params =dict(algorithm = 6, table_number = 6, 
						key_size=12, multi_probe_level = 1)
	search_params = dict(check=50)

	flann = cv2.FlannBasedMatcher(index_params, search_params)
	
	maxMatches = 0
	maxLabel = ''
		
	for i in glob.glob(path):
		img = cv2.imread(i,0 )
		kp2 = orb.detect(img,None)
		kp2, des2 = orb.compute(img,kp2)
		
		matches =flann.knnMatch(des,des2,k=2)
		matchesMask = [m[0] for m in matches if len(m) ==2 
						and m[0].distance <m[1].distance * 0.75]
				
		sumMatches = len(matchesMask)
		if(sumMatches > maxMatches):
			maxMatches = sumMatches
			maxLabel = i
			
	print maxLabel

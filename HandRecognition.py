import cv2
import numpy as np
import math
from imutils.video import VideoStream
import imutils
import argparse
import time
import glob

def getKeypoints():
	path = '/home/pi/Desktop/RoboticLamp/Images/*.jpg'
	j=0
	orb = cv2.ORB()
	descriptors = []
	for i in glob.glob(path):
		img = cv2.imread(i,0 )
		kp2 = orb.detect(img,None)
		kp2, des = orb.compute(img, kp2)
		descriptors.append((kp2,des, i))
		
	return descriptors
	


def drawMatches(img1, kp1, img2, kp2, matches):
    """
    My own implementation of cv2.drawMatches as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0

    This function takes in two images with their associated 
    keypoints, as well as a list of DMatch data structure (matches) 
    that contains which keypoints matched in which images.

    An image will be produced where a montage is shown with
    the first image followed by the second image beside it.

    Keypoints are delineated with circles, while lines are connected
    between matching keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint matching algorithm
    """

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)


    # Show the image
    cv2.imshow('Matched Features', out)
    cv2.waitKey(0)
    cv2.destroyWindow('Matched Features')

    # Also return the image if you'd like a copy
    return out
    

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
	
def getMatch(gray, keypoints):
	orb = cv2.ORB()
	kp = orb.detect(gray, None)
	kp, des = orb.compute(gray,kp)
	
	FLANN_INDEX_KDTREE = 0
	index_params =dict(algorithm = 6, table_number = 6, 
						key_size=12, multi_probe_level = 1)
	search_params = dict(check=50)

	flann = cv2.FlannBasedMatcher(index_params, search_params)
	
	maxMatches = 0
	maxLabel = ''
	for i in keypoints:
		kp2,des2, label = i		
		matches =flann.knnMatch(des,des2,k=2)
		matchesMask = [m[0] for m in matches if len(m) ==2 
						and m[0].distance <m[1].distance * 0.7]

		sumMatches = len(matchesMask)
		if(sumMatches > maxMatches):
			maxMatches = sumMatches
			maxLabel = label
			
		
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

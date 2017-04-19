import cv2
import numpy as np
import math
from imutils.video import VideoStream
import imutils
import argparse
import time

bg_captured=0
capture_done=0
b_bg = []
g_bg = []
r_bg = []
interrupt = 0


def recognize_hand(frame):
	interrupt=cv2.waitKey(10)

	# Capture hand by pressing 'c'
	if interrupt & 0xFF == ord('c'):
		if(bg_captured):
			capture_done=1
			b,g,r= get_dft(frame)
			b = b - b_bg
			g = g - g_bg
			r = r - r_bg
			ib = get_inverse(b)
			ig = get_inverse(g)
			ir = get_inverse(r)
			img = cv2.merge((b,g,r))
			return img
	# Capture background by pressing 'b'
	elif interrupt & 0xFF == ord('b'):
		b_bg, g_bg, r_bg = get_dft(frame)
		bg_captured=1
		return frame, "Place hand inside boxes and press 'c' to capture hand histogram"
	else:
		return frame, "Remove hand from the frame and press 'b' to capture background"
	
#def remove_bg(frame):
def get_dft(frame):
	image = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	fast = cv2.ORB_create()
	
	kp = fast.detect(image, None)
	kps,eds = fast.compute(image,kp)
	image[:] = (0)
	img2 = cv2.drawKeypoints(image, kps,None, color=(255,0,0))
	return img2


def get_inverse(img):
	img_back = cv2.idft(img)
	return img_back

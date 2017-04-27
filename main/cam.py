import cv2
import numpy as np
import time
import argparse
from imutils.video import VideoStream

PI = True

firstBox = None
secondBox = None
thirdBox = None
fourthBox = None

def inBetweenBox(point):
    (x,y) = point
    x = x

    (leftX, upY) = firstBox[0]
    (rightX, downY) = firstBox[1]

    if leftX <= x <= rightX:
        if upY <= y <= downY:
            return 0


    (leftX, upY) = secondBox[0]
    (rightX, downY) = secondBox[1]

    if leftX <= x <= rightX:
        if upY <= y <= downY:
            return 1


    (leftX, upY) = thirdBox[0]
    (rightX, downY) = thirdBox[1]

    if leftX <= x <= rightX:
        if upY <= y <= downY:
            return 2            
    

    (leftX, upY) = fourthBox[0]
    (rightX, downY) = fourthBox[1]

    if leftX <= x <= rightX:
        if upY <= y <= downY:
            return 3

    return -1

def cvFind(cap):
    noCount = 0
    badContours = 0
    while( cap.isOpened() ) :
        ret,oldimg = cap.read()
        oldimg = cv2.flip(oldimg, 1)
        img = oldimg[int(oldimg.shape[0] / 2):oldimg.shape[0], 0:oldimg.shape[1]]
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)
        ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
      
        contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        drawing = np.zeros(img.shape,np.uint8)

        max_area=0
       
    ##########

        downY = int(img.shape[0])
        upY = int(0)

        global firstBox, secondBox, thirdBox, fourthBox

        fifthX = int(img.shape[1])
        fourthX = int(fifthX * 0.75)
        thirdX = int(fifthX * 0.5)
        secondX = int(fifthX * 0.25)
        firstX = int(fourthX * 0)

        DIVIDE = 15

        #NW frame
        firstBox = ((firstX, upY), (secondX-DIVIDE, downY))
        cv2.rectangle(img, firstBox[0], firstBox[1], (255, 0, 0), 2)

        #NE frame
        secondBox = ((secondX + DIVIDE, upY), (thirdX - DIVIDE, downY))
        cv2.rectangle(img, secondBox[0], secondBox[1], (255, 0, 0), 2)

        #SW frame
        thirdBox = ((thirdX + DIVIDE, upY), (fourthX-DIVIDE, downY))
        cv2.rectangle(img, thirdBox[0], thirdBox[1], (255, 0, 0), 2)

        #SE frame
        fourthBox = ((fourthX+DIVIDE, upY), (fifthX, downY))
        cv2.rectangle(img, fourthBox[0], fourthBox[1], (255, 0, 0), 2)

        for i in range(len(contours)):
                cnt=contours[i]
                area = cv2.contourArea(cnt)
                if(area>max_area):
                    max_area=area
                    ci=i
        cnt = contours[ci]
        drawing = np.zeros(img.shape, np.uint8)
        hull = cv2.convexHull(cnt)
        moments = cv2.moments(cnt)
        if moments['m00']!=0:
                    cx = int(moments['m10']/moments['m00']) # cx = M10/M00
                    cy = int(moments['m01']/moments['m00']) # cy = M01/M00
                  
        centr=(cx,cy)       
        #cv2.circle(img,centr,5,[0,0,255],2)       
        cv2.drawContours(drawing,[cnt],0,(0,255,0),2) 
        cv2.drawContours(drawing,[hull],0,(0,0,255),2) 
              
        cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        hull = cv2.convexHull(cnt,returnPoints = False)
        
        Boxes = [0] * 4

        defects = cv2.convexityDefects(cnt,hull)
        mind=0
        maxd=0
        if defects != None:
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                dist = cv2.pointPolygonTest(cnt,centr,True)
                cv2.line(img,start,end,[0,255,0],2)
                
                cv2.circle(img,far,5,[0,0,255],-1)

                boxNum = inBetweenBox(far)
                if boxNum != -1:
                    Boxes[boxNum] = Boxes[boxNum] + 1

            maxFingers = np.argmax(Boxes)
            #print Boxes[maxFingers]
            if Boxes[maxFingers] >= 3:
                print "BOX " + str(maxFingers) + " SUCCESS!"
                return maxFingers
                #time.sleep(1)
                #return maxFingers
            else:
                return -1
                badContours = badContours + 1
                if badContours >= 10:
                    print "nothing for 10 frames"
                    return -1
                    badContours = 0

            #print(i)
            i=0
        else:
            return -1
            noCount = noCount + 1
            if noCount >= 10: # 10 frames no defects
                print "nothing for 10 frames"#return -1
                return -1
                noCount = 0

        cv2.imshow('output',drawing)
        cv2.imshow('input',oldimg)
                    
        k = cv2.waitKey(10)
        if k == 27:
            break

if PI:
    ap = argparse.ArgumentParser()
    ap.add_argument("-p","--picamera", type=int, default=1, help="whether or not the Raspberry Pi should be used")
    args = vars(ap.parse_args())
    #This code is used to setup the camera
    camera = VideoStream(usePiCamera=args["picamera"] > 0).start()

else:
    cap = cv2.VideoCapture(0)

while True:
    cvFind(cap)
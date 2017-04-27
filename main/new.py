import cv2
import numpy as np
import copy
import math
import time

# Environment:
# OS    : Mac OS EL Capitan
# python: 3.5
# opencv: 2.4.13

# parameters
cap_region_x_begin=0.5  # start point/total width
cap_region_y_end=1  # start point/total width
threshold = 60  #  BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 50

# variables
isBgCaptured = 0   # bool, whether the background captured
triggerSwitch = False  # if true, keyborad simulator works

NWbox = None
NEbox = None
SWbox = None
SEbox = None

startX = None
def printThreshold(thr):
    print("! Changed threshold to "+str(thr))


def removeBG(frame):
    fgmask = bgModel.apply(frame)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    res = cv2.bitwise_and(frame, frame, mask=fgmask)
    return res

# 0 = NW
# 1 = NE
# 2 = SW
# 3 = SE
def inBetweenBox(point):
    (x,y) = point
    print (x+startX, y)
    x = x + startX

    (leftX, upY) = NWbox[0]
    (rightX, downY) = NWbox[1]
    print NWbox[0]
    print NWbox[1]

    if leftX <= x <= rightX:
        if upY <= y <= downY:
            print "HELLO"
            return 0


    (leftX, upY) = NEbox[0]
    (rightX, downY) = NEbox[1]

    if leftX <= x <= rightX:
        if upY <= y <= downY:
            return 1


    (leftX, upY) = SWbox[0]
    (rightX, downY) = SWbox[1]

    if leftX <= x <= rightX:
        if upY <= y <= downY:
            return 2            
    

    (leftX, upY) = SEbox[0]
    (rightX, downY) = SEbox[1]

    if leftX <= x <= rightX:
        if upY <= y <= downY:
            return 3

    return -1

def calculateFingers(res,drawing):  # -> finished bool, cnt: finger count
    #  convexity defect

    # 0 - NW
    # 1 - NE
    # 2 - SW
    # 3 - SE
    Boxes = [0] * 4

    hull = cv2.convexHull(res, returnPoints=False)
    if len(hull) > 3:
        defects = cv2.convexityDefects(res, hull)
        if type(defects) != type(None):  # avoid crashing.   (BUG not found)

            cnt = 0
            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # cosine theorem
                if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
                    cnt += 1
                    cv2.circle(drawing, far, 8, [211, 84, 0], -1)

                    boxNum = inBetweenBox(far)
                    if boxNum != -1:
                        Boxes[boxNum] = Boxes[boxNum] + 1 

            if cnt > 0:
                print str(cnt)
                maxFingers = np.argmax(Boxes)
                print Boxes[maxFingers]
                if Boxes[maxFingers] >= 3:
                    return maxFingers
            return -1
    return -1


# Camera
camera = cv2.VideoCapture(0)
camera.set(10,200)
cv2.namedWindow('trackbar')
cv2.createTrackbar('trh1', 'trackbar', threshold, 100, printThreshold)


while camera.isOpened():
    ret, frame = camera.read()
    threshold = cv2.getTrackbarPos('trh1', 'trackbar')
    frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
    frame = cv2.flip(frame, 1)  # flip the frame horizontally
    #cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
     #            (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)

    leftX = int(cap_region_x_begin * frame.shape[1])
    startX = leftX
    rightX = int(frame.shape[1])
    midX = int(leftX + ((rightX - leftX) / 2))

    upY = 0
    downY = int(cap_region_y_end * frame.shape[0])
    midY = int(upY + ((downY - upY) / 2))

    # print str(leftX)
    # print str(midX)
    # print str(rightX)

    # print str(upY)
    # print str(midY)
    # print str(downY)

    #NW frame
    NWbox = ((leftX, upY), (midX-50, midY-50))
    cv2.rectangle(frame, NWbox[0], NWbox[1], (255, 0, 0), 2)

    #NE frame
    NEbox = ((midX+50, upY), (rightX, midY-50))
    cv2.rectangle(frame, NEbox[0], NEbox[1], (255, 0, 0), 2)

    #SW frame
    SWbox = ((leftX, midY+50), (midX-50, downY))
    cv2.rectangle(frame, SWbox[0], SWbox[1], (255, 0, 0), 2)

    #SE frame
    SEbox = ((midX+50, midY+50), (rightX, downY))
    cv2.rectangle(frame, SEbox[0], SEbox[1], (255, 0, 0), 2)
    
    # cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
    #              (frame.shape[1] / 2, int(cap_region_y_end * frame.shape[0])/2), (255, 0, 0), 2)

    # print (str(frame.shape[1] / 2)) + "," + str(int(cap_region_y_end * frame.shape[0])/2)

    cv2.imshow('original', frame)

    #  Main operation
    if isBgCaptured == 1:  # this part wont run until background captured
        img = removeBG(frame)
        img = img[0:int(cap_region_y_end * frame.shape[0]),
                    int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI
        cv2.imshow('mask', img)

        # convert the image into binary image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)
        cv2.imshow('blur', blur)
        ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
        cv2.imshow('ori', thresh)


        # get the coutours
        thresh1 = copy.deepcopy(thresh)
        contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        length = len(contours)
        maxArea = -1
        if length > 0:
            for i in range(length):  # find the biggest contour (according to area)
                temp = contours[i]
                area = cv2.contourArea(temp)
                if area > maxArea:
                    maxArea = area
                    ci = i

            res = contours[ci]
            hull = cv2.convexHull(res)
            drawing = np.zeros(img.shape, np.uint8)
            cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
            cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)

            location = calculateFingers(res,drawing)

            if location == 0:
                print "NW SUCCESS"
                #time.sleep(1)
            elif location == 1:
                print "NE SUCCESS"
                #time.sleep(1)
            elif location == 2:
                print "SW SUCCESS"
                #time.sleep(1)
            elif location == 3:
                print "SE SUCCESS"
                #time.sleep(1)
            else:
                pass

        cv2.imshow('output', drawing)

    # Keyboard OP
    k = cv2.waitKey(10)
    if k == 27:  # press ESC to exit
        break
    elif k == ord('b'):  # press 'b' to capture the background
        bgModel = cv2.BackgroundSubtractorMOG2(0, bgSubThreshold)
        isBgCaptured = 1
        print '!!!Background Captured!!!'
    elif k == ord('r'):  # press 'r' to reset the background
        bgModel = None
        triggerSwitch = False
        isBgCaptured = 0
        print '!!!Reset BackGround!!!'
    elif k == ord('n'):
        triggerSwitch = True
        print '!!!Trigger On!!!'

import cv2
import numpy as np
from shapedetector import ShapeDetector

cap = cv2.VideoCapture(0)

def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('Setting')
cv2.resizeWindow('Setting',350,400)

# Starting with 100's to prevent error while masking
h,s,v = 100,100,100

# Creating track bar
cv2.createTrackbar('h_L', 'Setting',0,179,nothing)
cv2.createTrackbar('s_L', 'Setting',0,255,nothing)
cv2.createTrackbar('v_L', 'Setting',0,255,nothing)

cv2.createTrackbar('h_H', 'Setting',179,179,nothing)
cv2.createTrackbar('s_H', 'Setting',255,255,nothing)
cv2.createTrackbar('v_H', 'Setting',255,255,nothing)

while (1):

    _, frame = cap.read()
    img = frame
    #img = cv2.imread('top1-process.png')
    #frame = img
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h_L = cv2.getTrackbarPos('h_L','Setting')
    s_L = cv2.getTrackbarPos('s_L','Setting')
    v_L = cv2.getTrackbarPos('v_L','Setting')

    h_H = cv2.getTrackbarPos('h_H','Setting')
    s_H = cv2.getTrackbarPos('s_H','Setting')
    v_H = cv2.getTrackbarPos('v_H','Setting')

    # red
    # InRange_L = np.array([30, 217, 174], dtype=np.uint8)
    # InRange_H= np.array([180, 255, 255], dtype=np.uint8)

    #test red range varies
    #InRange_L = np.array([0, 100, 100], dtype=np.uint8)
    #InRange_H= np.array([5, 255, 255], dtype=np.uint8)
    # yellow
    # InRange_L = np.array([17, 88, 244], dtype=np.uint8)
    # InRange_H= np.array([53, 201, 255], dtype=np.uint8)

    # green
    # InRange_L = np.array([53, 73, 0], dtype=np.uint8)
    # InRange_H= np.array([92, 255, 255], dtype=np.uint8)

    # find color by trackbar
    InRange_L = np.array([h_L,s_L,v_L])
    InRange_H = np.array([h_H,s_H,v_H])

    yellow = cv2.inRange(hsv, InRange_L, InRange_H)

    mask = cv2.bitwise_and(frame, frame, mask=yellow)

    # Threshold image for find contour
    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5, 5), np.uint8)
    gray = cv2.dilate(gray,kernel,iterations=3)
    cv2.imshow('gray',gray)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 50, 250, cv2.THRESH_BINARY)[1]
    cv2.imshow('T', thresh)

    # find contour
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(cnt, contours, -1, (0, 255, 0), 2)

    sd = ShapeDetector()
    dst = img
    # find center of object
    for c in range(len(contours)):
        M = cv2.moments(contours[c])
        rect = cv2.minAreaRect(contours[c])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        angle = int(rect[2])  # Box2D get (x,y),(width,height),theta
        cv2.drawContours(dst, [box], 0, (0, 0, 255), 2)

        # shape = sd.detect(c)

        cx = 0
        cy = 0
        if (M['m00'] != 0):
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

        cv2.circle(dst, (cx, cy), 7, (0, 0, 0), -1)
        Pos = str(cx) + ',' + str(cy) + ',' + str(angle)
        cv2.putText(dst, Pos, (cx - 30, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # cv2.imshow('frame', frame)
    cv2.imshow('yellow', yellow)
    cv2.imshow('mask', mask)
    cv2.imshow('img', img)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
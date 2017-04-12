import socket
import time
import cv2
import numpy as np
from shapedetector import ShapeDetector
from enum import Enum
from switch import Switch

class Color(Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2
    BLUE = 3
    ORANGE = 4

class control:
    def move(self,x,y,z):
        x = str(x / 1000.0)
        y = str(y / 1000.0)
        z = str(z / 1000.0)
        ro = str(1.47)
        pi = str(0.60)
        ya = str(-0.635)
        print(x,y,z,ro,pi,ya)
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=0.4,v=4)" + "\n"
        s.send(mm.encode('utf-8'))
        #self.s.close()

    def move2Jig(self,x,y,z,ro,pi,ya):
        x = str(x / 1000.0)
        y = str(y / 1000.0)
        z = str(z / 1000.0)
        ro = str(ro)
        pi = str(pi)
        ya = str(ya)
        print(x,y,z,ro,pi,ya)
        mm = "movej(p[" + x + "," + y + "," + z + "," + ro + "," + pi + "," + ya + "],a=0.4,v=4)" + "\n"
        s.send(mm.encode('utf-8'))
        #self.s.close()

    def pick(self):
        cmd = "set_digital_out(1,True)" + "\n"
        s.send(cmd.encode('utf-8'))

    def place(self):
        cmd = "set_digital_out(1,False)" + "\n"
        s.send(cmd.encode('utf-8'))

    def startLeftArm(self):
        cmd = "set_digital_out(0,True)" + "\n"
        s.send(cmd.encode('utf-8'))

    def stopLeftArm(self):
        cmd = "set_digital_out(0,False)" + "\n"
        s.send(cmd.encode('utf-8'))

def Px2mm(pix):
    err = pix-320
    if err < 0: mm = (((pix-320)*(300/480))-5-((pix-320)*(3/150)))
    if err > 0: mm = (((pix-320)*(300/480))-5-((pix-320)*(4/150)))
    return mm
def Py2mm(pix):
    mm = ((pix-240)*(300/480))-35
    return mm

# Camera Position for process
cpPosX = -111
cpPosY = -526
cpPosZ = 450

def findobject(nColor):

    with Switch(nColor) as case:
        if case(Color.RED.value):
            # red
            InRange_L = np.array([0, 89, 255], dtype=np.uint8)
            InRange_H = np.array([7, 255, 255], dtype=np.uint8)
        if case(Color.YELLOW.value):
            # yellow
            InRange_L = np.array([21, 144, 144], dtype=np.uint8)
            InRange_H= np.array([180, 255, 255], dtype=np.uint8)
        if case(Color.GREEN.value):
            # green
            InRange_L = np.array([61, 30, 255], dtype=np.uint8)
            InRange_H= np.array([74, 255, 255], dtype=np.uint8)
        if case(Color.BLUE.value):
            # blue
            InRange_L = np.array([86, 57, 255], dtype=np.uint8)
            InRange_H = np.array([115, 255, 255], dtype=np.uint8)
        if case(Color.ORANGE.value):
            # orange
            InRange_L = np.array([28, 74, 255], dtype=np.uint8)
            InRange_H = np.array([43, 112, 255], dtype=np.uint8)
    _, frame = cap.read()
    img = frame
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    target = cv2.inRange(hsv, InRange_L, InRange_H)
    mask = cv2.bitwise_and(frame, frame, mask=target)

    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5, 5), np.uint8)
    gray = cv2.dilate(gray,kernel,iterations=1)
    # cv2.imshow('gray',gray)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 50, 250, cv2.THRESH_BINARY)[1]
    # cv2.imshow('T', thresh)
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

        if cx!=320: xPos = Px2mm(cx)
        if cy!=240: yPos = Py2mm(cy)
        zPos = 213

        cv2.circle(dst, (cx, cy), 7, (0, 0, 0), -1)
        Pos = str(cx) + ',' + str(cy) + ',' + str(angle)
        cv2.putText(dst, Pos, (cx - 30, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # count += 1
    # if (xPos != 0):
    #     print (yPos)
    #     if (count == 25):
    #         control.move((-116)-xPos, yPos - 539, zPos)

    control.move(cpPosX - xPos, cpPosY + yPos, zPos)
    time.sleep(3)
    control.move(cpPosX - xPos, cpPosY + yPos, 108)
    time.sleep(2)
    control.pick(0)
    time.sleep(1)
    control.move(cpPosX - xPos, cpPosY + yPos, zPos)
    time.sleep(3)
    control.move2Jig(-375.8, -361, 226.9, 2.22,0.62,-1.07)
    time.sleep(2)
    control.move2Jig(-383.7, -310, 125.1, 2.48,0.5,-1.22)
    time.sleep(2)
    control.place(0)
    time.sleep(1)
    control.move(cpPosX, cpPosY, cpPosZ)
    time.sleep(2.5)
    control.startLeftArm(0)
    time.sleep(1)
    control.stopLeftArm(0)

    # cv2.imshow('frame', frame)
    # cv2.imshow('yellow', orange)
    # cv2.imshow('img', img)

HOST = "192.168.1.9"    # The remote host
PORT = 30002              # The same port as used by the server
#PORT = 30003              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

control().move(cpPosX,cpPosY,cpPosZ)
time.sleep(4)
xPos = 0
yPos = 0
zPos = 0

cap = cv2.VideoCapture(0)
count = 0


#cv2.imshow('img', img)
# findobject(Color.RED.value)
# findobject(Color.YELLOW.value)

findobject(Color.GREEN.value)
time.sleep(10)
#findobject(Color.GREEN.value)
#time.sleep(10)
findobject(Color.RED.value)
time.sleep(10)
findobject(Color.BLUE.value)
time.sleep(10)
findobject(Color.GREEN.value)
time.sleep(10)
#findobject(Color.YELLOW.value)
#time.sleep(10)
findobject(Color.ORANGE.value)
time.sleep(10)
cv2.destroyAllWindows()

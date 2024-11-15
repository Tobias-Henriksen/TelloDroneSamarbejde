from djitellopy import tello

#import module for time:
import time

#import the previous keyboard input module file from the first step:
import KeyboardTelloModule as kp
import numpy as np
#import opencv python module:
import cv2
#Global Variable
global img


fSpeed=117/10 # forward speed in cm/s (15cm/s)
aSpeed=360/10# Angular speed degrees/s
interval=0.25

dInterval= fSpeed*interval
aInterval=aSpeed*interval


def getKeyboardInput():
    #LEFT RIGHT, FRONT BACK, UP DOWN, YAW VELOCITY
    lr, fb, ud, yv = 0,0,0,0
    speed = 80
    liftSpeed = 80
    moveSpeed = 85
    rotationSpeed = 100

    if kp.getKey("LEFT"): lr = -speed #Controlling The Left And Right Movement
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = moveSpeed #Controlling The Front And Back Movement
    elif kp.getKey("DOWN"): fb = -moveSpeed

    if kp.getKey("w"): ud = liftSpeed #Controlling The Up And Down Movemnt:
    elif kp.getKey("s"): ud = -liftSpeed

    if kp.getKey("d"): yv = rotationSpeed #Controlling the Rotation:
    elif kp.getKey("a"): yv = -rotationSpeed

    if kp.getKey("q"): Drone.land(); time.sleep(3) #Landing The Drone
    elif kp.getKey("e"): Drone.takeoff() #Take Off The Drone

    if kp.getKey("z"): #Screen Shot Image From The Camera Display
        cv2.imwrite(f"tellopy/Resources/Images/{time.time()}.jpg", img)
        time.sleep(0.3)

    return [lr, fb, ud, yv] #Return The Given Value
#Initialize Keyboard Input
kp.init()

#Start Connection With Drone
Drone = tello.Tello()
Drone.connect()

#Get Battery Info
print(Drone.get_battery())

#Start Camera Display Stream
Drone.streamon()

def drawPoints():
    cv2.circle(img,(300,500),20,(0,0,255),cv2.FILLED)

while True:
#Get The Return Value And Stored It On Variable:
    keyValues = getKeyboardInput() #Get The Return Value And Stored It On Variable
#Control The Drone:
    Drone.send_rc_control(keyValues[0],keyValues[1],keyValues[2],keyValues[3])
    img=np.zeros((1000,1000,3),np.uint8)
    drawPoints()

#Get Frame From Drone Camera Camera
    #img = Drone.get_frame_read().frame
    #img = cv2.resize(img, (1080,720))
#Show The Frame
    cv2.imshow("DroneCapture", img)
    cv2.waitKey(1)
from djitellopy import Tello
import cv2, math, time

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()



#pseudo code for mapping of following function


num = 800
middleArea = {
    "x_range": (515, 565),
    "y_range": (335, 385)
}

def is_point_in_area(x, y, area):
    x_in_range = area["x_range"][0] <= x <= area["x_range"][1]
    y_in_range = area["y_range"][0] <= y <= area["y_range"][1]
    return x_in_range and y_in_range


def function followSubject:
    tello.takeoff() with speed x to height 170cm

    if not in frame:
        rotate horizontaly

    if in frame:

        if is_point_in_area == True:

            if pixels from cam-edge to subject < num:
                backwards

            else if pixels from cam-edge to subject > num:
                forward
            else:
                wait
        else
            rotate horizontaly the shortest way until subject in middleArea == True

    if not in frame:
        rotate horizontaly
    
    if subject leave frame left
        go forward to last semm destination with angle of -15 degress with speed x + x/2
        rotate left
    
    if subject leave frame left
        go forward to last semm destination with angle of +15 degress with speed x + x/2
        rotate right

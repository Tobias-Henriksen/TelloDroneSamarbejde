import cv2
import numpy as np
cap=cv2.VideoCapture(0)


while True:
    _,img=cap.read()
    cv2.imshow("Spying",img)
    cv2.waitKey(1)


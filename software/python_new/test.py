#transform video data into time series and extract events
import numpy as np
import cv2 as cv
import pandas as pd
import supfun as sf
import time

def nothing(x):
    pass

data_folder = "/home/andre/Dropbox/trabalho/"
data_file = "converted.mp4"
#data_file = "maze_test.mp4"
#for code inspection and testing of the code purposes we add a small pause in between frames in
#the main code loop... this variable just below this needs to be set to False if one is running the actual experiments
pause_between_frames = True

cv.namedWindow('slide')
cv.createTrackbar('threshold','slide',0,255,nothing)
cv.setTrackbarPos('threshold','slide',80)

cap = cv.VideoCapture(data_folder+data_file)
#cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

valid,raw_image = cap.read()

frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv.CAP_PROP_FPS))
#if recordVideo:
#    videoFileObject = sf.record_video(cap, recordFile, frame_width, frame_height, fps)

#create named windows to show the raw and detected data
#cv.namedWindow('binary')

cv.resizeWindow(winname="slide", width=frame_width+5, height=frame_height+5	)
#cv.namedWindow('original image', cv.WINDOW_NORMAL)
#create a trackbar to change the threshold for each movie


roi = cv.selectROI("frame", raw_image, showCrosshair=True) 
cv.imshow("slide",raw_image)
cv.waitKey(0)
#thresh_value=100
while True:
    # get current positions of the trackbars
    thresh_value = cv.getTrackbarPos('threshold','slide')
    #grab one frame:
    valid,raw_image = cap.read()
    #gray = cv.cvtColor(raw_image, cv.COLOR_BGR2GRAY)
    ret,binary_image = cv.threshold(raw_image,thresh_value,255,cv.THRESH_BINARY)

    # Display the resulting frame
    cv.imshow(winname="slide",mat=binary_image)
    cv.waitKey(0)
    #cv.imshow(winname="slide")
    
    if pause_between_frames:
        #time.sleep(1/fps)
        time.sleep(0.1)
cap.release()
cv.destroyAllWindows()


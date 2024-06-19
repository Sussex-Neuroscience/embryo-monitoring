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


cap = cv.VideoCapture(data_folder+data_file)
#cap = cv.VideoCapture(0)
if not cap.isOpened():
 print("Cannot open camera")
 exit()

frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv.CAP_PROP_FPS))
#if recordVideo:
#    videoFileObject = sf.record_video(cap, recordFile, frame_width, frame_height, fps)

#create named windows to show the raw and detected data
#cv.namedWindow('binary')
cv.namedWindow('slide',cv.WINDOW_GUI_NORMAL)
#cv.namedWindow('original image', cv.WINDOW_NORMAL)
#create a trackbar to change the threshold for each movie
cv.createTrackbar('threshold','slide',0,255,nothing)
while True:
    # get current positions of the trackbars
    thresh_value = cv.getTrackbarPos('threshold','slide')
    #grab one frame:
    valid,raw_image = cap.read()
    ret,binary_image = cv.threshold(raw_image,thresh_value,255,cv.THRESH_BINARY)

    # Display the resulting frame
    cv.imshow(winname="slide",mat= binary_image)
    #cv.imshow(winname="slide")
    time.sleep(0.1)

cap.release()
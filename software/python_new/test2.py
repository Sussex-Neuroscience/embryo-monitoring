
#import all needed libraries
import numpy as np
import cv2 as cv
import pandas as pd
import supfun as sf
import time
#import serial
import os
import pandas as pd
#from tkinter import filedialog as fd
#from tkinter import *
import csv
import copy

#for code inspection and testing of the code purposes we add a small pause in between frames in
#the main code loop... this variable just below this needs to be set to False if one is running the actual experiments
pause_between_frames = True

#manual crop borders if needed:
manual_crop = True

#if running experiments "testing" should be False (related to testing the code)
testing = True

#If ROIs need to be drawn by experiementer, set the next variable to TRUE
draw_rois = False

#If just testing and no video needs to be recorded, set the next variable to FALSE
record_video = False

#define where the video is coming from. Use 0 for the first camera on the computer,
#or a complete file path to use a pre-recorded video
video_input = '/home/andre/Dropbox/trabalho/converted.mp4'


#get the current date and time, so all files created do not overwrite existing data
date_time = sf.get_current_time_formatted()

if testing:
    new_dir_path = '/home/andre/Desktop/maze_recordings/'
    #new_dir_path = "C:/Users/labadmin/Desktop/maze_recordings/"
    
    
    #recordFile = os.path.join(new_dir_path, f"test_{date_time}.mp4")
    #load the trials file (description of each trial)
    
else:
    pass


cap = sf.start_camera(videoInput=video_input)

frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv.CAP_PROP_FPS))
if record_video:
    videoFileObject = sf.record_video(cap, recordFile, frame_width, frame_height, fps)

threshold = 75
#grab one frame:
valid,gray = cap.read()
#gray,_,_=cv.split(gray)

if manual_crop:
    crop_map = cv.selectROI('frame', gray)
    crop_image = gray[crop_map[1]:crop_map[1]+crop_map[3],
                      crop_map[0]:crop_map[0]+crop_map[2],0]
    
#     gray = gray[crop_map[0]:crop_map[0]+crop_map[2],
#                 crop_map[1]:crop_map[1]+crop_map[3]]


ret,binary = cv.threshold(crop_image,threshold,255,cv.THRESH_BINARY)

#binary1=copy.deepcopy(binary)

#crop_img = img[y:y+h, x:x+w]
#run a loop to catch each area and sum the pixel values on that area of the frame


    
contours, hierarchy = cv.findContours(binary, cv.RETR_TREE,
                                      cv.CHAIN_APPROX_NONE) #detecting contours

#run a loop to get all contour areas
contour_areas = list()
contour_index = list()
bounding_rectangles = list()
#centroids = list()
min_area = 200

for index,item in enumerate(contours):
    area = cv.contourArea(item)

    #print(area)
    if area>min_area:
        
        contour_areas.append(area)
        contour_index.append(index)
        x,y,w,h = cv.boundingRect(item)
        bounding_rectangles.append([x,y,w,h])
        
        #moment = cv.moments(item)
        #centroidx = moment['m10']/moment['m00']
        #centroidy = moment['m01']/moment['m00']
        #centroids.append([centroidx,centroidy])

#after finding the contours, we need to check the area of each contour,
#using the "moment" of the images, if the areas are smaller than a certain value,
#we use a mask to remove that contour as a valid contour.

# then these contours will be used as a grid map for ROIS going forward.
#each contour will get a ROI with a rectanble bounding box around
#then we calculate the pixel number on each box over time

#as well as the length, width in each box.

#all that data needs to go to a csv file with time stamps.
drawing = np.ones(binary.shape, np.uint8)
test=cv.drawContours(drawing, contours, -1, (255,0,0), 2)

#cap.read()

#create two windows to show the animal movement while in maze:
cv.namedWindow('original image', cv.WINDOW_NORMAL)
cv.namedWindow('binary maze plus ROIs', cv.WINDOW_NORMAL)
cv.namedWindow('contours', cv.WINDOW_NORMAL)


cv.imshow('contours',test)
cv.imshow('original image',crop_image)
cv.imshow('binary maze plus ROIs',binary)
cv.waitKey(1)


absolute_time_start = sf.time_in_millis()
video_ongoing=True


while video_ongoing:
    valid,gray = cap.read()
    crop_image = gray[crop_map[1]:crop_map[1]+crop_map[3],
                      crop_map[0]:crop_map[0]+crop_map[2],0]
    ret,binary = cv.threshold(crop_image,threshold,255,cv.THRESH_BINARY)
    #contours, hierarchy = cv.findContours(binary, cv.RETR_TREE,
    #                                  cv.CHAIN_APPROX_NONE) #detecting contours
    #cv.drawContours(drawing, contours, -1, (255,0,0), 1)
    #cv.drawContours(drawing, contours, -1, (255,0,0), 1)
    for item in bounding_rectangles:
        x = item[0]
        y = item[1]
        w = item[2]
        h = item[3]
        cv.rectangle(binary,(x-10,y-10),(x+10+w,y+10+h),255,2)
    cv.imshow('contours',drawing)
    #cv.imshow('original image',crop_image)
    cv.imshow('binary maze plus ROIs',binary)
    
    
    cv.waitKey(1)

    if not valid:
        print("Can't receive frame (stream end?). Exiting ...")
        break

# 
# cv.namedWindow('gray1', cv.WINDOW_NORMAL)
# cv.namedWindow('gray2', cv.WINDOW_NORMAL)
# cv.namedWindow('gray3', cv.WINDOW_NORMAL)
# cv.namedWindow('graysum', cv.WINDOW_NORMAL)
# cv.imshow('gray1',gray[:,:,0])
# cv.imshow('gray2',gray[:,:,1])
# cv.imshow('gray3',gray[:,:,2])
# cv.imshow('graysum',np.floor(np.sum(gray,2)/np.max(np.sum(gray,2))*255))
# cv.waitKey(1)
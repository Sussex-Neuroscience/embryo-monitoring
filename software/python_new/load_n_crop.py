
#import all needed libraries
import numpy as np
import cv2 as cv
import supfun as sf
from tqdm import tqdm
from tqdm import trange
import copy
import pandas as pd


detect_rois=False

#filename = "/home/andre/Desktop/M-Mov0007.avi"
#filename = "./data/corrected.avi"
filename = "/home/andre/Videos/M-Mov0007_compress.mp4"

#wanted_fps = 2

cap = sf.start_camera(videoInput=filename)

frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv.CAP_PROP_FPS))
num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
cap.release()

wanted_fps = 2

if detect_rois:
    bounding_rectangles,crop_map = sf.detect_n_store_rois(filename=filename, wanted_fps = wanted_fps)
    bounding_rectangles.to_json("./data/bounding_rectangles.json")
    np.save("./data/crop_map.npy",crop_map)

bounding_rectangles = pd.read_json("./data/bounding_rectangles.json")
crop_map = np.load("./data/crop_map.npy")

h_max=bounding_rectangles["h"][0]
w_max=bounding_rectangles["w"][0]


sf.extract_rois_fast(filename="/home/andre/Videos/M-Mov0007_compress.mp4",
                      boundingrect_file="./data/bounding_rectangles.json",
                      crop_map_file="./data/crop_map.npy",
                      out_location="./data/")

# # #     #cv.imshow('contours',drawing)
# # #     #cv.imshow('original image',crop_image)
# # #     #cv.imshow('binary maze plus ROIs',one_roi)
# # #     
# # #
# # 
# # for index in range(roi_raw_data.shape[0]):
# 
# # # 
# # 
# # # 
# # # cv.namedWindow('gray1', cv.WINDOW_NORMAL)
# # # cv.namedWindow('gray2', cv.WINDOW_NORMAL)
# # # cv.namedWindow('gray3', cv.WINDOW_NORMAL)
# # # cv.namedWindow('graysum', cv.WINDOW_NORMAL)
# # # cv.imshow('gray1',gray[:,:,0])
# # # cv.imshow('gray2',gray[:,:,1])
# # # cv.imshow('gray3',gray[:,:,2])
# # # cv.imshow('graysum',np.floor(np.sum(gray,2)/np.max(np.sum(gray,2))*255))
# # # cv.waitKey(1)
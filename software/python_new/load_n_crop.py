

#import all needed libraries
import numpy as np
import cv2 as cv
import supfun as sf
from tqdm import tqdm
from tqdm import trange
import copy
import pandas as pd
import os

define_threshold=True
detect_rois=True
extract_rois=True




#ffmpeg to convert from avi to mp4
#ffmpeg -i input_filename.avi -c:v copy -c:a copy -y output_filename.mp4

data_root = "./data/"
#video_name = "/home/andre/Documents/onedrive/projects/open_hardware_projects/embryo_monitoring/M-Mov0007_compress.mp4"
video_name = data_root+"output_gray1.avi"

#wanted_fps = 2

#cap = sf.start_camera(videoInput=video_name)

#frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
#frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
#fps = int(cap.get(cv.CAP_PROP_FPS))
#num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
#cap.release()

#wanted_fps = 2
bound_rect_file= data_root+ "bounding_rectangles.json"
#crop_map_file = "./data/crop_map.npy"
#crop_image_file = "./data/crop_image.npy"
threshold_file = data_root+ "threshold.txt"

if define_threshold:
    #crop_map, threshold,crop_image = sf.define_threshold(filename=video_name)
    threshold = sf.define_threshold(filename=video_name)
    #np.save(crop_map_file,crop_map)
    #np.save(crop_image_file,crop_image)
    with open(threshold_file,"w") as fid:
        fid.write(str(threshold))
else:
    #crop_map = np.load(crop_map_file)
    #crop_image = np.load(crop_image_file)
    with open(threshold_file,"r") as fid:
        threshold=int(fid.readline())


if detect_rois:
    bounding_rectangles = sf.detect_n_store_rois(filename=video_name,
                                                 #crop_map=crop_map,
                                                 threshold=threshold,
                                                 #crop_image=crop_image
                                                 )
    bounding_rectangles.to_json(bound_rect_file)
    

if extract_rois:
    sf.extract_rois_fast(filename=video_name,
                        threshold=threshold,
                      boundingrect_file=bound_rect_file,
                      #crop_map_file=crop_map_file,
                      out_location="./data/")


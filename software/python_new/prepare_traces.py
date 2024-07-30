import os
import supfun as sf
import pandas as pd
import numpy as np
from tqdm import tqdm

datafolder = "./data"
#get content from folder
folder_content = os.listdir(datafolder)
folder_content.sort()

all_means = list()
all_mov_aver = list()
all_squared = list()
all_rois = list()

for item in tqdm(folder_content):
    if "ROI" in item and "npy" in item:
        all_rois.append(item)
        one_roi = np.load(datafolder+"//"+item)
        mean_brightness = sf.calculate_brightness(data=one_roi)
        mean_subtracted =  mean_brightness-np.mean(mean_brightness)
        
        moving_average = sf.calculate_moving_average(data=mean_subtracted,window_size = 60)
        squared = sf.square_square_root(data=moving_average)
        
        all_means.append(mean_brightness)
        all_mov_aver.append(moving_average)
        
        all_squared.append(squared)



    
import os
import supfun as sf
import pandas as pd
import numpy as np
from tqdm import tqdm
datafolder = "./data"
#get content from folder
folder_content = os.listdir(datafolder)

all_means = list()
all_mov_aver = list()
all_squared = list()
all_rois = list()

for tqdm(item in folder_content.sort()):
    if "ROI" in item and "npy" in item:
        all_rois.append(item)
        one_roi = np.load(datafolder+"//"+item)
        mean_brightness = sf.calculate_brightness(data=one_roi)
        moving_average = sf.calculate_moving_average(data=mean_brightness,window_size = 60)
        squared = sf.square_square_root(data=moving_average)
        
        all_means.append(mean_brightness)
        all_mov_aver.append(moving_average)
        all_squared.append(all_squared)



    
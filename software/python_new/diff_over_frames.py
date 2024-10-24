import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms
#import time
#test = np.random.randint(low=0,high=255,size=(25,15))
#plot = True
#all_data = np.load("./data/ROI0.npy")
ROIfile = input("name of ROI file:")
all_data = np.load(f"./data/{ROIfile}")
#threshold_value = 30
#thresholds= all_data>threshold_value
#mean_brightness=np.zeros([all_data.shape[2],1])

#derivative = np.diff(a = all_data,n = 1, axis = 2)


fig, axs = plt.subplots(1,2)


#base = plt.gca().transData
#rot = transforms.Affine2D().rotate_deg(-90)
plt.ion()

brightness_list = []
broc_list = []
broc_speed_list = []
broc_speed_threshold = 6

prev_height = 0
prev_width = 0
sudden_threshold = 4



def calculate_metrics(frame):
    threshold = 60
    bright_pixels = np.where(frame > threshold)
    
    if bright_pixels[0].size == 0:
        return 0, 0, 0
    
    height = bright_pixels[0].max() - bright_pixels[0].min()
    width = bright_pixels[1].max() - bright_pixels[1].min()
    
    brightness = np.mean(frame[bright_pixels])
    brightness_list.append(brightness)
    
    return height, width, brightness


for i in range(1,all_data.shape[2],600):
    print("frame ", i)
    axs[0].imshow(all_data[:,:,i],cmap="binary_r",vmin=0,vmax=256)
    axs[1].imshow(abs(all_data[:,:,i]-all_data[:,:,i-1]),cmap="binary_r",vmin=0,vmax=256)
    height, width, brightness = calculate_metrics(all_data[:, :, i])

    if i > 1:
        broc = brightness_list[-1] - brightness_list[-2]
        broc_list.append(broc)

        if len(broc_list) > 1:
            broc_speed = broc_list[-1] - broc_list[-2]
            broc_speed_list.append(broc_speed)
            print(f"speed of rate of change at frame {i}: {broc_speed}")

            if abs(broc_speed) > broc_speed_threshold and broc_speed > 0:
                print(f"Significant change in brightness rate detected at frame {i}: {broc_speed}")
    

    if prev_height != 0:
        if abs(height - prev_height) > sudden_threshold:
            print(f"Sudden height change detected at frame {i}: previous height = {prev_height}, current height = {height}")
    
    if prev_width != 0:
        if abs(width - prev_width) > sudden_threshold:
            print(f"Sudden width change detected at frame {i}: previous width = {prev_width}, current width = {width}")
    
    prev_height = height
    prev_width = width

    axs[0].set_title(f"Original Frame {i}")
    axs[1].set_title(f"Height: {height}, Width: {width}, Brightness: {brightness:.2f}")

    plt.show()
    plt.pause(0.00000001)

#ROI45 fails this
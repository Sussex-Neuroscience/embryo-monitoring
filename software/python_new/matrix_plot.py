import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms
#import time
#test = np.random.randint(low=0,high=255,size=(25,15))
plot = True
all_data = np.load("./data/ROI00.npy")
threshold_value = 70
thresholds= all_data>threshold_value
mean_brightness=np.zeros([all_data.shape[2],1])

# for i in range(0,all_data.shape[2],1):
#     embryo = all_data[:,:,i][thresholds[:,:,0]]
#     mean_brightness[i]=np.mean(embryo)
# 
# max_brightness = np.max(mean_brightness)
# min_brightness = np.mean(mean_brightness)
# 
# norm_brightness = mean_brightness/max_brightness



# if plot:
#     fig, axs = plt.subplots(1,2)
# 
#     axs[0].plot(mean_brightness)
#     axs[1].plot(norm_brightness)
#     plt.show()

#test=all_data[:,:,0	]
#thresh=test>30
#test_mask=test*thresh

fig, axs = plt.subplots(1,3)


base = plt.gca().transData
rot = transforms.Affine2D().rotate_deg(-90)
plt.ion()

for i in range(0,all_data.shape[2],100):
    print("frame ", i)


    frame = all_data[:,:,i]
    #thresh=frame>threshold_value
    frame_mask=frame*thresholds[:,:,i]
    #print("mean ", np.mean(frame[thresh]))
    #sum values over rows, so that we can get an idea of vertical brightness distributions
    vertical_collapse = frame_mask.sum(axis=1)
    horizontal_collapse = frame_mask.sum(axis=0)

    if plot:
        
        axs[0].imshow(frame,cmap="binary_r",vmin=0,vmax=300)


        axs[1].imshow(frame_mask,cmap="binary_r",vmin=0,vmax=300)
        

        axs[2].plot(vertical_collapse/np.max(vertical_collapse)*256,transform= rot + base)

        #axs[1][1].plot(horizontal_collapse/np.max(horizontal_collapse)*255)

        #axs[0][2].set_title("thresholded")
        axs[0].set_title("thresholded")
        axs[0].set_title("raw_data")
        plt.show()
        plt.pause(0.01)

        axs[0].cla()
        axs[1].cla()
        axs[2].cla()
        #axs[1][1].cla()
# #test[range(len(test.argmax(1))),test.argmax(1)]=500
# 
# #axs[0].colorbar()
# 
# 
# 
# 
# 
# #threshold this, so that we can understand when the embryo increases in length (as a proxy for
# #bursting out of the egg)
# #vert_thresh = test>30
# 
# # first of all, the base transformation of the data points is needed
# 
# 
# 
# 
# 
# 

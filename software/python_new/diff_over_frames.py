import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms
#import time
#test = np.random.randint(low=0,high=255,size=(25,15))
#plot = True
all_data = np.load("./data/ROI0.npy")
#threshold_value = 30
#thresholds= all_data>threshold_value
#mean_brightness=np.zeros([all_data.shape[2],1])

#derivative = np.diff(a = all_data,n = 1, axis = 2)

fig, axs = plt.subplots(1,2)


#base = plt.gca().transData
#rot = transforms.Affine2D().rotate_deg(-90)
plt.ion()

for i in range(1,all_data.shape[2],600):
    print("frame ", i)
    axs[0].imshow(all_data[:,:,i],cmap="binary_r",vmin=0,vmax=256)
    axs[1].imshow(abs(all_data[:,:,i]-all_data[:,:,i-1]),cmap="binary_r",vmin=0,vmax=256)
    plt.show()
    plt.pause(0.001)

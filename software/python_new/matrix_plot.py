import numpy as np
import matplotlib.pyplot as plt
from matplotlib import transforms
import supfun as sf
#import time
#test = np.random.randint(low=0,high=255,size=(25,15))
plot = False
all_data = np.load("./data/ROI00.npy")
with open("./data/threshold.txt","r") as fid:
    threshold_value = int(fid.readline())-10

mean_brightness = sf.calculate_brightness(data=all_data)
moving_average = sf.calculate_moving_average(data=mean_brightness,window_size = 60)
squared = sf.square_square_root(data=moving_average)

thresholds= all_data>threshold_value


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
# 

vertical_minima = list()
vertical_maxima = list()
vertical_max_bright = list()
vertical_length = list()

horizontal_minima = list()
horizontal_maxima = list()
horizontal_max_bright = list()
horizontal_length = list()

def calculate_moments_histogram(data):
    minimum_index = np.nonzero(data)[0][0]
    maximum_index = np.nonzero(data)[0][-1]
    index_highest_value = np.argmax(data)
    number_of_nonzero_pixels = np.sum(data>0)
    return [minimum_index,maximum_index,index_highest_value,number_of_nonzero_pixels]



if plot:
    fig, axs = plt.subplots(2,3)
    base = plt.gca().transData
    rot = transforms.Affine2D().rotate_deg(-90)
for i in range(0,all_data.shape[2],100):
    #print("frame ", i)

    
    frame = all_data[:,:,i]
    #thresh=frame>threshold_value
    frame_mask=frame*thresholds[:,:,i]
    #print("mean ", np.mean(frame[thresh]))
    #sum values over rows, so that we can get an idea of vertical brightness distributions
    vertical_collapse = frame_mask.sum(axis=1)
    horizontal_collapse = frame_mask.sum(axis=0)
    if len(vertical_collapse.nonzero()[0])>0:
        result = calculate_moments_histogram(vertical_collapse)
        result1 = calculate_moments_histogram(horizontal_collapse)

    else:
        result = [0,0,0,0]
        result1 = [0,0,0,0]
    
    vertical_minima.append(result[0])
    vertical_maxima.append(result[1])
    vertical_max_bright.append(result[2])
    vertical_length.append(result[2])
    
    horizontal_minima.append(result1[0])
    horizontal_maxima.append(result1[1])
    horizontal_max_bright.append(result1[2])
    horizontal_length.append(result1[2])
        
    if plot:
        
        axs[0][0].imshow(frame,cmap="binary_r",vmin=0,vmax=300)


        axs[0][1].imshow(frame_mask,cmap="binary_r",vmin=0,vmax=300)
        

        axs[0][2].plot(vertical_collapse/np.max(vertical_collapse)*256,transform= rot + base)
        plt.show()
        axs[1][1].plot(horizontal_collapse/np.max(horizontal_collapse)*255)
        plt.show()
        #axs[0][2].set_title("thresholded")
        axs[0][1].set_title("thresholded")
        axs[0][0].set_title("raw_data")
        axs[0][2].set_title("vertical_average")
        axs[1][1].set_title("horizontal_average")
        plt.show()
        plt.pause(0.01)

        axs[0][0].cla()
        axs[0][1].cla()
        axs[0][2].cla()
        axs[1][1].cla()


time_index = np.linspace(start=0, stop=len(horizontal_length),num=len(horizontal_length),dtype=int, endpoint=False)


#plt.figure();plt.plot(horizontal_length,vertical_length,'bo')
#plt.figure()
#plt.plot(vertical_maxima,'go');plt.plot(vertical_minima,'bo')
#plt.figure();plt.plot(horizontal_maxima,'ro');plt.plot(horizontal_minima,'ko')
#plt.figure();plt.plot(horizontal_length,vertical_length,'bo')



plt.show()
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

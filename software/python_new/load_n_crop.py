
#import all needed libraries
import numpy as np
import cv2 as cv
import supfun as sf
from tqdm import tqdm
import copy





#video_input="/home/andre/Dropbox/trabalho/c.avi"
video_input="/home/andre/Desktop/M-Mov0007.avi"
cap = sf.start_camera(videoInput=video_input)

frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv.CAP_PROP_FPS))
num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))



    
#threshold = 30
#grab one frame:
valid,gray = cap.read()


crop_map = cv.selectROI('frame', gray)
crop_image = gray[crop_map[1]:crop_map[1]+crop_map[3],
                 crop_map[0]:crop_map[0]+crop_map[2],0]
cv.destroyWindow("frame")



threshold_slider_max = 255
#title_window = 'Linear Blend'

def nothing(x):
    pass

#cv.namedWindow("raw_data")
#cv.namedWindow("image")
cv.namedWindow("test")
#cv.imshow("raw_data",crop_image)

cv.createTrackbar("threshold", 'test' , 70, threshold_slider_max, nothing)
print("press 'enter' after you decided on the threshold level")
while(1):
    
    threshold = cv.getTrackbarPos('threshold','test')
    ret,binary = cv.threshold(crop_image,threshold,255,cv.THRESH_BINARY)
    numpy_horizontal_concat = np.concatenate((crop_image, binary), axis=1)
    #cv.imshow('image',binary)
    
    cv.imshow("test",numpy_horizontal_concat)
    k = cv.waitKey(1) & 0xFF
    if k == 13:
        break

cv.destroyWindow("test")
#cv.destroyWindow("raw_data")
  
contours, hierarchy = cv.findContours(binary, cv.RETR_TREE,
                                      cv.CHAIN_APPROX_NONE) #detecting contours


#run a loop to get all contour areas
contour_areas = list()
contour_index = list()
bounding_rectangles = list()
#centroids = list()


border_size = 5

w_max=20+2*border_size
h_max=50+2*border_size

#create a named window to show detected rois
cv.namedWindow('ROI candidate', cv.WINDOW_NORMAL)

min_area = 200
max_area = 600
for index,item in enumerate(contours):
    area = cv.contourArea(item)

    #print(area)
    if area>min_area and area<max_area:
        #temp_left=
        
        x,y,w,h = cv.boundingRect(item)
        temp_image=copy.deepcopy(crop_image)
       
        #added = False
        while True:
            cv.drawContours(temp_image, item, -1, 255, 1)
            cv.rectangle(temp_image,(x,y),
                                    (w,h),255,2)
            cv.imshow('ROI candidate',temp_image)
            k = cv.waitKey(33)
            #print(k)
            if  k == 121:
                contour_areas.append(area)
                contour_index.append(index)
                bounding_rectangles.append([x-border_size,
                                    y-border_size,
                                    w_max,
                                    h_max])
                break
            elif k == 110:
                break
        

cv.destroyWindow("ROI candidate")

index=1
for item in tqdm(bounding_rectangles): 
    roi_raw_data = np.zeros([h_max,w_max,num_frames],dtype="int8")
    
    for frame in range(num_frames):
        valid,gray = cap.read()
        cv.waitKey(1)
        if not valid:
            print("Can't receive frame (stream end?). Exiting ...")
            break
  
        crop_image = gray[crop_map[1]:crop_map[1]+crop_map[3],
                      crop_map[0]:crop_map[0]+crop_map[2],0]

       
#         
        x = item[0]
        y = item[1]
        w = item[2]
        h = item[3]
#         cv.rectangle(binary,(x,y),(x+w,y+h),255,2)
        one_roi = crop_image[y:y+h,x:x+w]
        roi_raw_data[:,:,frame]=one_roi
    
    print("saving ROI: ",index)
    filename = "./data/ROI{0}.npy".format(index)
    np.save(file=filename, arr=roi_raw_data[index])
    index=index+1
# #     #cv.imshow('contours',drawing)
# #     #cv.imshow('original image',crop_image)
# #     #cv.imshow('binary maze plus ROIs',one_roi)
# #     
# #
# 
# for index in range(roi_raw_data.shape[0]):

# # 
# 
# # 
# # cv.namedWindow('gray1', cv.WINDOW_NORMAL)
# # cv.namedWindow('gray2', cv.WINDOW_NORMAL)
# # cv.namedWindow('gray3', cv.WINDOW_NORMAL)
# # cv.namedWindow('graysum', cv.WINDOW_NORMAL)
# # cv.imshow('gray1',gray[:,:,0])
# # cv.imshow('gray2',gray[:,:,1])
# # cv.imshow('gray3',gray[:,:,2])
# # cv.imshow('graysum',np.floor(np.sum(gray,2)/np.max(np.sum(gray,2))*255))
# # cv.waitKey(1)
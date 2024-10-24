#import all needed libraries
import numpy as np
import cv2 as cv
from tqdm import tqdm
from tqdm import trange
import copy
import pandas as pd

def start_camera(videoInput=0):
    cap = cv.VideoCapture(videoInput)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    return cap

def get_video_info(filename = 0):
    """
    Retrieves video information such as frame width, frame height, frames per second (fps), 
    and the number of frames from a video file or a camera stream.

    Parameters:
    filename (str or int): The path to the video file or 0 for the default camera stream. 
                           If 0, the function will use the default camera.

    Returns:
    dict: A dictionary containing the following keys:
        - "frame_width" (int): The width of the video frames.
        - "frame_height" (int): The height of the video frames.
        - "fps" (int): The frames per second of the video.
        - "num_frames" (int or str): The total number of frames in the video. 
                                     If the input is a camera stream, this will be "stream".
    """
    
    cap = start_camera(videoInput=filename)

    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv.CAP_PROP_FPS))
    
    if filename != 0:
        num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    else:
        num_frames = "stream"
    cap.release()
    
    info = {"frame_width":frame_width,
            "frame_height":frame_height,
            "fps":fps,
            "num_frames": num_frames}
    
    return info

def define_threshold(filename="/home/andre/Desktop/M-Mov0007.avi",
                     
                        #wanted_fps=2
                        ):
    cap = start_camera(videoInput=filename)
    info = get_video_info(filename=filename)

    valid,gray = cap.read()
    #cv.namedWindow("frame", cv.WINDOW_NORMAL)

    #crop_map = cv.selectROI('frame', gray)
    #crop_image = gray[crop_map[1]:crop_map[1]+crop_map[3],
    #                 crop_map[0]:crop_map[0]+crop_map[2],0]
    #cv.destroyWindow("frame")



    threshold_slider_max = 255
    #title_window = 'Linear Blend'

    def nothing(x):
        pass


    cv.namedWindow("threshold",cv.WINDOW_NORMAL)

    cv.createTrackbar("threshold_bar", 'threshold' , 70, threshold_slider_max, nothing)
    print("press 'enter' after you decided on the threshold level")
    while(1):
        
        threshold = cv.getTrackbarPos('threshold_bar','threshold')
        ret,binary = cv.threshold(gray,threshold,255,cv.THRESH_BINARY)
        numpy_horizontal_concat = np.concatenate((gray, binary), axis=1)
        #cv.imshow('image',binary)
        
        cv.imshow("threshold",numpy_horizontal_concat)
        k = cv.waitKey(1) & 0xFF
        if k == 13:
            break

    cv.destroyWindow("threshold")
    
    return threshold#crop_map, threshold,crop_image

def detect_n_store_rois(filename="/home/andre/Desktop/M-Mov0007.avi",
                        #crop_map=np.zeros([20,30]),
                                          threshold=70,
                        #crop_image=np.zeros([200,300])
                        ):



    cap = start_camera(videoInput=filename)
    info = get_video_info(filename=filename)
    
    valid,gray = cap.read()
    gray=gray[:,:,0]
    ret,binary = cv.threshold(gray,threshold,255,cv.THRESH_BINARY)  
    contours, _ = cv.findContours(binary, cv.RETR_TREE,
                                          cv.CHAIN_APPROX_NONE) #detecting contours
    #run a loop to get all contour areas
    contour_areas = list()
    contour_index = list()
    bounding_rectangles = list()

    #create a named window to show detected rois
    cv.namedWindow('ROI candidate', cv.WINDOW_NORMAL)

    min_area = 150
    max_area = 700
    
    border_size = 6        
    
    for index,item in enumerate(contours):
        area = cv.contourArea(item)

        if area>min_area and area<max_area:

            
            x,y,w,h = cv.boundingRect(item)
            temp_image=copy.deepcopy(gray)
            

            while True:
                cv.drawContours(temp_image, item, -1, 255, 1)
                cv.rectangle(temp_image,(x-border_size,
                                         y-border_size),
                                         (x+w+border_size,
                                          y+h+border_size),
                                         255,2)
                cv.imshow('ROI candidate',temp_image)
                k = cv.waitKey(33)
                if  k == 121:
                    contour_areas.append(area)
                    contour_index.append(index)
                    bounding_rectangles.append([x,y,
                                                w,h,
                                                border_size])
                    break
                elif k == 110:
                    break
            

    cv.destroyWindow("ROI candidate")
    cap.release()
    rectangles = pd.DataFrame(bounding_rectangles,columns=["x","y","w","h","border"])
    sorted_rectangles=rectangles.sort_values(by=['x', 'y'])
    #rectangles.to_json("./data/bounding_rectangles.json")
    
    return sorted_rectangles





def extract_rois_fast(filename="/home/andre/Videos/M-Mov0007_compress.mp4",
                      boundingrect_file="./data/bounding_rectangles.json",
                      #crop_image_file="./data/crop_image.npy",
                      threshold=70,
                      out_location="./data/"):
    
    bounding_rectangles = pd.read_json(boundingrect_file)
    #crop_map = np.load(crop_map_file)
    
    info = get_video_info(filename=filename)

    num_frames = info["num_frames"]
    
    cap = start_camera(videoInput=filename)
    h_max=max(bounding_rectangles["h"])
    w_max=max(bounding_rectangles["w"])
    border = bounding_rectangles["border"][0]
    
    all_data=np.zeros([h_max+2*border,w_max+2*border,num_frames,len(bounding_rectangles)],dtype="uint8")
    
    for index_frame in tqdm(trange(num_frames),position=0,leave=False):
        valid,gray = cap.read()
        cv.waitKey(1)
        if not valid:
            #cap.release()
            #del(cap)
            print("Can't receive frame (stream end?). Exiting ...")
            break
        #crop_image = gray[crop_map[1]:crop_map[1]+crop_map[3],
        #                  crop_map[0]:crop_map[0]+crop_map[2],0]
        
        for index_roi in range(len(bounding_rectangles)):#tqdm(trange(len(bounding_rectangles)),position=1,leave=False):
        
            x = bounding_rectangles["x"][index_roi]
            y = bounding_rectangles["y"][index_roi]
            w = bounding_rectangles["w"][index_roi]
            h = bounding_rectangles["h"][index_roi]
            border = bounding_rectangles["border"][index_roi]
            one_roi = gray[y-2*border:y+h_max,x-2*border:x+w_max,0]

            all_data[0:one_roi.shape[0],0:one_roi.shape[1],index_frame,index_roi] = one_roi
            
            #index_frame=index_frame+1

        
        
    for index_roi in tqdm(trange(len(all_data[0,0,0,:]))):
        if len(str(index_roi))==1:
            name_roi = "0"+str(index_roi)
        else:
            name_roi = str(index_roi)

        out_filename = out_location+"ROI"+name_roi+".npy"
        np.save(file=out_filename,arr=all_data[:,:,:,index_roi])
        #np.save(file=out_filename, arr=roi_raw_data)

def calculate_brightness(data=[1,1,1,1]):
    mean_brightness_raw = np.mean(data,0)
    mean_brightness_raw = np.mean(mean_brightness_raw,0)
    return mean_brightness_raw


def calculate_moving_average(data=[1,1,1,1],window_size=60):
    i = 0
    # Initialize an empty list to store moving averages
    moving_average = []
    #data = list(data)
    # Loop through the array to consider
    # every window of size 3
    while i < len(data) - window_size + 1:
   
        # Store elements from i to i+window_size
        # in list to get the current window
        window = data[i : i + window_size]
 
        # Calculate the average of current window
        window_average = round(sum(window) / window_size, 2)
     
        # Store the average of current
        # window in moving average list
        moving_average.append(window_average)
     
        # Shift window to right by one position
        i += 1
    moving_average = np.array(moving_average)
    return moving_average

def square_square_root(data = [1,1,1,1]):
    powers = [2]*len(data)
    squared = np.pow(data,powers)
    sqrt = np.sqrt(squared)
    return sqrt

# def extract_rois_slow(filename="/home/andre/Videos/M-Mov0007_compress.mp4",
#                       boundingrect_file="./data/bounding_rectangles.json",
#                       crop_map_file="./data/crop_map.npy"):
#     
#     bounding_rectanlges = pd.read_json(boundingrect_file)
#     crop_map = np.load(crop_map_file)
#     
#     info = get_video_info(filename=filename)
#     
#     frame_width = info["frame_width"]#int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
#     frame_height = info["frame_heigth"]#int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
#     fps = info["fps"]#int(cap.get(cv.CAP_PROP_FPS))
#     num_frames = info["num_frames"]#int(cap.get(cv.CAP_PROP_FRAME_COUNT))
#     
#     cap = start_camera(videoInput=filename)
#     for index_roi in tqdm(trange(0,len(bounding_rectangles)),position=0):
#         roi_raw_data = np.zeros([h_max,w_max,num_frames],dtype="uint8")
#         index_frame=0
#         for frame in tqdm(trange(0,num_frames),position=1,leave=False):
#             #cap.set(cv.CAP_PROP_POS_FRAMES, frame-1)
#             valid,gray = cap.read()
#             cv.waitKey(1)
#             if not valid:
#                 #cap.release()
#                 #del(cap)
#                 print("Can't receive frame (stream end?). Exiting ...")
#                 break
#       
#             crop_image = gray[crop_map[1]:crop_map[1]+crop_map[3],
#                           crop_map[0]:crop_map[0]+crop_map[2],0]
# 
#            
# 
#             x = bounding_rectangles["x"][index_roi]
#             y = bounding_rectangles["y"][index_roi]
#             w = bounding_rectangles["w"][index_roi]
#             h = bounding_rectangles["h"][index_roi]
# 
#             one_roi = crop_image[y:y+h,x:x+w]
# 
#             roi_raw_data[:,:,index_frame]=one_roi
#             
#             index_frame=index_frame+1
# 
#         #cap.release()
#         #del(cap)
#         print("saving ROI: ",index_roi)
#         cap.set(cv.CAP_PROP_POS_FRAMES, -1)
#         if len(index_roi)==1:
#             name_roi = "0"+str(index_roi)
#         else:
#             name_roi = str(index_roi)
#         
#         out_filename = "./data/ROI"+name_roi+".npy".format(index_roi)
#         
#         np.save(file=out_filename, arr=roi_raw_data)
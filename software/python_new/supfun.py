#import all needed libraries
import numpy as np
import cv2 as cv
import supfun as sf
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
    cap = sf.start_camera(videoInput=filename)

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



def detect_n_store_rois(filename="/home/andre/Desktop/M-Mov0007.avi",
                        wanted_fps=2):
#video_input="/home/andre/Dropbox/trabalho/c.avi"


    cap = start_camera(videoInput=filename)
    info = get_video_info(filename=filename)
    
    frame_width = info["frame_width"]#int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = info["frame_heigth"]#int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = info["fps"]#int(cap.get(cv.CAP_PROP_FPS))
    num_frames = info["num_frames"]#int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    wanted_fps = 2

        
    #threshold = 30
    #grab one frame:
    valid,gray = cap.read()
    cv.namedWindow("frame", cv.WINDOW_NORMAL)

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

    w_max=20+border_size
    h_max=50+border_size

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
                cv.rectangle(temp_image,(x-border_size,y-border_size),
                                        (x+w+border_size,y+h+border_size),255,2)
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
    rectangles = pd.DataFrame(bounding_rectangles,columns=["x","y","w","h"])
    #rectangles.to_json("./data/bounding_rectangles.json")
    cap.release()
    return rectangles,crop_map


def extract_rois_slow(filename="/home/andre/Videos/M-Mov0007_compress.mp4",
                      boundingrect_file="./data/bounding_rectangles.json",
                      crop_map_file="./data/crop_map.npy"):
    
    bounding_rectanlges = pd.read_json(boundingrect_file)
    crop_map = np.load(crop_map_file)
    
    info = get_video_info(filename=filename)
    
    frame_width = info["frame_width"]#int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = info["frame_heigth"]#int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = info["fps"]#int(cap.get(cv.CAP_PROP_FPS))
    num_frames = info["num_frames"]#int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    
    cap = sf.start_camera(videoInput=filename)
    for index_roi in tqdm(trange(0,len(bounding_rectangles)),position=0):
        roi_raw_data = np.zeros([h_max,w_max,num_frames],dtype="uint8")
        index_frame=0
        for frame in tqdm(trange(0,num_frames),position=1,leave=False):
            #cap.set(cv.CAP_PROP_POS_FRAMES, frame-1)
            valid,gray = cap.read()
            cv.waitKey(1)
            if not valid:
                #cap.release()
                #del(cap)
                print("Can't receive frame (stream end?). Exiting ...")
                break
      
            crop_image = gray[crop_map[1]:crop_map[1]+crop_map[3],
                          crop_map[0]:crop_map[0]+crop_map[2],0]

           

            x = bounding_rectangles["x"][index_roi]
            y = bounding_rectangles["y"][index_roi]
            w = bounding_rectangles["w"][index_roi]
            h = bounding_rectangles["h"][index_roi]

            one_roi = crop_image[y:y+h,x:x+w]

            roi_raw_data[:,:,index_frame]=one_roi
            
            index_frame=index_frame+1

        #cap.release()
        #del(cap)
        print("saving ROI: ",index_roi)
        cap.set(cv.CAP_PROP_POS_FRAMES, -1)
        
        out_filename = "./data/ROI{0}.npy".format(index_roi)
        
        np.save(file=out_filename, arr=roi_raw_data)


def extract_rois_fast(filename="/home/andre/Videos/M-Mov0007_compress.mp4",
                      boundingrect_file="./data/bounding_rectangles.json",
                      crop_map_file="./data/crop_map.npy",
                      out_location="./data/"):
    
    bounding_rectangles = pd.read_json(boundingrect_file)
    crop_map = np.load(crop_map_file)
    
    info = get_video_info(filename=filename)
    
    frame_width = info["frame_width"]#int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = info["frame_height"]#int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = info["fps"]#int(cap.get(cv.CAP_PROP_FPS))
    num_frames = info["num_frames"]#int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    
    cap = sf.start_camera(videoInput=filename)
    h_max=bounding_rectangles["h"][0]
    w_max=bounding_rectangles["w"][0]
    all_data=np.zeros([h_max,w_max,num_frames,len(bounding_rectangles)],dtype="uint8")
    for index_frame in tqdm(trange(num_frames),position=0,leave=False):
        valid,gray = cap.read()
        cv.waitKey(1)
        if not valid:
            #cap.release()
            #del(cap)
            print("Can't receive frame (stream end?). Exiting ...")
            break
        crop_image = gray[crop_map[1]:crop_map[1]+crop_map[3],
                          crop_map[0]:crop_map[0]+crop_map[2],0]
        
        for index_roi in range(len(bounding_rectangles)):#tqdm(trange(len(bounding_rectangles)),position=1,leave=False):
        
            x = bounding_rectangles["x"][index_roi]
            y = bounding_rectangles["y"][index_roi]
            w = bounding_rectangles["w"][index_roi]
            h = bounding_rectangles["h"][index_roi]

            one_roi = crop_image[y:y+h,x:x+w]

            all_data[:,:,index_frame,index_roi]=one_roi
            
            #index_frame=index_frame+1

        
        
    for index_roi in tqdm(trange(len(all_data[0,0,0,:]))):
        out_filename = out_location+"ROI{0}.npy".format(index_roi)
        np.save(file=out_filename,arr=all_data[:,:,:,index_roi])
        #np.save(file=out_filename, arr=roi_raw_data)
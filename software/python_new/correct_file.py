import cv2 as cv
import numpy as np
from tqdm import tqdm
from tqdm import trange
import supfun as sf

filename = "/home/andre/Documents/onedrive/projects/open_hardware_projects/embryo_monitoring/M-Mov0007.avi"


wanted_fps = 2

cap = sf.start_camera(videoInput=filename)

frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv.CAP_PROP_FPS))
num_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

#cap.release()

fps_ratio = int(fps/wanted_fps)
size = (frame_width,frame_height)
result = cv.VideoWriter('./data/corrected.avi',  
                         cv.VideoWriter_fourcc(*'MJPG'), 
                         wanted_fps, size) 

#cap = sf.start_camera(videoInput=filename)

for index in range(num_frames):
    valid,gray = cap.read()
    cv.waitKey(1)
    if not valid:
        cap.release()
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    if index%fps_ratio==0:
        print(index)
        result.write(gray)
        
cap.release()




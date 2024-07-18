import cv2
import numpy as np
import time

def sample_fps(video, sample_duration=600, max_frames=10):
    frame_count = 0
    start_time = time.time()
    
    while True:
        ret, frame = video.read()
        if not ret:
            break
        
        frame_count += 1
        
        if frame_count >= max_frames:
            break
        
        if time.time() - start_time >= sample_duration:
            break
        
        # Extract Y channel (grayscale) from YUVJ422P
        gray = frame[:, :, 0]
        
        # Display the frame (optional)
        cv2.imshow('Frame', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    end_time = time.time()
    duration = end_time - start_time
    
    return frame_count, duration

# Open the video file
video = cv2.VideoCapture('/home/andre/Videos/M-Mov0007.avi')

if not video.isOpened():
    print("Error opening video file")
    exit()

# Get video properties
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Sample FPS
sample_frames, sample_duration = sample_fps(video, sample_duration=60, max_frames=1000)

# Calculate FPS
calculated_fps = sample_frames / sample_duration

print(f"Calculated FPS: {calculated_fps:.2f}")
print(f"Sample Frame Count: {sample_frames}")
print(f"Sample Duration: {sample_duration:.2f} seconds")
print(f"Resolution: {width}x{height}")

# Get total frame count (may be inaccurate)
video.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
total_frames = int(video.get(cv2.CAP_PROP_POS_FRAMES))
video.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

print(f"Total Frames (from metadata): {total_frames}")
print(f"Estimated Total Duration: {total_frames / calculated_fps:.2f} seconds")

video.release()
cv2.destroyAllWindows()

# import cv2
# import numpy as np
# import time
# 
# 
# 
# # Open the video file
# video = cv2.VideoCapture('/home/andre/Videos/M-Mov0007.avi')
# 
# if not video.isOpened():
#     print("Error opening video file")
#     exit()
# 
# # Get video properties
# width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
# 
# # Sample FPS
# sample_duration=60
# max_frames=1000
# 
# frame_count = 0
# start_time = time.time()
# 
# while True:
#     ret, frame = video.read()
#     if not ret:
#         break
#     
#     frame_count += 1
#     
#     if frame_count >= max_frames:
#         break
#     
#     if time.time() - start_time >= sample_duration:
#         break
#     
#     # Convert from YUVJ422P to BGR
#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_YUV2GRAY_NV21)
#     
#     # Display the frame (optional)
#     cv2.imshow('Frame', frame_rgb)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# 
# end_time = time.time()
# duration = end_time - start_time
# 
# 
# # Calculate FPS
# calculated_fps = sample_frames / sample_duration
# 
# print(f"Calculated FPS: {calculated_fps:.2f}")
# print(f"Sample Frame Count: {sample_frames}")
# print(f"Sample Duration: {sample_duration:.2f} seconds")
# print(f"Resolution: {width}x{height}")
# 
# # Get total frame count (may be inaccurate)
# video.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)
# total_frames = int(video.get(cv2.CAP_PROP_POS_FRAMES))
# video.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)
# 
# print(f"Total Frames (from metadata): {total_frames}")
# print(f"Estimated Total Duration: {total_frames / calculated_fps:.2f} seconds")
# 
# video.release()
# cv2.destroyAllWindows()
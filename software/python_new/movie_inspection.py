import supfun as sf
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np




filename="/home/andre/Videos/output.mp4"
cap = sf.start_camera(videoInput=filename)
valid,gray = cap.read()
cap.release()
del(cap)

test = np.array(gray,dtype=np.uint32)

fig, axs = plt.subplots(nrows=2,ncols=2)

axs[0][0].imshow(test.sum(axis=2))
axs[0][0].set_title("sum of all mp4")

axs[0][1].imshow(gray[:,:,0])
axs[0][1].set_title("one channel mp4")

filename="/home/andre/Videos/M-Mov0007.avi"
cap = sf.start_camera(videoInput=filename)
valid,gray = cap.read()
cap.release()


test = np.array(gray,dtype=np.uint32)
axs[1][0].imshow(test.sum(axis=2))
axs[1][0].set_title("sum of all avi")


axs[1][1].imshow(gray[:,:,0])
axs[1][1].set_title("one channel avi")
plt.show()

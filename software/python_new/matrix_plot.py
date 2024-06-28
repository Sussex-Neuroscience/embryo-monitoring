import numpy as np
import matplotlib.pyplot as plt

test = np.random.randint(low=0,high=255,size=(25,15))
thresh=test>100
test_mask=test*thresh

#test[range(len(test.argmax(1))),test.argmax(1)]=500

plt.imshow(test_mask,cmap="binary_r",vmin=0,vmax=255)
plt.colorbar()
plt.show()

#sum values over rows, so that we can get an idea of vertical brightness distributions
vertical_collapse = test.sum(axis=1)
#threshold this, so that we can understand when the embryo increases in length (as a proxy for
#bursting out of the egg)
vert_thresh = test>100


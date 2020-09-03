import numpy as np
import micasense.imageutils as imageutils
from cv2 import cv2
def CalNBI(im_aligned):
    norm = np.zeros(im_aligned.shape)
    kernel = np.ones((5,5),np.float32)/25
    im_sum = (im_aligned[:,:,0]+im_aligned[:,:,1]+im_aligned[:,:,2]+im_aligned[:,:,3]+im_aligned[:,:,4])
    for i in range(im_aligned.shape[2]):
        #norm[:,:,i] = cv2.filter2D(im_aligned[:,:,i]/im_sum,-1,kernel)
        norm[:,:,i] = im_aligned[:,:,i]/im_sum
    OSAVI =  (1+0.16) * (norm[:,:,3]-norm[:,:,2])/(norm[:,:,3]+norm[:,:,2]+0.16)
    TCARI = 3* ((norm[:,:,4]-norm[:,:,2])-
            (0.2*(norm[:,:,4]-norm[:,:,1])*
                (norm[:,:,4]/norm[:,:,2])))
    NDVI = (im_aligned[:,:,3]-im_aligned[:,:,2])/(im_aligned[:,:,3]+im_aligned[:,:,2])
    NDVIMASK = NDVI < 0.5
    NBI = TCARI/OSAVI
    NBI[NDVIMASK] = 0
    return NBI, NDVIMASK

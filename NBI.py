import numpy as np
import micasense.imageutils as imageutils

def CalNBI(im_aligned):
    OSAVI =  (1+0.16) * (im_aligned[:,:,3]-im_aligned[:,:,2])/(im_aligned[:,:,3]+im_aligned[:,:,2]+0.16)
    TCARI = 3* ((im_aligned[:,:,4]-im_aligned[:,:,2])-
            (0.2*(im_aligned[:,:,4]-im_aligned[:,:,1])*
                (im_aligned[:,:,4]/im_aligned[:,:,2])))
    return TCARI/OSAVI

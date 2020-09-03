import pytest
from cv2 import cv2
from NBI import CalNBI
import numpy as np
import micasense.capture as cap
import micasense.imageutils as imageutils
import os, glob
from Allignment import AllignImage ,ReadAllignmentMatrix

def test_NBI(i):
    imagePath = os.path.join('.','data','tiff')
    outPath = os.path.join('.','data','output','{:04d}.png'.format(i))
    #outPath = os.path.join('.','data','gaus','{:04d}.png'.format(i))
    imageNames = glob.glob(os.path.join(imagePath,'IMG_{:04d}_*.tif'.format(i)))
    capture = cap.Capture.from_filelist(imageNames)
    allignmat, havePrev = ReadAllignmentMatrix(".")
    im_aligned = AllignImage(allignmat,capture)
    NBI,ndvimask = CalNBI(im_aligned)
    print(imageNames)
    min = -1.5
    max = 1.5
    lower = NBI < min
    NBI[lower] = min
    higher = NBI >max
    NBI[higher] = max    
    NBI = ((NBI - min)/(max-min)) * 255.0
    NBI = NBI.astype(np.uint8)
    #NBI= cv2.normalize(NBI,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
    im_color = cv2.applyColorMap(NBI, cv2.COLORMAP_JET)
    #cv2.imshow('normalize',im_color)
    #cv2.waitKey(10)
    im_color[ndvimask] = [0,0,0]
    cv2.imwrite(outPath,im_color)
    return


if __name__ == "__main__":
    for i in range(168,370):
        test_NBI(i)
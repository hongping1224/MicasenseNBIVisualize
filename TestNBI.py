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
    imageNames = glob.glob(os.path.join(imagePath,'IMG_{:04d}_*.tif'.format(i)))
    print(imageNames)
    capture = cap.Capture.from_filelist(imageNames)
    allignmat, havePrev = ReadAllignmentMatrix(".")
    im_aligned = AllignImage(allignmat,capture)
    NBI = CalNBI(im_aligned)
    im_min = np.percentile(NBI.flatten(), 0.5) 
    im_max = np.percentile(NBI.flatten(), 99.5)
    print(im_min, im_max)
    NBI = imageutils.normalize(NBI, -10, 5)
    NBI= cv2.normalize(NBI,None,0,255,cv2.NORM_MINMAX,cv2.CV_8U)
    cv2.imshow('NBI',NBI)
    im_color = cv2.applyColorMap(NBI, cv2.COLORMAP_JET)
    cv2.imshow('normalize',im_color)
    cv2.waitKey(10)
    return


if __name__ == "__main__":
    for i in range(168,371):
        test_NBI(i)
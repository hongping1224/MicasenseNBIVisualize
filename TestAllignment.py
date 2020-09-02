import pytest
from cv2 import cv2
from NBI import CalNBI
import numpy as np
import micasense.capture as cap
import micasense.imageutils as imageutils
import os, glob
from Allignment import AllignImage ,GetAllignmentMatrix,SaveAllignmentMatrix,ReadAllignmentMatrix

def test_Allignment():
    imagePath = os.path.join('.','data','tiff')
    imageNames = glob.glob(os.path.join(imagePath,'IMG_0168_*.tif'))
    panelNames = glob.glob(os.path.join(imagePath,'IMG_0000_*.tif'))
    
    if panelNames is not None:
        panelCap = cap.Capture.from_filelist(panelNames)
    else:
        panelCap = None
    capture = cap.Capture.from_filelist(imageNames)
    if panelCap is not None:
        if panelCap.panel_albedo() is not None:
            panel_reflectance_by_band = panelCap.panel_albedo()
        else:
            panel_reflectance_by_band = [0.65]*len(imageNames)
        panel_irradiance = panelCap.panel_irradiance(panel_reflectance_by_band)    
        img_type = "reflectance"
    allignmat, havePrev = ReadAllignmentMatrix(".")
    if havePrev == False:
        allignmat=GetAllignmentMatrix(capture)
        SaveAllignmentMatrix("a_mat_{}.txt",allignmat)
    im_aligned = AllignImage(allignmat,capture)
    print(capture.band_names())
    rgb_band_indices = [capture.band_names().index('Red'),capture.band_names().index('Green'),capture.band_names().index('Blue')]
    cir_band_indices = [capture.band_names().index('NIR'),capture.band_names().index('Red'),capture.band_names().index('Green')]
    im_display = np.zeros((im_aligned.shape[0],im_aligned.shape[1],im_aligned.shape[2]), dtype=np.float32 )

    im_min = np.percentile(im_aligned[:,:,rgb_band_indices].flatten(), 0.5)  # modify these percentiles to adjust contrast
    im_max = np.percentile(im_aligned[:,:,rgb_band_indices].flatten(), 99.5)  # for many images, 0.5 and 99.5 are good values

    for i in rgb_band_indices:
        im_display[:,:,i] =  imageutils.normalize(im_aligned[:,:,i], im_min, im_max)

    rgb = im_display[:,:,rgb_band_indices]
    for i in cir_band_indices:
        im_display[:,:,i] =  imageutils.normalize(im_aligned[:,:,i])
    cir = im_display[:,:,cir_band_indices]
    cv2.imshow("rgb",rgb)
    cv2.imshow("cir",cir)
    cv2.waitKey(0)
    return


if __name__ == "__main__":
    test_Allignment()
  
   
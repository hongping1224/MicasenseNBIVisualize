import numpy as np
import os, glob
import micasense.capture as capture
import micasense.imageutils as imageutils
from cv2 import cv2

def ReadAllignmentMatrix(path):
    matrix = []
    matrix_path = glob.glob('./a_mat_*.txt')
    matrix_path.sort()

    for path in matrix_path:
        try:
            matrix.append(np.loadtxt(path))
        except:
            return [] ,False
    return matrix , True

def SaveAllignmentMatrix(path, matrix):
    for i in range(len(matrix)):
       np.savetxt(path.format(i),matrix[i])
    return


def AllignImage(mat, images):
    if images.dls_present():
        img_type='reflectance'
    else:
        img_type = "radiance"
    warp_mode = cv2.MOTION_HOMOGRAPHY
    match_index = 4
    cropped_dimensions, edges = imageutils.find_crop_bounds(images, mat, warp_mode=warp_mode)
    im_aligned = imageutils.aligned_capture(images, mat, warp_mode, cropped_dimensions, match_index, img_type=img_type)
    return im_aligned

def GetAllignmentMatrix(images):
    ## Alignment settings
    match_index = 4 # Index of the band, here we use green
    max_alignment_iterations = 20
    warp_mode = cv2.MOTION_HOMOGRAPHY # MOTION_HOMOGRAPHY or MOTION_AFFINE. For Altum images only use HOMOGRAPHY
    pyramid_levels = 3 # for 10-band imagery we use a 3-level pyramid. In some cases
    warp_matrices, alignment_pairs = imageutils.align_capture(images,
                                                          ref_index = match_index,
                                                          max_iterations = max_alignment_iterations,
                                                          warp_mode = warp_mode,
                                                          pyramid_levels = pyramid_levels)
    return warp_matrices


def main():
    path = ""
    confPath = ""
    mat = GetAllignmentMatrix(path)
    SaveAllignmentMatrix(confPath, mat)
    return


if __name__== "__main__":
    main()

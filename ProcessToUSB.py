import time
import glob
import numpy as np
from datetime import datetime
import os
import micasense.capture as cap
from Allignment import ReadAllignmentMatrix, AllignImage
from NBI import Calall
import cv2
_Running =False
_index = 0
_total = 0

def stats():
    global _Running, _index , _total
    return _Running , _index, _total 

def GetAllImageRoot():
    result = glob.glob("./img/*_5.tif")
    suffix = "_5.tif"
    files = []

    for f in result:
        filename = f.replace(suffix,"_*.tif")
        files.append(filename)
    files.sort()        
    return files

def processImage(p,OutRoot,almat):
    result = glob.glob(p)
    capture = cap.Capture.from_filelist(result)
    im_aligned = AllignImage(almat, capture)
    nbi , ndvi , rgb = Calall(im_aligned)
    imgname = p.replace("_*","").replace("./img/","")
    rgb= cv2.normalize(rgb,None,0,255,cv2.NORM_MINMAX,cv2.CV_8UC3)
    cv2.imwrite(os.path.join(OutRoot,"rgb",imgname.replace(".tif",".png")),rgb)
    print(os.path.join(OutRoot,"rgb",imgname))
    cv2.imwrite(os.path.join(OutRoot,"ndvi",imgname),np.float32(ndvi))
    cv2.imwrite(os.path.join(OutRoot,"nbi",imgname),np.float32(nbi))
    del nbi
    del rgb
    del ndvi
    del im_aligned
    capture.clear_image_data()
    del capture
    del result
    return 


def Start(OutRoot):
    global _Running, _index , _total
    _Running = True
    ImagePath = GetAllImageRoot()
    _total = len(ImagePath)
    _index = 0
    print(ImagePath)
    now = datetime.now()
    rootfolder = now.strftime('MicasenceResult_%Y%m%d_%H%M%S')
    o = os.path.join(OutRoot,rootfolder)
    if os.path.isdir(o):
        o=o+"_2"
    if os.path.isdir(o) == False:
        os.mkdir(o)
        os.mkdir(os.path.join(o,"rgb"))
        os.mkdir(os.path.join(o,"ndvi"))
        os.mkdir(os.path.join(o,"nbi"))
    almat,_ =ReadAllignmentMatrix(".")
    for p in ImagePath:
        print(p)
        try:
            processImage(p,o,almat)
        except:
            print("{} is  not valid".format(p))
        _index = _index +1
    print("Done Send to USB")
    _Running = False
    return


from Allignment import ReadAllignmentMatrix,AllignImage
from NBI import CalNBI , DrawLegend
import os
import json
import requests
import time
import glob
from threading import Thread
import micasense.capture as cap
import numpy as np
import cv2
import argparse
import subprocess

IMGROOT = "./img"
Running = True
def Serve(mat,ip,screensize = (1920,1080)):
    global Running
    cache = {}
    allignmat, havePrev = ReadAllignmentMatrix(".")
    if havePrev == False:
        print('Please do Allignment First')
        return 
    newestIMG = -1
    while(Running):
        url,filename,new = ReadImage(ip,cache)
        if new ==True :
            cache[url] = True
            paths = DownloadImage(url,filename)
            s = int(os.path.basename(paths[0]).split("_")[1])
            if s <= newestIMG:
                continue
            newestIMG = s
            capture = cap.Capture.from_filelist(paths)
            im_aligned = AllignImage(allignmat,capture)
            capture.clear_image_data()
            capture =None
            nbi,mask = CalNBI(im_aligned)
            del im_aligned
            ShowImage(nbi,mask,screensize)
            del nbi 
            del mask
        else:
            time.sleep(0.001)
    print("Stoping NBI Program")
    cv2.destroyAllWindows()
    return


def Stop():
    global Running
    Running = False

def getrequest(request):
    ret = requests.get(request) 
    return ret.content

def DownloadImage(url,files):
    global IMGROOT
    threads = []

    for i in range(5):
        if not os.path.exists(IMGROOT):
            os.makedirs(IMGROOT)
        path = os.path.join(IMGROOT,files.format(i+1))
        t = Thread(target=download,args=(url.format(i+1),path))
        threads.append(t)

    # Start all threads
    for x in threads:
        x.start()

    # Wait for all of them to finish
    for x in threads:
        x.join()
        
    return glob.glob(os.path.join(IMGROOT,files.replace('{}','*')))

def download(url,path):
    #print(url, path)
    myfile= requests.get(url)
    with open(path,'wb') as f:
        f.write(myfile.content)

def ReadImage(ip,cache):
    base_url = ip+"/files"
    sets = json.loads(getrequest(base_url))["directories"]
    if sets == None:
        return None,None,False
    sets_len = len(sets)
    if sets_len == 0 :
        return None,None,False
    sets_url=base_url+"/"+sets[sets_len-1]
    #print(sets_url)
    folders = json.loads(getrequest(sets_url))["directories"]
    folders_len = len(folders)
    if folders_len == 0 :
        print(folders_len)
        return None,None,False
    folders_url = sets_url+"/"+folders[folders_len-1]
    #print(folders_url)
    files = json.loads(getrequest(folders_url))["files"]
    files_len = len(files)
    offset = 1
    suffix = "_5.tif"
    while(files_len-offset >=0): 
        if files[files_len-offset]["name"].endswith(suffix):
            filename = files[files_len-offset]["name"]
            filename = filename.replace(suffix,'') +"_{}.tif"
            files_url = folders_url+"/"+filename
            if cache.get(files_url,None) == None:
                return files_url,filename, True
        offset = offset+1
    return None,None ,False

def ShowImage(NBI,mask,size):
    global im_color_cache
    min = -1.5
    max = 1.5
    lower = NBI < min
    NBI[lower] = min
    del lower
    higher = NBI >max
    NBI[higher] = max    
    del higher
    NBI = ((NBI - min)/(max-min)) * 255.0
    NBI = NBI.astype(np.uint8)
    im_color = cv2.applyColorMap(NBI, cv2.COLORMAP_JET)
    im_color[mask] = [0,0,0]
    im_color = DrawLegend(im_color)

    resize = cv2.resize(im_color,size,interpolation=cv2.INTER_NEAREST)
    cv2.imshow('NBI',resize)
    #cv2.imshow('NBI',im_color)
    cv2.waitKey(50)
    return im_color

def get_screen_resolution():
    output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
    resolution = output.split()[0].split(b'x')
    return {'width': resolution[0], 'height': resolution[1]}
def InitDisplay():
    cv2.namedWindow("NBI", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("NBI",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

def main(ip):
    global Running
    cameraIP= "http://"+ip 
    
    Amat = ReadAllignmentMatrix('.')
    screensize = get_screen_resolution()
    InitDisplay()
    size =(1280,720)
    try:
        size = (int(screensize['width']),int(screensize['height']))
    except:
        print("Fail to Automatic get screen size, set resolution to 1280x720")
    Running = True
    Serve(Amat,cameraIP,screensize=size)
    return 

    
if __name__ == '__main__':
    main()
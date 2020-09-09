import numpy as np
import micasense.imageutils as imageutils
import cv2

kernel = np.ones((5,5),np.float32)/25

def CalNBI(im_aligned):
    global kernel

    norm = np.zeros(im_aligned.shape)
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
    del TCARI 
    del OSAVI
    del norm
    del NDVI
    return NBI, NDVIMASK


def DrawLegend(img):
    a = np.arange(255,dtype=np.uint8)
    a = np.flip(a)
    a = cv2.resize(a,(1,301),interpolation= cv2.INTER_NEAREST)
    t = np.zeros((301,30))
    t[:] = a
    #t = np.transpose(t)
    t  = t.astype(np.uint8)
    print(t)
    t = cv2.applyColorMap(t, cv2.COLORMAP_JET)
    img = cv2.rectangle(img, (40, 115), (80, 426), (255, 255, 255), -1)
    img[120:421, 45:75] = t
    cv2.putText(img, "Low Nitrogen", (40, 90), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "1.5", (100, 130), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "0", (100, 275), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "-1.5", (100, 426), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "High Nitrogen", (40, 480), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 255, 255), 2, cv2.LINE_AA)
    return img

def Calall(im_aligned):
    global kernel
    norm = np.zeros(im_aligned.shape)
    im_sum = (im_aligned[:,:,0]+im_aligned[:,:,1]+im_aligned[:,:,2]+im_aligned[:,:,3]+im_aligned[:,:,4])
    for i in range(im_aligned.shape[2]):
        #norm[:,:,i] = cv2.filter2D(im_aligned[:,:,i]/im_sum,-1,kernel)
        norm[:,:,i] = im_aligned[:,:,i]/im_sum
    OSAVI =  (1+0.16) * (norm[:,:,3]-norm[:,:,2])/(norm[:,:,3]+norm[:,:,2]+0.16)
    TCARI = 3* ((norm[:,:,4]-norm[:,:,2])-
            (0.2*(norm[:,:,4]-norm[:,:,1])*
                (norm[:,:,4]/norm[:,:,2])))
    NDVI = (im_aligned[:,:,3]-im_aligned[:,:,2])/(im_aligned[:,:,3]+im_aligned[:,:,2])
    NBI = TCARI/OSAVI
    del TCARI 
    del OSAVI
    del norm
    rgb = im_aligned[:,:,[0,1,2]]
    return NBI, NDVI,rgb

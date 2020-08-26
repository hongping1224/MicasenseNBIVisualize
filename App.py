from Allignment import ReadAllignmentMatrix,AllignImage
from NBI import CalNBI

def Serve(mat,ip):
    while(True):
        images,new = ReadImage(ip)
        if new ==True :
            alligned = AllignImage(mat,images)
            nbi = CalNBI(alligned)
            ShowImage(nbi)
    return

def ReadImage(ip):
    return None, False

def ShowImage(image):
    return

def main():
    confPath = ""
    cameraIP= ""
    Amat = ReadAllignmentMatrix(confPath)
    Serve(Amat,cameraIP)
    return 

if __name__=="__main__":
    main()

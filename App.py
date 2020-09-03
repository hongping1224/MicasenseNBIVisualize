from Allignment import ReadAllignmentMatrix,AllignImage
from NBI import CalNBI
from flask import Flask
app = Flask(__name__)

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

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0')


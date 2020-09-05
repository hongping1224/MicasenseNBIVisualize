from flask import Flask
app = Flask(__name__)
import subprocess
import os

@app.route('/')
def index():
    return 'Hello World!'

def StartApp():
    return

def GetUSBPath():
    output = subprocess.Popen('ls /media/nuc/ | grep \"\"',shell=True, stdout=subprocess.PIPE).communicate()[0]
    res = output.split(b'\n')
    result = [] 
    for r in res:
        if r == b"":
            continue
        result.append(os.path.join("/media/nuc",r.decode("utf-8") ))
    return result

def WriteToUSB(path):
    return

def SaveCameraIP(ip):
    return



if __name__ == '__main__':
    
    app.debug = True
    app.run('0.0.0.0')


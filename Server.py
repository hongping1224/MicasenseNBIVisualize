from flask import Flask, request, render_template, jsonify, send_file,redirect
app = Flask(__name__)
import subprocess
import os
from threading import Thread
from App import main,Stop
import glob
from Allignment import AutoAllign
from ProcessToUSB import Start, stats

selectedDevice = ['']
selectPath = ""
@app.route('/', methods=['GET', 'POST'])
def index():
    return renderPage()   

def renderPage():
    global selectedDevice,selectPath
    devices = GetUSBPath()
    usbrunning , index , total = stats()
    ip = ReadCameraIP()
    if len(devices) == 0:
        devices = ["No USB Found"]
        selectedDevice = ["Selected"]
    elif len(devices) == 1:
        selectedDevice = ["Selected"]
    else:
        if selectPath in devices:
            selectedDevice = []
            for d in devices:
                if d == selectPath:
                    selectedDevice.append('Selected')
                else:
                    selectedDevice.append('')                
    return render_template('index.html',len = len(devices) ,Devices = devices,SelectedDevice = selectedDevice, cameraIP = ip,show_hidden=usbrunning , processindex =index , totalindex = total) 

@app.route('/Allignment', methods=['GET'])
def ResetAllignment():
    AutoAllign()
    return "Finish Allignment" , 200


NBIProgramThread = None
@app.route('/StartCapture', methods=['GET'])
def StartApp():
    global NBIProgramThread
    if NBIProgramThread is None:
        t = openTerminal()
        NBIProgramThread = t
    return redirect('/')

@app.route('/StopCapture', methods=['GET'])
def StopApp():
    global NBIProgramThread
    if NBIProgramThread is not None:
        Stop()
        print('STOP')
        NBIProgramThread.join()
        print('JOINED')
        NBIProgramThread = None 
    return redirect('/')



@app.route('/ClearStorage', methods=['GET'])
def ClearStorage():
    files = glob.glob("./img/*")
    for f in files:
        os.remove(f)
    return redirect('/')


def openTerminal():
    t = Thread(target=main)
    t.start()
    return t

def GetUSBPath():
    output = subprocess.Popen('ls /media/nuc/ | grep \"\"',shell=True, stdout=subprocess.PIPE).communicate()[0]
    res = output.split(b'\n')
    result = [] 
    for r in res:
        if r == b"":
            continue
        result.append(os.path.join("/media/nuc",r.decode("utf-8") ))
    return result



@app.route('/SaveToUSB', methods=['POST'])
def SaveToUSB():
    usbrunning , _, _ = stats()
    if usbrunning == True:
        return renderPage()
    tmp = request.values['devices']
    if(tmp!= '' and tmp != "No USB Found"):
        print(tmp)
        t = Thread(target=Start,args=(tmp,))
        t.start()
    return redirect('/')

@app.route('/setIP', methods=['GET'])
def setIP():
    ip = request.values['cameraIP']
    if(ip!= ''):
        SaveCameraIP(ip)
    return redirect('/')


def SaveCameraIP(ip):
    with open('cameraIP.txt','w') as w:
        w.write(ip)

def ReadCameraIP():
    if os.path.isfile('cameraIP.txt') == False:
        SaveCameraIP('192.168.11.20')
    with open('cameraIP.txt','r') as r:
        ip=r.readline()
        print(ip)
    return ip

if __name__ == '__main__':
    
    app.debug = True
    app.run('0.0.0.0')


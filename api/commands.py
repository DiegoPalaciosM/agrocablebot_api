import subprocess
import os
import time
import cv2
import threading

import asyncio

from greenlet import getcurrent

from agrocablebot.commands import logger

class CameraEvent(object):
    def __init__(self):
        self.events = {}

    def wait(self):
        ident = getcurrent()
        if ident not in self.events:
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        now = time.time()
        remove = None
        for ident, event in self.events.items():

            if not event[0].isSet():
                event[0].set()
                event[1] = now
            else:
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        self.events[getcurrent()][0].clear()

class Camera:
    def __init__(self, source, cname):
        self.source = source
        self.cname = cname
        self.frame = None
        self.frameData = None
        self.last_access = 0
        self.event = CameraEvent()
        self.thread = None
        
    def create_thread(self):
        if self.thread is None:
            self.camera = cv2.VideoCapture(self.source)
            self.last_access = time.time()

            self.thread = threading.Thread(target=self.thread_function) # type: ignore
            self.thread.start()

            self.event.wait()
        
    def thread_function(self):
        for_frames = self.frames()
        for frame in for_frames:
            self.frame = frame
            self.event.set()
            print (time.time() - self.last_access )
            if time.time() - self.last_access > 1:
                for_frames.close()
                self.camera.release()
                break
        self.thread = None

    def frames(self):
        while True:
            success, img = self.camera.read()
            if not success:
                break
            ret, buffer = cv2.imencode('.jpg', img) 
            self.frameData = img
            yield buffer.tobytes()
    
    def get_frame(self):
        self.last_access = time.time()

        self.event.wait()
        self.event.clear()
        return self.frame


def gen_frame(camera):
    camera.create_thread()
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
def gen_screenshot(self, camera):
    if camera:
        camera.create_thread()
        screenshot = camera.get_frame()
        return screenshot
    return ''

def deviceInfo():
    try:
        ssid = subprocess.check_output(['iwgetid']).decode('utf-8').split('"')[1]
        mac = subprocess.check_output(
            ['cat', '/sys/class/net/wlp2s0/address']).decode('utf-8').strip('\n')
    except:
        ssid = 'error'
        mac = 'error'
    return {'ssid' : ssid, 'mac' : mac, 'name' : 'imacuna'}

def cameraID():
    ids = {'above' : 0, 'below' : 1}
    res = subprocess.run(['v4l2-ctl','--list-devices'], stdout=subprocess.PIPE)
    resDecoded = res.stdout.decode().split('\n')
    for i in range(len(resDecoded)):
        if os.environ['ABOVE_CAMERA'] in resDecoded[i]:
            ids['above'] = int(resDecoded[i+1].strip('\t/dev/video'))
        elif os.environ['BELOW_CAMERA'] in resDecoded[i]:
            ids['below'] = int(resDecoded[i+1].strip('\t/dev/video'))
    return ids

def getIndex(pos):
    aportex = 0.1
    aportey = 1

    pos[0] = pos[0]/100
    pos[1] = pos[1]/100

    x = (pos[0] - pos[0]%1 + 4) + (pos[0]%1 * aportex)
    y = ((-pos[1] + pos[1]%1 + 4) * 9) - ((pos[1]%1 * aportey))
    #(f'X({pos[0]} Y({pos[1]}))',x+y)
    return x+y
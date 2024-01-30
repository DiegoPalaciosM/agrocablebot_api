import subprocess
import os
import time
import cv2
import threading
import imageio
import inspect
import sys
import csv

from greenlet import getcurrent
from json import dumps

from agrocablebot.settings import DATA_PATH
from agrocablebot.commands import logger
from api import models


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
    def __init__(self, source, cname, resolution):
        self.resolution = resolution
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
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, int(self.resolution[0]))
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.resolution[1]))
            self.last_access = time.time()

            self.thread = threading.Thread(target=self.thread_function) # type: ignore
            self.thread.start()

            self.event.wait()
        
    def thread_function(self):
        for_frames = self.frames()
        for frame in for_frames:
            self.frame = frame
            self.event.set()
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

    def save_frame(self, pos, prueba, path=DATA_PATH):
        os.makedirs(f"{path}/{prueba}/fotos/{self.cname}/", exist_ok=True)
        self.create_thread()
        cv2.imwrite(f"{path}/{prueba}/fotos/{self.cname}/{getIndex(pos)}_{pos}.png", self.frameData)


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

def deviceInfo(*args, **kwargs):
    try:
        ssid = subprocess.check_output(['iwgetid']).decode('utf-8').split('"')[1]
        mac = subprocess.check_output(
            ['cat', '/sys/class/net/wlp2s0/address']).decode('utf-8').strip('\n')
    except Exception as error:
        ssid = 'error'
        mac = 'error'
        logger.error(f"{type(error)} {error}")
    return {'ssid' : ssid, 'mac' : mac, 'name' : 'imacuna'}

def cameraInfo():
    ids = {'above' : 0, 'below' : 1}
    resolutions = {'above' : [], 'below' : []}
    res = subprocess.run(['v4l2-ctl','--list-devices'], stdout=subprocess.PIPE)
    resDecoded = res.stdout.decode().split('\n')
    for i in range(len(resDecoded)):
        if os.environ['ABOVE_CAMERA'] in resDecoded[i]:
            ids['above'] = int(resDecoded[i+1].strip('\t/dev/video'))
            temp = subprocess.Popen(['v4l2-ctl', '-d', f'{ids["above"]}', '--list-formats-ext'], stdout=subprocess.PIPE)
            temp2 = subprocess.check_output(('grep', 'x'), stdin=temp.stdout)
            resolutions['above'] = temp2.decode('utf-8').split('\n')[0].split('\t')[2].split(' ')[-1].split('x')
        elif os.environ['BELOW_CAMERA'] in resDecoded[i]:
            ids['below'] = int(resDecoded[i+1].strip('\t/dev/video'))
            temp = subprocess.Popen(['v4l2-ctl', '-d', f'{ids["below"]}', '--list-formats-ext'], stdout=subprocess.PIPE)
            temp2 = subprocess.check_output(('grep', 'x'), stdin=temp.stdout)
            resolutions['below'] = temp2.decode('utf-8').split('\n')[0].split('\t')[2].split(' ')[-1].split('x')
    return ids, resolutions


def offset(value):
    if value >= 0 and value < 180:
        return value * (360 - 180) / 180 + 180
    elif value > 180:
        return (value - 180) * (180 - 0) / (360 - 180) + 0

def getIndex(pos):
    aportex = 0.1
    aportey = 1

    posA = pos
    
    posA['x'] = posA['x']/100 
    posA['y'] = posA['y']/100

    x = (posA['x'] - posA['x']%1 + 4) + (posA['x']%1 * aportex)
    y = ((-posA['y'] + posA['y']%1 + 4) * 9) - ((posA['y']%1 * aportey))
    #(f"X({pos[0]} Y({pos[1]}))",x+y)
    return x+y

def exportGif(prueba):
    try:
        cameras = ['superior', 'inferior']
        for camera in cameras:
            path = f'{DATA_PATH}/{prueba}/fotos/{camera}'
            names = os.listdir(path)
            names.sort()
            images = []
            for n in names:
                images.append(imageio.imread(f'{path}/{n}'))
                imageio.imread(f'{path}/{n}')
            imageio.mimsave(f'{path}.gif', images)
    except Exception as error:
        logger.error(f"{type(error)} error")

def csvWritter(filename, nprueba):
    os.makedirs(f'{filename}', exist_ok=True)
    for name, obj in inspect.getmembers(sys.modules[models.__name__]):
        if inspect.isclass(obj):
            try:
                if hasattr(obj, 'prueba'):
                    registros = obj.objects.filter(prueba = nprueba).values_list()
                    keys = [field.name for field in obj._meta.fields][1:-2]
                    with open(f'{filename}/{obj.name}.csv', 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(keys)
                        writer.writerows([registro[1:-2] for registro in registros])
            except Exception as error:
                logger.error(f"{type(error)} {error}")
    pass
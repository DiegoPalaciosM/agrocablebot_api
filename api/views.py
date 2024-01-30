from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse, FileResponse
from django.utils import timezone

from json import dumps, loads
import sys
import inspect
import datetime
from zoneinfo import ZoneInfo
import os
import shutil

from agrocablebot.settings import DATA_PATH
from agrocablebot.commands import logger
from api.commands import Camera, deviceInfo, gen_frame, cameraInfo, exportGif, csvWritter
from api import models
from mqtt.mqtt import MQTT_CLIENT

camera_ids, camera_resolutions= cameraInfo()
camera = {'/aboveCam/' : Camera(camera_ids['above'], 'superior', camera_resolutions['above']), '/belowCam/' : Camera(camera_ids['below'], 'inferior', camera_resolutions['below'])}

MQTT_CLIENT.cameras = camera
MQTT_CLIENT.client.loop_start()

# Create your views here.

def home(request):
    return render(request, 'home.html', {'prefix':models.Configuracion.objects.get(name = 'numeroPrueba')})

def cameras(request):
    return StreamingHttpResponse(gen_frame(camera[request.path]),content_type='multipart/x-mixed-replace; boundary=frame')

def fetchData(request, sensor):
    for name, obj in inspect.getmembers(sys.modules[models.__name__]):
        if inspect.isclass(obj):
            try:
                if obj.name == sensor:
                    json = loads(request.body.decode('utf-8'))
                    dateInit = timezone.make_aware(datetime.datetime.strptime(json['dateInit'],'%Y-%m-%d %H:%M:%S'), timezone=ZoneInfo("Etc/UTC"))
                    dateEnd = timezone.make_aware(datetime.datetime.strptime(json['dateEnd'],'%Y-%m-%d %H:%M:%S'), timezone=ZoneInfo("Etc/UTC"))
                    data = obj.objects.filter(fecha_creacion__range=(dateInit, dateEnd))                    
                    returnData = []
                    for d in list(data.values()):
                        d["fecha_creacion"] = d["fecha_creacion"].strftime("%Y-%m-%d %H:%M:%S")
                        returnData.append(d)
                    return HttpResponse(dumps(returnData), content_type="application/json")
                    pass
            except Exception as error:
                logger.error(f"{type(error)} {error}")
    return redirect('home')


def apiInfo(request):
    return HttpResponse(dumps(deviceInfo()), content_type="application/json")

def download(request, file = None):
    if file:
        cwd = os.getcwd()
        exportGif(file)
        os.system(f'cd {DATA_PATH} && zip -qr {file}.zip {file} && cd {cwd}')
        csvWritter(f"{DATA_PATH}/{file}/csv", file)
        with open(os.path.join(DATA_PATH, f'{file}.zip'), 'rb') as f:
                data = f.readlines()
        os.remove(os.path.join(DATA_PATH, f'{file}.zip'))
        return FileResponse(data, content_type='application/zip')
        return redirect('download')
    files = [elemento for elemento in os.listdir(DATA_PATH) if '.' not in elemento]
    return render(request, 'download.html', {'files' : files})

def delete(request, file):
    if file:
        shutil.rmtree(f'{DATA_PATH}/{file}')
    return redirect('download')

def changePrefix(request, prefix=None):
    print (request.method)
    if prefix:
        print (prefix)
        temp = models.Configuracion.objects.get(name = 'numeroPrueba')
        temp.data = prefix
        temp.save()
    return redirect('home')

def test(request):
    html = ''
    
    return HttpResponse(html)
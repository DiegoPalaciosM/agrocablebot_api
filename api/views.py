from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.utils import timezone

from json import dumps, loads
import sys, inspect
import datetime
from zoneinfo import ZoneInfo

from api.commands import Camera, deviceInfo, gen_frame
from api import models

camera = {'/aboveCamera/' : Camera(2, 'superior'), '/belowCamera/' : Camera(0, 'inferior')}


# Create your views here.

def home(request):
    return render(request, 'home.html')

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
            except Exception as e:
                pass        
    return redirect('home')


def apiInfo(request):
    return deviceInfo()

def test(request):
    html = ''
    
    return HttpResponse(html)
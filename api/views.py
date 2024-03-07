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
from api.commands.camera import AboveCamera, BelowCamera, gen_frame, exportGif
from api.commands.functions import csvWritter
from api.commands.information import deviceInfo
from api import models
from api.commands.mqtt import MqttClient

MqttClient()

# Create your views here.

def home(request):
    """
    Vista para la página de inicio.

    Esta vista renderiza la plantilla 'home.html' y pasa el valor de 'numeroPrueba' de la configuración como contexto.

    Parámetros:
    request (HttpRequest): La solicitud HTTP recibida.

    Returns:
    HttpResponse: Una respuesta HTTP que renderiza la plantilla 'home.html'.
    """
    return render(request, 'home.html', {'prefix':models.Configuracion.objects.get(name = 'numeroPrueba')})

def cameras(request):
    """
    Vista para el streaming de las cámaras.

    Esta vista devuelve una respuesta de transmisión multipart/x-mixed-replace que contiene los fotogramas de la cámara solicitada.

    Parámetros:
    request (HttpRequest): La solicitud HTTP recibida.

    Returns:
    StreamingHttpResponse: Una respuesta de transmisión multipart/x-mixed-replace que contiene los fotogramas de la cámara.
    """
    camera = AboveCamera() if request.path == '/aboveCam/' else BelowCamera() if request.path == '/belowCam/' else None
    return StreamingHttpResponse(gen_frame(camera),content_type='multipart/x-mixed-replace; boundary=frame')

def fetchData(request, sensor):
    """
    Vista para obtener datos de un sensor en un rango de tiempo específico.

    Esta vista devuelve los datos del sensor especificado en formato JSON dentro del rango de tiempo proporcionado en la solicitud.

    Parámetros:
    request (HttpRequest): La solicitud HTTP recibida.
    sensor (str): El nombre del sensor del cual obtener los datos.

    Returns:
    HttpResponse: Una respuesta HTTP que contiene los datos del sensor en formato JSON.
    """
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
    """
    Vista para obtener información del dispositivo en formato JSON.

    Esta vista devuelve la información del dispositivo en formato JSON.

    Parámetros:
    request (HttpRequest): La solicitud HTTP recibida.

    Returns:
    HttpResponse: Una respuesta HTTP que contiene la información del dispositivo en formato JSON.
    """
    return HttpResponse(dumps(deviceInfo()), content_type="application/json")

def download(request, file = None):
    """
    Vista para descargar un archivo.

    Esta vista permite descargar un archivo previamente exportado como un archivo ZIP junto con un archivo CSV que contiene los datos del archivo.

    Parámetros:
    request (HttpRequest): La solicitud HTTP recibida.
    file (str, opcional): El nombre del archivo a descargar.

    Returns:
    FileResponse: Una respuesta HTTP que contiene el archivo ZIP para descargar.
    HttpResponse: Una respuesta HTTP que renderiza la plantilla 'download.html'.
    """
    if file:
        cwd = os.getcwd()
        exportGif(file)
        os.system(f'cd {DATA_PATH} && zip -qr {file}.zip {file} && cd {cwd}')
        csvWritter(f"{DATA_PATH}/{file}/csv", file, models)
        with open(os.path.join(DATA_PATH, f'{file}.zip'), 'rb') as f:
                data = f.readlines()
        os.remove(os.path.join(DATA_PATH, f'{file}.zip'))
        return FileResponse(data, content_type='application/zip')
        return redirect('download')
    os.makedirs(DATA_PATH, exist_ok=True)
    files = [elemento for elemento in os.listdir(DATA_PATH) if '.' not in elemento]
    return render(request, 'download.html', {'files' : files})

def delete(request, file):
    """
    Vista para eliminar un archivo.

    Esta vista elimina un archivo y su carpeta asociada del sistema de archivos.

    Parámetros:
    request (HttpRequest): La solicitud HTTP recibida.
    file (str): El nombre del archivo a eliminar.

    Returns:
    HttpResponseRedirect: Una respuesta HTTP que redirige al usuario de vuelta a la página de descargas.
    """
    if file:
        shutil.rmtree(f'{DATA_PATH}/{file}')
    return redirect('download')

def changePrefix(request, prefix=None):
    """
    Vista para cambiar el prefijo de la configuración.

    Esta vista permite cambiar el valor del prefijo en la configuración.

    Parámetros:
    request (HttpRequest): La solicitud HTTP recibida.
    prefix (str, opcional): El nuevo valor del prefijo.

    Returns:
    HttpResponseRedirect: Una respuesta HTTP que redirige al usuario de vuelta a la página de inicio.
    """
    if prefix:
        temp = models.Configuracion.objects.get(name = 'numeroPrueba')
        temp.data = prefix
        temp.save()
    return redirect('home')

def changeName(request, name=None):
    if name:
        temp = models.Configuracion.objects.get(name = 'nombreDispositivo')
        temp.data = name
        temp.save()
    return redirect('home')

def test(request):
    html = ''
    
    return HttpResponse(html)
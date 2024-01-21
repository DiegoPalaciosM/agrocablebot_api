from django.shortcuts import render

from django.http import HttpResponse, StreamingHttpResponse

from api.commands import Camera, deviceInfo, gen_frame

camera = {'/aboveCamera/' : Camera(0, 'superior'), '/belowCamera/' : Camera('http://192.168.1.6:4747/video', 'inferior')}

import threading

# Create your views here.

def home(request):
    return render(request, 'home.html')

def apiInfo(request):
    return deviceInfo()

def dashboard(request):
    return render(request, 'dashboard.html')

def cameras(request):
    return StreamingHttpResponse(gen_frame(camera[request.path]),content_type='multipart/x-mixed-replace; boundary=frame')

def test(request):
    html = ''
    for th in threading.enumerate():
        html += th.name + '\n'
    return HttpResponse(html)
from django.shortcuts import render

from django.http import HttpResponse, StreamingHttpResponse

from api.commands import Camera, deviceInfo, gen_frame

camera = {'/aboveCamera/' : Camera(2, 'superior'), '/belowCamera/' : Camera(0, 'inferior')}


# Create your views here.

def home(request):
    return render(request, 'home.html')

def apiInfo(request):
    return deviceInfo()

def dashboard(request):
    return render(request, 'dashboard.html')

def cameras(request):
    print (request.path)
    return StreamingHttpResponse(gen_frame(camera[request.path]),content_type='multipart/x-mixed-replace; boundary=frame')

def test(request):
    html = ''
    
    return HttpResponse(html)
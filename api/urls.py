from django.urls import path
from django.http import StreamingHttpResponse

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aboveCamera/', views.cameras, name='aboveCamera'),
    path('belowCamera/', views.cameras, name='belowCamera'),
    path('data/<sensor>', views.fetchData, name='fetchData'),
    path('deviceInfo', views.deviceInfo, name='deviceInfo'),
    path('test/', views.test, name='test')
]

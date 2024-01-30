from django.urls import path
from django.http import StreamingHttpResponse

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('aboveCam/', views.cameras, name='aboveCamera'),
    path('belowCam/', views.cameras, name='belowCamera'),
    path('data/<sensor>', views.fetchData, name='fetchData'),
    path('deviceInfo', views.apiInfo, name='deviceInfo'),
    path('download/', views.download, name='download'),
    path('download/<file>', views.download, name='downloadFile'),
    path('delete/<file>', views.delete, name='deleteFile'),
    path("changePrefix/<prefix>", views.changePrefix, name="changePrefix"),
    path('test/', views.test, name='test')
]

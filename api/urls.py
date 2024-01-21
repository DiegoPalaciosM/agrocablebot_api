from django.urls import path
from django.http import StreamingHttpResponse

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('data/<sensor>', views.home, name='startBot'),
    path('sensors', views.home, name='stopBot'),
    path('changePrefix/<id>', views.home, name='botStatus'),
    path('download/', views.home, name='botStatus'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('aboveCamera/', views.cameras),
    path('belowCamera/', views.cameras),
    path('test/', views.test, name='test')
]

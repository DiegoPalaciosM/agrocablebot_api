from django.db import models

import datetime

from api.commands.functions import getIndex

# Create your models here.

class Acelerometro(models.Model):
    name = "acelerometro"
    pitch = models.FloatField()
    roll = models.FloatField()
    yaw = models.FloatField()
    prueba = models.IntegerField()
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    pos_id = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now = True)

    def build_data(self, json, pos):
        self.pitch = json['pitch']
        self.roll = json['roll']
        self.yaw = json['yaw']
        self.prueba = Configuracion.objects.get(name='numeroPrueba').data
        self.pos_x = pos['x']
        self.pos_y = pos['y']
        self.pos_z = pos['z']
        self.pos_id = getIndex(pos)
        self.fecha_creacion = datetime.datetime.now()
        return json

class Giroscopio(models.Model):
    name = "giroscopio"    
    pitch = models.FloatField()
    roll = models.FloatField()
    yaw = models.FloatField()
    prueba = models.IntegerField()
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    pos_id = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now = True)

    def build_data(self, json, pos):
        self.pitch = json['pitch']
        self.roll = json['roll']
        self.yaw = json['yaw']
        self.prueba = Configuracion.objects.get(name='numeroPrueba').data
        self.pos_x = pos['x']
        self.pos_y = pos['y']
        self.pos_z = pos['z']
        self.pos_id = getIndex(pos)
        self.fecha_creacion = datetime.datetime.now()
        return json

class Magnetometro(models.Model):
    name = "magnetometro"
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    prueba = models.IntegerField()
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    pos_id = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now = True)

    def build_data(self, json, pos):
        self.x = json['x']
        self.y = json['y']
        self.z = json['z']
        self.prueba = Configuracion.objects.get(name='numeroPrueba').data
        self.pos_x = pos['x']
        self.pos_y = pos['y']
        self.pos_z = pos['z']
        self.pos_id = getIndex(pos)
        self.fecha_creacion = datetime.datetime.now()
        return json

class Orientacion(models.Model):
    name = "orientacion"
    pitch = models.FloatField()
    roll = models.FloatField()
    yaw = models.FloatField()
    prueba = models.IntegerField()
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    pos_id = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now = True)

    def build_data(self, json, pos):
        self.pitch = json['pitch']
        self.roll = json['roll']
        self.yaw = json['yaw']
        self.prueba = Configuracion.objects.get(name='numeroPrueba').data
        self.pos_x = pos['x']
        self.pos_y = pos['y']
        self.pos_z = pos['z']
        self.pos_id = getIndex(pos)
        self.fecha_creacion = datetime.datetime.now()
        return json

class Humedad(models.Model):
    name = "humedad"
    value = models.FloatField()
    prueba = models.IntegerField()
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    pos_id = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now = True)

    def build_data(self, json, pos):
        self.value = json['value']
        self.prueba = Configuracion.objects.get(name='numeroPrueba').data
        self.pos_x = pos['x']
        self.pos_y = pos['y']
        self.pos_z = pos['z']
        self.pos_id = getIndex(pos)
        self.fecha_creacion = datetime.datetime.now()
        return json

class Presion(models.Model):
    name = "presion"
    value = models.FloatField()
    prueba = models.IntegerField()
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    pos_id = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now = True)

    def build_data(self, json, pos):
        self.value = json['value']
        self.prueba = Configuracion.objects.get(name='numeroPrueba').data
        self.pos_x = pos['x']
        self.pos_y = pos['y']
        self.pos_z = pos['z']
        self.pos_id = getIndex(pos)
        self.fecha_creacion = datetime.datetime.now()
        return json

class Temperatura(models.Model):
    name = "temperatura"
    value = models.FloatField()
    prueba = models.IntegerField()
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    pos_id = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now = True)

    def build_data(self, json, pos):
        self.value = json['value']
        self.prueba = Configuracion.objects.get(name='numeroPrueba').data
        self.pos_x = pos['x']
        self.pos_y = pos['y']
        self.pos_z = pos['z']
        self.pos_id = getIndex(pos)
        self.fecha_creacion = datetime.datetime.now()
        return json

class Configuracion(models.Model):
    name = models.TextField(blank=True)
    data = models.TextField(blank=True)
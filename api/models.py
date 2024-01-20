from django.db import models

# Create your models here.

class Acelerometro(models.Model):
    pitch = models.FloatField()
    roll = models.FloatField()
    yaw = models.FloatField()
    prueba = models.IntegerField()
    fecha_creacion = models.DateTimeField()

class Giroscopio(models.Model):
    pitch = models.FloatField()
    roll = models.FloatField()
    yaw = models.FloatField()
    prueba = models.IntegerField()
    fecha_creacion = models.DateTimeField()

class Magnetometro(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    prueba = models.IntegerField()
    fecha_creacion = models.DateTimeField()

class Humedad(models.Model):
    value = models.FloatField()
    prueba = models.IntegerField()
    fecha_creacion = models.DateTimeField()

class Presion(models.Model):
    value = models.FloatField()
    prueba = models.IntegerField()
    fecha_creacion = models.DateTimeField()

class Temperatura(models.Model):
    value = models.FloatField()
    prueba = models.IntegerField()
    fecha_creacion = models.DateTimeField()

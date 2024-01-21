from django.db import models

# Create your models here.

class Acelerometro(models.Model):
    pitch = models.FloatField()
    roll = models.FloatField()
    yaw = models.FloatField()
    prueba = models.IntegerField()
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    pos_id = models.IntegerField()
    fecha_creacion = models.DateTimeField()

class Giroscopio(models.Model):
    pitch = models.FloatField()
    roll = models.FloatField()
    yaw = models.FloatField()
    prueba = models.IntegerField()
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    pos_id = models.IntegerField()
    fecha_creacion = models.DateTimeField()

class Magnetometro(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()
    prueba = models.IntegerField()
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    pos_id = models.IntegerField()
    fecha_creacion = models.DateTimeField()

class Orientacion(models.Model):
    pitch = models.FloatField()
    roll = models.FloatField()
    yaw = models.FloatField()
    prueba = models.IntegerField()
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    pos_id = models.IntegerField()
    fecha_creacion = models.DateTimeField()

class Humedad(models.Model):
    value = models.FloatField()
    prueba = models.IntegerField()
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    pos_id = models.IntegerField()
    fecha_creacion = models.DateTimeField()

class Presion(models.Model):
    value = models.FloatField()
    prueba = models.IntegerField()
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    pos_id = models.IntegerField()
    fecha_creacion = models.DateTimeField()

class Temperatura(models.Model):
    value = models.FloatField()
    prueba = models.IntegerField()
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    pos_id = models.IntegerField()
    fecha_creacion = models.DateTimeField()

class Configuracion(models.Model):
    filePrefix = models.IntegerField()
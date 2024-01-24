import django
import os
import uuid
from json import dumps, loads
from sense_emu import SenseHat
import paho.mqtt.client as mqtt

from agrocablebot.commands import logger
from api import commands
from api.models import *


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrocablebot.settings')
django.setup()

class MQTT:
    instance = None

    def __new__(self, *args, **kwargs):
        if not self.instance:
            instance = super(MQTT, self).__new__(self)
            self.instance = instance
        return self.instance

    def __init__(self):
        self.client = mqtt.Client(
            client_id=f'apiClient-{uuid.uuid4()}', 
            clean_session=True,
            userdata=None,
            protocol=mqtt.MQTTv311,
            transport='tcp'
            )
        self.client.username_pw_set(os.environ['MQTT_BROKER_USERNAME'], os.environ['MQTT_BROKER_PASSWORD'])
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        #self.client.on_disconnect = self.on_disconnect
        self.client.connect(os.environ['MQTT_BROKER_HOST'], int(os.environ['MQTT_BROKER_PORT']))
        self.sense = SenseHat()
        self.topics = {'comandos' : self.comandos, 'status' : self.status}
        self.interfaceCommands = {'send_data' : self.send_data, 'send_aio' : self.send_aio}
        self.last_position = {'x' : 0, 'y' : 0, 'z' : 0}
    
    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('comandos')
        self.client.subscribe('status')

    def on_message(self, client, userdata, msg):
        try:
            self.topics[msg.topic](loads(msg.payload.decode('utf-8')))
        except Exception as error:
            logger.error(f"{type(error)} {error}")

    def on_publish(self, client, userdata, result):
        pass

    def on_disconnect(self, client, userdata, rc):
        pass
        #self.client.loop_stop()
        #self.client.loop_start()
    
    def comandos(self, message):
        if message.get('interface'):
            self.interfaceCommands[message['interface']]()
            

    def status(self, message):
        if (any(key in ['x', 'y', 'z'] for key in message.keys())):
            self.last_position = message

    
    def send_aio(self):
        sensores = {
            'acelerometro': {x: round(float(y),4) for x, y in self.sense.get_accelerometer().items()},
            'giroscopio': {x: round(float(commands.offset(y)),4) for x, y in self.sense.get_gyroscope().items()},
            'magnetometro': {x: round(float(y),4) for x, y in self.sense.get_compass_raw().items()},
            'orientacion': {x: round(float(commands.offset(y)),4) for x, y in self.sense.get_orientation().items()},
            'humedad': {'value': round(float(self.sense.get_humidity()),4)},
            'presion': {'value': round(float(self.sense.get_pressure()),4)},
            'temperatura': {'value': round(float(self.sense.get_temperature()),4)},
        }
        self.client.publish('sensores', dumps(sensores))

    def send_data(self):
        acel = Acelerometro()
        giro = Giroscopio()
        magn = Magnetometro()
        orie = Orientacion()
        hume = Humedad()
        pres = Presion()
        temp = Temperatura()
        self.client.publish(
            'sensores/acelerometro', dumps(acel.build_data({x: round(float(y),4) for x, y in self.sense.get_accelerometer().items()}, self.last_position)))
        self.client.publish(
            'sensores/giroscopio', dumps(giro.build_data({x: round(float(commands.offset(y)),4) for x, y in self.sense.get_gyroscope().items()}, self.last_position)))
        self.client.publish(
            'sensores/magnetometro', dumps(magn.build_data({x: round(float(y),4) for x, y in self.sense.get_compass_raw().items()}, self.last_position)))
        self.client.publish(
            'sensores/orientacion', dumps(orie.build_data({x: round(float(y),4) for x, y in self.sense.get_orientation().items()}, self.last_position)))
        self.client.publish(
            'sensores/humedad', dumps(hume.build_data({'value': round(float(self.sense.get_humidity()), 4)}, self.last_position)))
        self.client.publish(
            'sensores/presion', dumps(pres.build_data({'value': round(float(self.sense.get_pressure()),4)}, self.last_position)))
        self.client.publish(
            'sensores/temperatura', dumps(temp.build_data({'value': round(float(self.sense.get_temperature()),4)}, self.last_position)))
        acel.save()
        giro.save()
        magn.save()
        orie.save()
        hume.save()
        pres.save()
        temp.save()
        self.cameras['/aboveCam/'].save_frame(self.last_position, Configuracion.objects.get(name='numeroPrueba').data)
        self.cameras['/belowCam/'].save_frame(self.last_position, Configuracion.objects.get(name='numeroPrueba').data)
        


MQTT_CLIENT = MQTT()
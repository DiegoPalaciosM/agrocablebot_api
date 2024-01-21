import django
import paho.mqtt.client as mqtt
import os
import uuid
from json import dumps, loads
from sense_emu import SenseHat

from . import commands

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agrocablebot.settings')
django.setup()

class MQTT:
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
        self.filePrefix = 0
    
    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('comandos')
        self.client.subscribe('status')

    def on_message(self, client, userdata, msg):
        try:
            self.topics[msg.topic](loads(msg.payload.decode('utf-8')))
        except Exception as e:
            print (e)

    def on_publish(self, client, userdata, result):
        print (result)

    def on_disconnect(self, client, userdata, rc):
        print (client, userdata, rc)
        #self.client.loop_stop()
        #self.client.loop_start()
    
    def comandos(self, message):
        print ('comandos')
        if message.get('interface'):
            self.interfaceCommands[message['interface']]()

    def status(self, message):
        print ('status')
        if (any(key in ['x', 'y', 'z'] for key in message.keys())):
            self.last_position = message
    
    def send_aio(self):
        print ('send_aio')
        sensores = {
            'acelerometro': {x: round(float(y),4) for x, y in self.sense.get_accelerometer_raw().items()},
            'giroscopio': {x: round(float(commands.offset(y)),4) for x, y in self.sense.get_gyroscope().items()},
            'magnetometro': {x: round(float(y),4) for x, y in self.sense.get_compass_raw().items()},
            'orientacion': {x: round(float(commands.offset(y)),4) for x, y in self.sense.get_orientation().items()},
            'humedad': {'value': round(float(self.sense.get_humidity()),4)},
            'presion': {'value': round(float(self.sense.get_pressure()),4)},
            'temperatura': {'value': round(float(self.sense.get_temperature()),4)},
        }
        self.client.publish('sensores', dumps(sensores))

    def send_data(self):
        print ('send_data')
        self.client.publish(
            'sensores/acelerometro', dumps({x: round(float(y),4) for x, y in self.sense.get_accelerometer_raw().items()}))
        self.client.publish(
            'sensores/giroscopio', dumps({x: round(float(commands.offset(y)),4) for x, y in self.sense.get_gyroscope().items()}))
        self.client.publish(
            'sensores/magnetometro', dumps({x: round(float(y),4) for x, y in self.sense.get_compass_raw().items()}))
        self.client.publish(
            'sensores/orientacion', dumps({x: round(float(y),4) for x, y in self.sense.get_orientation().items()}))
        self.client.publish(
            'sensores/humedad', dumps({'value': round(float(self.sense.get_humidity()), 4)}))
        self.client.publish(
            'sensores/presion', dumps({'value': round(float(self.sense.get_pressure()),4)}))
        self.client.publish(
            'sensores/temperatura', dumps({'value': round(float(self.sense.get_temperature()),4)}))

mqtt = MQTT()
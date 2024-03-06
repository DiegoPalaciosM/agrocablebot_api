import django
import os
import uuid
from json import dumps, loads
from sense_emu import SenseHat
#from sense_hat import SenseHat
import paho.mqtt.client as mqtt

from agrocablebot.commands import logger, singleton
from api.commands.functions import offset
from api.commands.camera import AboveCamera, BelowCamera
from api.models import *

@singleton
class MqttClient:
    """
    Clase para manejar un cliente MQTT.

    Esta clase proporciona métodos para conectar y comunicarse con un servidor MQTT, así como para manejar mensajes recibidos.

    Attributes:
    __client (mqtt.Client): Cliente MQTT para la comunicación con el servidor.
    sense (SenseHat): Instancia de SenseHat para obtener datos de sensores.
    topics (dict): Diccionario que mapea nombres de topics MQTT a métodos de manejo de mensajes.
    interfaceCommands (dict): Diccionario que mapea nombres de comandos de interfaz a métodos de la instancia.
    last_position (dict): Última posición registrada del dispositivo.
    """
    def __init__(self):
        """
        Inicializa el cliente MQTT y otros atributos.
        """
        self.__client = mqtt.Client(
            client_id=f'apiClient-{uuid.uuid4()}', 
            clean_session=True,
            userdata=None,
            protocol=mqtt.MQTTv311,
            transport='tcp'
            )
        self.__client.username_pw_set(os.environ['MQTT_BROKER_USERNAME'], os.environ['MQTT_BROKER_PASSWORD'])
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.on_publish = self.__on_publish
        self.__client.on_disconnect = self.__on_disconnect
        self.__client.connect(os.environ['MQTT_BROKER_HOST'], int(os.environ['MQTT_BROKER_PORT']))
        self.sense = SenseHat()
        self.topics = {'comandos' : self.__comandos, 'status' : self.__status}
        self.interfaceCommands = {'send_data' : self.send_data, 'send_aio' : self.send_aio}
        self.last_position = {'x' : 0, 'y' : 0, 'z' : 0}
        self.__client.loop_start()      
            
    def __on_connect(self, client, userdata, flags, rc):
        """
        Método de devolución de llamada para manejar la conexión exitosa al servidor MQTT.
        """
        self.__client.subscribe('comandos')
        self.__client.subscribe('status')
        self.__client.publish('testingimacuna', 'pos si se conectó')

    def __on_message(self, client, userdata, msg):
        """
        Método de devolución de llamada para manejar mensajes MQTT entrantes.
        """
        try:
            self.topics[msg.topic](loads(msg.payload.decode('utf-8')))
        except Exception as error:
            logger.error(f"{type(error)} {error}")

    def __on_publish(self, client, userdata, result):
        pass

    def __on_disconnect(self, client, userdata, rc):
        pass
        #self.__client.loop_stop()
        #self.__client.loop_start()
    
    def __comandos(self, message):
        """
        Método para manejar los mensajes recibidos en el topic 'comandos'.
        """
        if message.get('interface'):
            pass
            self.interfaceCommands[message['interface']]()
            

    def __status(self, message):
        """
        Método para manejar los mensajes recibidos en el topic 'status'.
        """
        if (any(key in ['x', 'y', 'z'] for key in message.keys())):
            self.last_position = message

    
    def send_aio(self):
        """
        Método para publicar datos de sensores en un topic MQTT llamado 'sensores'.
        """
        sensores = {
            'acelerometro': {x: round(float(y),4) for x, y in self.sense.get_accelerometer().items()},
            'giroscopio': {x: round(float(offset(y)),4) for x, y in self.sense.get_gyroscope().items()},
            'magnetometro': {x: round(float(y),4) for x, y in self.sense.get_compass_raw().items()},
            'orientacion': {x: round(float(offset(y)),4) for x, y in self.sense.get_orientation().items()},
            'humedad': {'value': round(float(self.sense.get_humidity()),4)},
            'presion': {'value': round(float(self.sense.get_pressure()),4)},
            'temperatura': {'value': round(float(self.sense.get_temperature()),4)},
        }
        self.__client.publish('sensores', dumps(sensores))

    def send_data(self):
        """
        Método para publicar datos de sensores en topics MQTT específicos y guardar los datos en la base de datos.
        """
        acel = Acelerometro()
        giro = Giroscopio()
        magn = Magnetometro()
        orie = Orientacion()
        hume = Humedad()
        pres = Presion()
        temp = Temperatura()
        self.__client.publish(
            'sensores/acelerometro', dumps(acel.build_data({x: round(float(y),4) for x, y in self.sense.get_accelerometer().items()}, self.last_position)))
        self.__client.publish(
            'sensores/giroscopio', dumps(giro.build_data({x: round(float(offset(y)),4) for x, y in self.sense.get_gyroscope().items()}, self.last_position)))
        self.__client.publish(
            'sensores/magnetometro', dumps(magn.build_data({x: round(float(y),4) for x, y in self.sense.get_compass_raw().items()}, self.last_position)))
        self.__client.publish(
            'sensores/orientacion', dumps(orie.build_data({x: round(float(y),4) for x, y in self.sense.get_orientation().items()}, self.last_position)))
        self.__client.publish(
            'sensores/humedad', dumps(hume.build_data({'value': round(float(self.sense.get_humidity()), 4)}, self.last_position)))
        self.__client.publish(
            'sensores/presion', dumps(pres.build_data({'value': round(float(self.sense.get_pressure()),4)}, self.last_position)))
        self.__client.publish(
            'sensores/temperatura', dumps(temp.build_data({'value': round(float(self.sense.get_temperature()),4)}, self.last_position)))
        acel.save()
        giro.save()
        magn.save()
        orie.save()
        hume.save()
        pres.save()
        temp.save()
        AboveCamera.save_frame(self.last_position, Configuracion.objects.get(name='numeroPrueba').data)
        BelowCamera.save_frame(self.last_position, Configuracion.objects.get(name='numeroPrueba').data)

    def publish(self, topic, message):
        """
        Método para publicar un mensaje MQTT en un topic específico.
        """
        self.__client.publish(topic, message)
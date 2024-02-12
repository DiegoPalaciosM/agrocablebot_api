from sense_emu import SenseHat
from json import dumps, loads
from commands import logger, offset

class SENSORES:
    def __init__(self, mqtt):
        self.mqtt = mqtt
        self.interfaceCommands = {'send_data' : self.splittedData, 'send_aio' : self.sensores}
        self.mqtt.client.on_message = self.on_message
        self.sense = SenseHat()
        pass

    def on_message(self, client, userdata, msg):
        try:
            if msg.topic == "comandos":
                print (msg.payload.decode("utf-8"))
                message = loads(msg.payload.decode("utf-8"))
                if message.get('interface'):
                    command = message['interface']
                    self.interfaceCommands[command]()
        except Exception as e:
            print ('aca',   e)
                

    def sensores(self):
        logger.info('sensores')
        sensores = {
            "humedad": {"value": round(float(self.sense.get_humidity()),4)},
            "temperatura": {"value": round(float(self.sense.get_temperature()),4)},
            "presion": {"value": round(float(self.sense.get_pressure()),4)},
            "compass": {x: round(float(y),4) for x, y in self.sense.get_compass_raw().items()},
            "acelerometro": {x: round(float(y),4) for x, y in self.sense.get_accelerometer_raw().items()},
            "giroscopio": {x: round(float(offset(y)),4) for x, y in self.sense.get_gyroscope().items()}
        }
        self.mqtt.client.publish("sensores", dumps(sensores))

    def splittedData(self):
        print (dumps({x: round(float(offset(y)),4) for x, y in self.sense.get_gyroscope().items()}))
        logger.info('splittedData')
        self.mqtt.client.publish(
            "sensores/humedad", dumps({'value': round(float(self.sense.get_humidity()), 4)}))
        self.mqtt.client.publish(
            "sensores/temperatura", dumps({'value': round(float(self.sense.get_temperature()),4)}))
        self.mqtt.client.publish(
            "sensores/presion", dumps({'value': round(float(self.sense.get_pressure()),4)}))
        self.mqtt.client.publish(
            "sensores/compass", dumps({x: round(float(y),4) for x, y in self.sense.get_compass_raw().items()}))
        self.mqtt.client.publish(
            "sensores/acelerometro", dumps({x: round(float(y),4) for x, y in self.sense.get_accelerometer_raw().items()}))
        self.mqtt.client.publish(
            "sensores/giroscopio", dumps({x: round(float(offset(y)),4) for x, y in self.sense.get_gyroscope().items()}))

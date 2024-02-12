import paho.mqtt.client as mqtt
from commands import logger


class MQTT:
    def __init__(self, name: str = '', user: str = '', password: str = '', host: str = '', port: int = 0):
        self.client = mqtt.Client(client_id=name, clean_session=True,
                                  userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.username_pw_set(
            user, password)
        self.client.connect(host, port)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe('comandos')
        logger.info('Connected')

    def on_message(self, client, userdata, msg):
        # logger.debug(f'{msg.topic}-{msg.payload.decode("utf-8")}')
        pass

    def on_publish(self, client, userdata, result):
        # logger.debug('Data sended')
        pass

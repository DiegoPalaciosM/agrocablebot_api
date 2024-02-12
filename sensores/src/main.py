from mqtt import MQTT
from sensores import SENSORES
from threads import mThread
import os


if __name__ == '__main__':
    mqtt = MQTT('sensores', os.environ['MQTT_USERNAME'], os.environ['MARIADB_PASSWORD'], os.environ['SERVER_HOST'], 1883)
    sensores = SENSORES(mqtt)
    while True:
        pass
    # autoSensores = mThread(sensores.auto_data, 10)
    # autoSensores.start()
    # while True:
    #     din = input()
    #     if din == "toggle":
    #         autoSensores.toggle()
    #     elif din == "send":
    #         sensores.auto_data()
    #     elif din == "exit":
    #         exit()

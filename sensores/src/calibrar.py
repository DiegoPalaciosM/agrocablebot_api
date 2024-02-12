#from sense_hat import SenseHat
import time
from json import dumps

#sense = SenseHat()
#sense.set_imu_config(True, True, True)

def get_offset(sense):
    offset = {'pitch' : 0, 'roll' : 0, 'yaw' : 0}
    count = 0

    for i in range(1, 101):
        offset['pitch'] += sense.get_gyroscope()['pitch']
        offset['roll'] += sense.get_gyroscope()['roll']
        offset['yaw'] += sense.get_gyroscope()['yaw']
        count += 1
    for key, value in offset.items():
        offset[key] = value/count
    return offset

if __name__ == "__main__":


    from mqtt import MQTT

    mqtt = MQTT('testjjnm', 'imacuna', 'pi', '192.168.0.105', 1883)

    try:
        while True:
            mqtt.client.publish("comandos", dumps({"interface" : "send_data"}))
            time.sleep(10)
    except:
        exit()

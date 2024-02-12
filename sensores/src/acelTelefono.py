from commands import logger, Kalman

import time
import numpy as np

init = time.time()
offset = 0
sumatoria = np.matrix(np.zeros(shape=(3,1)))

kalman = Kalman(3,3)
kalman.h = np.matrix(np.identity(kalman.n_state))
kalman.r *= 0.01

tiniA = time.time()
tini = time.time()
count = 0

import websocket
import json


def on_message(ws, message):
    global count
    global offset
    global sumatoria
    global kalman
    global tini
    global tiniA

    data = json.loads(message)['values']


    if count < 100:
        sumatoria += np.matrix([data[0],data[1],data[2]]).getT()
        count += 1
        print (count)
        return
    if count == 100:
        offset = sumatoria / count
        count += 1
        tiniA = time.time()
    
    Am = np.matrix([round(data[0]-offset.item(0),8),round(data[1]-offset.item(1),8),round(data[2]-offset.item(2),8)]).getT() - 0

    if kalman.init:
        kalman.x = Am
        kalman.init = False

    kalman.update(Am)
    kalman.predict()

    kalman.dt = time.time() - kalman.tini

    if any(A[0] > 0.05 or A[0] < -0.05 for A in Am.tolist()):

        kalman.updateV(Am)
        kalman.updateP(Am)
     
    else:

        kalman.vk1 = np.matrix(np.zeros(shape=(kalman.n_sensors, 1)))
        kalman.pk1 = np.matrix(np.zeros(shape=(kalman.n_sensors, 1)))
        
        kalman.Vk = np.matrix(np.zeros(shape=(kalman.n_sensors, 1)))
        kalman.Pk = np.matrix(np.zeros(shape=(kalman.n_sensors, 1)))

    kalman.tini = time.time()

    if time.time() - tini > 1:
        try:
            print ('A: ', Am.getT())
            print ('V: ', kalman.Vk.getT())
            print ('P: ', kalman.Pk.getT())
            print (time.time() - tiniA)
        except:
            pass
        tini = time.time()
 

def on_error(ws, error):
    print("error occurred ", error)
    exit()
    
def on_close(ws, close_code, reason):
    print("connection closed : ", reason)
    exit()
    
def on_open(ws):
    print("connected")
    

def connect(url):
    ws = websocket.WebSocketApp(url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
 
 
connect("ws://192.168.0.101:8080/sensor/connect?type=android.sensor.accelerometer") 

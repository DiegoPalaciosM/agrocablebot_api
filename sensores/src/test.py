import websocket
import json
import numpy as np
import time


from commands import Kalman, kalman, tini, tiniA

def on_message(ws, message):
    global tini
    global count
    values = json.loads(message)['values']
    x = values[0]
    y = values[1]
    z = values[2]
    Am = np.matrix([x,y,z]).getT()

    if kalman.init:
        kalman.x = Am
        kalman.init = False

    a = 0
    A = kalman.x

    v = 0
    V = v + (2 * (time.time() - kalman.tini) * (A - a))
        #print (time.time() - kalman.tini)
        #print ('A: ', A - a)
        #print ('V: ', V - v)

    p = 0
    P = p + ((time.time() - kalman.tini) * (V - v))

    v = V
    a = A

    kalman.V = V
    kalman.P = P

    kalman.update(Am)
    kalman.predict()

    if time.time() - tini > 1:
        print("x = ", x , "y = ", y , "z = ", z )
        print ('A: ', kalman.x[0][0],kalman.x[1][0],kalman.x[2][0])
        print ('V: ', kalman.V[0][0],kalman.V[1][0],kalman.V[2][0])
        print ('P: ', kalman.P[0][0],kalman.P[1][0],kalman.P[2][0])
        print (time.time() - tiniA)
        tini = time.time()
        count += 1
        

def on_error(ws, error):
    print("error occurred ", error)
    
def on_close(ws, close_code, reason):
    print("connection closed : ", reason)
    
def on_open(ws):
    print("connected")
    

def connect(url):
    global tini
    tini = time.time()
    ws = websocket.WebSocketApp(url,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
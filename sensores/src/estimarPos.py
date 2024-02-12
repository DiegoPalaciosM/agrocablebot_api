from commands import logger, Kalman
from threads import mThread

import time
import numpy as np

from sense_hat import SenseHat

sense = SenseHat()

offset = np.matrix(np.zeros(shape=(3,1)))
sumatoria = np.matrix(np.zeros(shape=(3,1)))

init = time.time()
for i in range(101):
    data = sense.get_accelerometer_raw()
    sumatoria += np.matrix([data['x'],data['y'],data['z']]).getT()
offset = sumatoria / 100

kalman = Kalman(3,3)
kalman.h = np.matrix(np.identity(kalman.n_state))
kalman.r *= 0.01

tiniA = time.time()
tini = time.time()
count = 0 
    
def thread_function(args):
    global tini
    kalman = args[0]
    sense = args[2]
    offset = args[3]
    data = sense.get_accelerometer_raw()
    Am = np.matrix([data['x'],data['y'],data['z']]).getT() - offset
    Am = Am * 10

    if kalman.init:
        kalman.x = Am
        kalman.init = False

    kalman.update(Am)
    kalman.predict()

    dt = (time.time() - kalman.tini)

    kalman.Vk = kalman.vk1 + (dt * Am)

    kalman.Pk = kalman.Pk + kalman.Vk * dt + 0.5 * Am * dt**2
    #kalman.Pk = kalman.pk1 + ((time.time() - kalman.tini)**2 * Am * 0.5)

    kalman.tini = time.time()

    kalman.vk1 = kalman.Vk
    kalman.pk1 = kalman.Pk

    if time.time() - tini > 1:
        print ('A: ', Am.getT())
        print ('V: ', kalman.Vk.getT())
        print ('P: ', kalman.Pk.getT())
        print (time.time() - tiniA)
        tini = time.time()
    
def main():
    global tini
    global tiniA
    global kalman
    delay = 0
    kalman_thread = mThread(thread_function, delay, [kalman, delay, sense, offset])
    kalman_thread.status = False
    kalman_thread.start()
    logger.info('ready')
    while True:
        for event in sense.stick.get_events():
            if event.action == 'pressed' and event.direction == 'up':
                logger.info('start')
                kalman_thread.status = True
                time.sleep(0.2)
            elif event.action == 'pressed' and event.direction == 'down':
                logger.info('stop')
                kalman_thread.status = False
                time.sleep(0.2)
            elif event.action == 'pressed' and event.direction == 'middle':
                exit()
        if kalman_thread.status == False:
            kalman.tini = time.time()
            tiniA = kalman.tini

        time.sleep(1)

if __name__ == "__main__":
    main()
    pass
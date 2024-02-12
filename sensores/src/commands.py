import logging
import numpy as np
from threads import mThread
import time

class CustomFormatter(logging.Formatter):
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fmt = '%(asctime)s | %(levelname)8s | %(message)s'
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(CustomFormatter(fmt))

logger.addHandler(stdout_handler)

def offset(value):
    if value >= 0 and value < 180:
        return value * (360 - 180) / 180 + 180
    elif value > 180:
        return (value - 180) * (180 - 0) / (360 - 180) + 0
    #return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class Kalman:
    def __init__(self, n_sensors, n_state):
        self.n_sensors = n_sensors
        self.n_state = n_state
        self.init = True
        self.tini = time.time()
        self.dt = 0

        self.Vk = 0
        self.Pk = 0

        self.vk1 = 0
        self.pk1 = 0
        
        self.x = np.matrix(np.zeros(shape=(self.n_state,1)))                 # Estado de estimacion k-1
        self.p = np.matrix(np.identity(self.n_state))                        # Estado de covarianza k-1
        self.f = np.matrix(np.identity(self.n_state))
        self.u = np.matrix(np.zeros(shape=(self.n_state,1)))                 # Dato de entrada
        self.h = np.matrix(np.zeros(shape=(self.n_sensors, self.n_state)))   # Probabilidad predictiva
        self.r = np.matrix(np.identity(self.n_sensors))                      # Ruido de covarianza de la matriz
        self.i = np.matrix(np.identity(self.n_state))                        # Ganancia de Kalman
        self.b = np.eye(self.x.shape[0])
    
    def predict(self):
        #self.x = np.dot(self.f, self.x) + self.u
        self.x = np.dot(self.f, self.x) + self.u

        self.p = np.dot(self.f, np.dot(self.p, self.f.getT())) + self.u

    def update(self, A):
        S = np.dot(self.h, np.dot(self.p, self.h.getT())) + self.r
        K = np.dot(self.p, np.dot(self.h.getT(), S.getI()))
        self.x = self.x + np.dot(K, (A - np.dot(self.h, self.x)))
        #self.p = self.p - np.dot(K, np.dot(self.h, self.p))
        self.p = self.p - np.dot(K, np.dot(S, K.getT()))

    def updateV(self, A):
        self.Vk = self.vk1 + (self.dt * A)
        self.vk1 = self.Vk
    
    def updateP(self, A):
        self.Pk = self.pk1 + self.Vk * self.dt + 5 * A * self.dt**2
        self.pk1 = self.Pk

class Kalman2:
    def __init__(self, n_sensors, n_states):
        pass
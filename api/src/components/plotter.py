# [missing-module-docstring]
import pandas
import csv
import os
import matplotlib.pyplot as plt
from matplotlib import cm
    
import numpy as np

from commands import getIndex2, getIndex3

df = pandas.read_csv('data/1/csv/giroscopio.csv')

filePrefix = 1
last_position = {'x' : -400, 'y' : 100, 'z': 0}

for i in range(400, -450, -50):
    for j in range (-400, 450, 100):
        
        #getIndex2({'x' : j, 'y' : i, 'z': 0})
        getIndex3([j, i])

def csv_writter(sensor: str = 'nosensor', sensorData: dict = {}):
    print (sensor)
    os.makedirs(f'data/{filePrefix}/csv/', exist_ok=True)
    file_name = f'data/{filePrefix}/csv/{sensor}.csv'
    sensorData['id'] = getIndex2(last_position)
    sensorData['x_pos'] = last_position['x']
    sensorData['y_pos'] = last_position['y']
    sensorData['z_pos'] = last_position['z']
    if os.path.exists(file_name):
        with open(file_name, mode='a') as file:
            writter = csv.writer(
                file)
            writter.writerow(list(sensorData.values()))
            file.close()
    else:
        with open(file_name, mode='x') as file:
            writter = csv.DictWriter(file, fieldnames=list(sensorData.keys()))
            writter.writeheader()
            writter.writerow(sensorData)
            file.close()

headers = df.columns.tolist()
headers.remove('id')
headers.remove('x_pos')
headers.remove('y_pos')
headers.remove('z_pos')

data = []

for i in df.index:
    pos = {'x' : df['x_pos'][i], 'y' : df['y_pos'][i], 'z' : df['z_pos'][i]}
    dataA = {}
    for header in headers:
        dataA[header] = df[header][i]
    data.append({'id' : i, 'pos' : pos, 'data' : dataA})


fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

X = []
Y = []
Z = []

for item in data:
    X.append((item['pos']['x']))
    Y.append((item['pos']['y']))
    Z.append(item['data']['roll'])

ax.plot_trisurf(X, Y, Z, color='white', edgecolors='grey', alpha=0.5)

#plt.show()
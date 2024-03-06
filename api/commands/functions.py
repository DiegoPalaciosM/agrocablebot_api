import os
import inspect
import sys
import csv

from agrocablebot.commands import logger

def offset(value):
    """
    Esta función toma un valor y devuelve un valor de desplazamiento basado en las siguientes condiciones:

    Si el valor está entre 0 y 180, se escalará a un valor entre 180 y 360.
    Si el valor es mayor que 180, se escalará a un valor entre 0 y 180.

    Parámetros
    ----------
    valor : float
        El valor a desplazar.

    Devuelve
    -------
    float
        El valor compensado.

    """
    if value >= 0 and value < 180:
        return value * (360 - 180) / 180 + 180
    elif value > 180:
        return (value - 180) * (180 - 0) / (360 - 180) + 0

def getIndex(pos):
    """
    Calcula un índice a partir de una posición dada.

    Esta función toma una posición representada como un diccionario con las claves 'x' y 'y'.
    Luego, normaliza las coordenadas dividiéndolas por 100 y aplica una serie de cálculos
    para calcular un índice basado en la posición. El cálculo del índice se realiza de la siguiente manera:

    - La coordenada x se redondea hacia abajo y se le suma 4, luego se agrega el aporte x multiplicado por el decimal restante de la coordenada x.
    - La coordenada y se redondea hacia abajo, se le suma 4 y se multiplica por 9. Luego se resta el aporte y multiplicado por el decimal restante de la coordenada y.

    Parámetros:
    pos (dict): Un diccionario que representa la posición con las claves 'x' y 'y'.

    Returns:
    float: El índice calculado basado en la posición dada.

    Ejemplos:
    >>> getIndex({'x': 150, 'y': 250})
    62.5
    >>> getIndex({'x': 300, 'y': 500})
    62.5
    """
    aportex = 0.1
    aportey = 1

    posA = pos
    
    posA['x'] = posA['x']/100 
    posA['y'] = posA['y']/100

    x = (posA['x'] - posA['x']%1 + 4) + (posA['x']%1 * aportex)
    y = ((-posA['y'] + posA['y']%1 + 4) * 9) - ((posA['y']%1 * aportey))
    #(f"X({pos[0]} Y({pos[1]}))",x+y)
    return x+y

def csvWritter(filename, nprueba, models):
    """
    Escribe los datos de los modelos filtrados por 'prueba' en archivos CSV.

    Esta función toma un nombre de archivo, un número de prueba y un módulo que contiene modelos de Django.
    Itera sobre los modelos en el módulo dado y, si un modelo tiene un campo llamado 'prueba', recupera los registros
    que coinciden con el número de prueba especificado. Luego, escribe los datos de estos registros en un archivo CSV
    en un directorio con el nombre del archivo especificado.

    Parámetros:
    filename (str): El nombre del archivo para el directorio donde se guardarán los archivos CSV.
    nprueba (int): El número de prueba utilizado para filtrar los registros de los modelos.
    models (module): El módulo que contiene los modelos de Django.

    Returns:
    None

    Ejemplo:
    csvWritter("output", 1, models)
    """
    os.makedirs(f'{filename}', exist_ok=True)
    for name, obj in inspect.getmembers(sys.modules[models.__name__]):
        if inspect.isclass(obj):
            try:
                if hasattr(obj, 'prueba'):
                    registros = obj.objects.filter(prueba = nprueba).values_list()
                    keys = [field.name for field in obj._meta.fields][1:-2]
                    with open(f'{filename}/{obj.name}.csv', 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(keys)
                        writer.writerows([registro[1:-2] for registro in registros])
            except Exception as error:
                logger.error(f"{type(error)} {error}")
    pass
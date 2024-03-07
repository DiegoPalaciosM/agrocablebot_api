import os
import subprocess

from agrocablebot.commands import logger
from api.models import Configuracion

def deviceInfo(*args, **kwargs):
    """
    Recupera información del dispositivo, incluyendo el SSID de la red inalámbrica y el nombre de la configuración.

    Esta función utiliza el comando de sistema 'iwgetid' para obtener el SSID de la red inalámbrica a la que está conectado el dispositivo.
    Si se produce algún error al recuperar el SSID, se establece como 'error' y se registra en el registro de errores.
    Además, obtiene el nombre de la configuración utilizando el modelo `Configuracion` de la aplicación `miapp`.

    Parámetros:
    *args: Argumentos posicionales adicionales (no utilizados en esta función).
    **kwargs: Argumentos de palabra clave adicionales (no utilizados en esta función).

    Returns:
    dict: Un diccionario que contiene el SSID de la red inalámbrica y el nombre de la configuración.

    Ejemplo:
    >>> device_info = deviceInfo()
    >>> print(device_info)
    {'ssid': 'MiSSID', 'name': 'NombreDeConfiguracion'}
    """
    try:
        ssid = subprocess.check_output(['iwgetid']).decode('utf-8').split('"')[1]
    except Exception as error:
        ssid = 'error'
        logger.error(f"{type(error)} {error}")
    return {'ssid' : ssid, 'name' : Configuracion.objects.get(name = 'nombreDispositivo').data}

def cameraInfo2():
    ids = {'above' : 0, 'below' : 1}
    resolutions = {'above' : [], 'below' : []}
    res = subprocess.run(['v4l2-ctl','--list-devices'], stdout=subprocess.PIPE)
    resDecoded = res.stdout.decode().split('\n')
    for i in range(len(resDecoded)):
        if os.environ['ABOVE_CAMERA'] in resDecoded[i]:
            ids['above'] = int(resDecoded[i+1].strip('\t/dev/video'))
            temp = subprocess.Popen(['v4l2-ctl', '-d', f'{ids["above"]}', '--list-formats-ext'], stdout=subprocess.PIPE)
            temp2 = subprocess.check_output(('grep', 'x'), stdin=temp.stdout)
            resolutions['above'] = temp2.decode('utf-8').split('\n')[0].split('\t')[2].split(' ')[-1].split('x')
        elif os.environ['BELOW_CAMERA'] in resDecoded[i]:
            ids['below'] = int(resDecoded[i+1].strip('\t/dev/video'))
            temp = subprocess.Popen(['v4l2-ctl', '-d', f'{ids["below"]}', '--list-formats-ext'], stdout=subprocess.PIPE)
            temp2 = subprocess.check_output(('grep', 'x'), stdin=temp.stdout)
            resolutions['below'] = temp2.decode('utf-8').split('\n')[0].split('\t')[2].split(' ')[-1].split('x')
    return ids, resolutions

def cameraInfo(camera = None):
    """
    Recupera información sobre una cámara de video.

    Esta función toma el nombre de la cámara como argumento opcional. Si no se proporciona el nombre de la cámara,
    la función no hace nada y devuelve None. Si se proporciona el nombre de la cámara, la función busca el dispositivo
    correspondiente en la lista de dispositivos de video utilizando el comando 'v4l2-ctl --list-devices'. Luego, busca
    la resolución de video admitida para ese dispositivo utilizando el comando 'v4l2-ctl -d <id> --list-formats-ext',
    donde <id> es el ID del dispositivo encontrado. La función devuelve el ID del dispositivo y su resolución.

    Parámetros:
    camera (str, opcional): El nombre de la cámara (definido en la variable de entorno) para buscar en la lista de dispositivos.

    Returns:
    tuple: Una tupla que contiene el ID del dispositivo de video y su resolución, o None si no se proporciona el nombre de la cámara.

    Ejemplo:
    >>> camera_id, camera_resolution = cameraInfo('MY_CAMERA')
    >>> print(camera_id, camera_resolution)
    1, [1280, 720]
    """
    if not camera:
        return
    else:
        id = 0
        resolution = [0,0]
        res = subprocess.run(['v4l2-ctl','--list-devices'], stdout=subprocess.PIPE)
        resDecoded = res.stdout.decode().split('\n')
        for i in range(len(resDecoded)):
            if os.environ[camera] in resDecoded[i]:
                id = int(resDecoded[i+1].strip('\t/dev/video'))
                temp = subprocess.Popen(['v4l2-ctl', '-d', f'{id}', '--list-formats-ext'], stdout=subprocess.PIPE)
                temp2 = subprocess.check_output(('grep', 'x'), stdin=temp.stdout)
                resolution = temp2.decode('utf-8').split('\n')[0].split('\t')[2].split(' ')[-1].split('x')
        return id, resolution

import os
import cv2
import imageio
from greenlet import getcurrent
import threading
import time

from api.commands.functions import getIndex
from api.commands.information import cameraInfo
from agrocablebot.settings import DATA_PATH
from agrocablebot.commands import singleton, logger

class CameraEvent(object):
    """
    Una clase que implementa una primitiva de sincronización para eventos entre hilos.
    """
    def __init__(self):
        """
        Inicializa una nueva instancia de la clase CameraEvent.
        """
        self.events = {}

    def wait(self):
        """
        Espera a que ocurra un evento.

        Devuelve:
            Un bool que indica si el evento ocurrió.
        """
        ident = getcurrent()
        if ident not in self.events:
            self.events[ident] = [threading.Event(), time.time()]
        return self.events[ident][0].wait()

    def set(self):
        """
        Establece el evento.
        """
        now = time.time()
        remove = None
        for ident, event in self.events.items():

            if not event[0].isSet():
                event[0].set()
                event[1] = now
            else:
                if now - event[1] > 5:
                    remove = ident
        if remove:
            del self.events[remove]

    def clear(self):
        """
        Borra el evento.
        """
        self.events[getcurrent()][0].clear()

class Camera:
    """
    Una clase que representa una cámara.
    """
    def __init__(self, cname):
        """
        Inicializa una nueva instancia de la clase Camera.

        Args:
            cname (str): El nombre de la cámara.
        """
        self.cname = cname
        self.frame = None
        self.frameData = None
        self.last_access = 0
        self.event = CameraEvent()
        self.thread = None
        
    def create_thread(self):
        """
        Crear un hilo para leer fotogramas de la cámara.
        """
        if self.thread is None:
            self.source, self.resolution = cameraInfo(self.cname)
            self.camera = cv2.VideoCapture(self.source)
            #self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, int(self.resolution[0]))
            #self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, int(self.resolution[1]))
            self.camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.last_access = time.time()

            self.thread = threading.Thread(target=self.thread_function) # type: ignore
            self.thread.start()

            self.event.wait()
        
    def thread_function(self):
        """
        La función que se ejecuta en el hilo para leer fotogramas de la cámara.
        """
        for_frames = self.frames()
        for frame in for_frames:
            self.frame = frame
            self.event.set()
            if time.time() - self.last_access > 1:
                for_frames.close()
                self.camera.release()
                break
        self.thread = None

    def frames(self):
        """
        Un generador que produce fotogramas de la cámara.
        """
        while True:
            success, img = self.camera.read()
            if not success:
                break
            ret, buffer = cv2.imencode('.jpg', img) 
            self.frameData = img
            time.sleep(0.033)
            yield buffer.tobytes()
    
    def get_frame(self):
        """
        Obtiene el último fotograma de la cámara.

        Devuelve:
            El último fotograma de la cámara.
        """
        self.last_access = time.time()

        self.event.wait()
        self.event.clear()
        return self.frame

    def save_frame(self, pos, prueba, path=DATA_PATH):
        """
        Guarda un fotograma de la cámara.

        Args:
            pos (dict): La posición de la cámara.
            prueba (str): El nombre de la prueba.
            path (str, opcional): La ruta en la que guardar el fotograma. Por defecto es DATA_PATH.
        """
        os.makedirs(f"{path}/{prueba}/fotos/{self.cname}/", exist_ok=True)
        self.create_thread()
        cv2.imwrite(f"{path}/{prueba}/fotos/{self.cname}/{getIndex(pos)}_{pos}.png", self.frameData)


@singleton
class AboveCamera(Camera):
    """
    Clase que representa la cámara de arriba.
    """
    def __init__(self):
        """
        Inicializa una nueva instancia de la clase AboveCamera.
        """
        Camera.__init__(self, 'ABOVE_CAMERA')

@singleton
class BelowCamera(Camera):
    """
    Clase que representa la cámara inferior.
    """
    def __init__(self):
        """
        Inicializa una nueva instancia de la clase BelowCamera.
        """
        Camera.__init__(self, 'BELOW_CAMERA')

def gen_frame(camera):
    """
    Genera un fotograma desde la cámara especificada.

    Args:
        camera (Cámara): La cámara desde la que generar el fotograma.

    Produce:
        Un fotograma de la cámara especificada.
    """
    camera.create_thread()
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
def gen_screenshot(self, camera):
    """
    Genera una captura de pantalla desde la cámara especificada.

    Args:
        camera (Cámara, opcional): La cámara desde la que generar la captura de pantalla. Por defecto es None.

    Devuelve:
        La captura de pantalla de la cámara especificada.
    """
    if camera:
        camera.create_thread()
        screenshot = camera.get_frame()
        return screenshot
    return ''


def exportGif(prueba):
    """
    Exporta un gif de la prueba especificada.

    Args:
        prueba (str): El nombre de la prueba.
    """
    try:
        cameras = ['superior', 'inferior']
        for camera in cameras:
            path = f'{DATA_PATH}/{prueba}/fotos/{camera}'
            names = os.listdir(path)
            names.sort()
            images = []
            for n in names:
                images.append(imageio.imread(f'{path}/{n}'))
                imageio.imread(f'{path}/{n}')
            imageio.mimsave(f'{path}.gif', images)
    except Exception as error:
        logger.error(f"{type(error)} error")

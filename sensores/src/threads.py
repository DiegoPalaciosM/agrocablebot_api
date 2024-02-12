from threading import Thread
from time import sleep


class mThread(Thread):
    def __init__(self, funcion, delay, args):
        Thread.__init__(self, daemon=True)
        self.funcion = funcion
        self.delay = delay
        self.status = True
        self.args = args

    def run(self):
        while True:
            while self.status:
                self.funcion(self.args)
                sleep(self.delay)

    def pause(self):
        self.status = False

    def resume(self):
        self.status = True

    def toggle(self):
        self.status = not self.status

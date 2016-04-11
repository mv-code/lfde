import time
from threading import Thread

class Pulser(Thread):
    """A bit dodgy, but should be ok to sweep the progress bar"""
    def __init__(self, callback, done_callback):
        Thread.__init__(self)

        self.interval = 0.1
        self.callback = callback
        self.done_callback = done_callback
        self.stopping = False

    def run(self):
        while self.stopping == False:
            self.callback()
            time.sleep(self.interval)

        self.done_callback()

    def stop(self):
        self.stopping = True


import zmq
import numpy as np
from threading import Thread
from time import sleep
import pmt
import time


class SpectrumThread(Thread):
    def __init__(
        self, group=None, target=None, name=None, history_length=1000, port=5560
    ):
        super().__init__(group=group, target=target, name=name, daemon=True)
        self.history_length = history_length
        self.spectrum = None
        self.history = []
        self.port = port

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://localhost:%s" % self.port)
        socket.subscribe("")
        while True:
            rec = socket.recv()
            var = np.frombuffer(rec, dtype="float32")
            if len(self.history) >= self.history_length:
                self.history.pop()
            self.history.insert(0, (time.time(), var))
            self.spectrum = var

    def get_spectrum(self):
        return self.spectrum

    def get_power_history(self, tsys, tcal, calpwr):
        spectrum_history = self.history.copy()
        power_history = []
        for t, spectrum in spectrum_history:
            p = np.sum(spectrum)
            a = len(spectrum)
            pwr = (tsys + tcal) * p / (a * calpwr)
            power_history.insert(0, (t, pwr))
        return power_history

    def get_history(self):
        return self.history.copy()


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    thread = SpectrumThread()
    thread.start()
    sleep(1)
    print(thread.get_spectrum())
    data = thread.get_spectrum()
    plt.hist(range(len(data)), range(len(data)), weights=data)
    plt.xlabel("Frequency")
    plt.ylabel("Power")
    plt.show()
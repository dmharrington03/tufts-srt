import zmq
import numpy as np
from threading import Thread
import json


class StatusThread(Thread):
    def __init__(self, group=None, target=None, name=None, port=5554):
        super().__init__(group=group, target=target, name=name, daemon=True)
        self.status = {}
        self.port = port

    def run(self):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://localhost:%s" % self.port)
        socket.subscribe("")
        while True:
            rec = socket.recv()
            dump = json.loads(rec)
            self.status.update(dump)

    def get_status(self):
        return self.status


if __name__ == '__main__':
    thread = StatusThread()
    thread.start()
    thread.join()
#!/usr/bin/env python3

import time
import zmq
import logging
import os
import gc
import atexit
from functools import wraps
import sys

logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")


def gc_decorator(critical_func):
    @wraps(critical_func)
    def wrapper(*args, **kwargs):
        gc.disable()
        # gc.disable() doesn't work, because some random 3rd-party library will
        gc.set_threshold(0)
        # Suicide immediately after other atexit functions finishes.
        # CPython will do a bunch of cleanups in Py_Finalize which
        # will again cause Copy-on-Write, including a final GC
        atexit.register(os._exit, 0)
        return critical_func(*args, **kwargs)


# @gc_decorator
def run(l_nb_nodes):
    logging.info("Dealer Node Started")
    gc.disable()
    gc.set_threshold(0)
    gc.set_threshold(0)
    atexit.register(os._exit, 0)

    context = zmq.Context()
    sockets = []
    cmpt = 0
    while cmpt < l_nb_nodes:
        port_number = 30000 + cmpt + 1
        topic = "tcp://127.0.0.1:%d" % port_number
        socket = context.socket(zmq.DEALER)
        socket.setsockopt(zmq.LINGER, 0)
        socket.setsockopt(zmq.SNDTIMEO, 0)
        socket.connect(topic)
        sockets.append(socket)
        cmpt +=1
    iterator = 0
    try:
        while True:
            for socket in sockets:
                time_nanosec = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                socket.send(b"%d,%d" % (iterator, time_nanosec))
                # logging.info("Message %d sent at %d " % (iterator, time_nanosec))
                time.sleep(0.01)
            iterator += 1
    except KeyboardInterrupt:
        for socket in sockets:
            socket.close()
        logging.info("Terminating Dealer Node")


# Main function
if __name__ == '__main__':
    nb_nodes = sys.argv[1]
    run(int(nb_nodes))

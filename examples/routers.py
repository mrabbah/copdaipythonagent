#!/usr/bin/env python3

import time
import zmq
import logging
import os
import sys
import gc
import atexit
from functools import wraps

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

    return wrapper


# @gc_decorator
def run(l_node_name):
    logging.info("Lunching node: %s" % l_node_name)
    root_folder = "/tmp/"
    proto = "ipc://"
    topic_folder = "cdp"
    topic = "%s%s%s/%s" % (proto, root_folder, topic_folder, args[0])
    # mkdir_topic_folder
    path = os.path.join(root_folder, topic_folder)
    if not os.path.exists(path):
        logging.info("Creating topic folder : %s " % path)
        os.makedirs(path)
    tracing_topic = "%s%s%s/%s" % (proto, root_folder, topic_folder, "trace")
    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)
    socket.setsockopt(zmq.ROUTER_HANDOVER, 1)
    socket.bind(topic)
    # Initialize poll set
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    tracing_socket = context.socket(zmq.DEALER)
    tracing_socket.connect(tracing_topic)
    try:
        while True:
            socks = dict(poller.poll())
            message = socket.recv_multipart()
            time_nanosec = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
            trace_msg = "%s,%s,%d\n" % (l_node_name, message[1].decode('utf-8'), time_nanosec)
            tracing_socket.send_string(trace_msg)
            # logging.info("Receive message: %s at %d" % (message, time_nanosec))
    except KeyboardInterrupt:
        tracing_socket.close()
        socket.close()
        logging.info("Terminating Node %s" % l_node_name)


# Main function
if __name__ == '__main__':
    args = sys.argv[1:]
    node_name = args[0]
    run(node_name)

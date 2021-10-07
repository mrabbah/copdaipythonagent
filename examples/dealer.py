import time
import zmq
import logging
import os
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


def run():
    logging.info("Dealer Node Started")
    root_folder = "/tmp/"
    proto = "ipc://"
    topic_folder = "cdp"
    path = os.path.join(root_folder, topic_folder)
    topics_path = os.listdir(path)
    logging.info("Topics list : %s " % topics_path)
    topics = []
    context = zmq.Context()
    sockets = []
    for topic_path in topics_path:
        if topic_path == "trace" or topic_path == "trace.csv":
            continue
        topic = "%s%s%s/%s" % (proto, root_folder, topic_folder, topic_path)
        topics.append(topic)
        socket = context.socket(zmq.DEALER)
        socket.setsockopt(zmq.LINGER, 0)
        socket.setsockopt(zmq.SNDTIMEO, 0)
        socket.connect(topic)
        sockets.append(socket)
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
    run()

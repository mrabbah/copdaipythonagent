import time
import zmq
import logging
import os

# Main function
if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
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
        socket.connect(topic)
        sockets.append(socket)

    iterator = 0
    try:
        while True:
            for socket in sockets:
                time_nanosec = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
                # msg = "%d,%d" % (iterator, time_nanosec)
                # b_msg = str.encode(msg)
                socket.send(b"%d,%d" % (iterator, time_nanosec))
                # socket.send_string(f"{iterator},{time_nanosec}")
                # socket.send(b"MSG_%d" % iterator)
                # socket.send(b_msg)
                # socket.send(b"Message %d " % iterator)
                logging.info("Message %d sent at %d " % (iterator, time_nanosec))
            iterator += 1
    except KeyboardInterrupt:
        for socket in sockets:
            socket.close()
        logging.info("Terminating Dealer Node")

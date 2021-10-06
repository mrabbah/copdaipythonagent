import time
import zmq
import logging
import os
import sys

# Main function
if __name__ == '__main__':
    args = sys.argv[1:]
    logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")
    node_name = args[0]
    logging.info("Lunching node: %s" % node_name)

    root_folder = "/tmp/"
    proto = "ipc://"
    topic_folder = "cdp"
    topic = "%s%s%s/%s" % (proto, root_folder, topic_folder, args[0])

    # mkdir_topic_folder
    path = os.path.join(root_folder, topic_folder)
    if not os.path.exists(path):
        logging.info("Creating topic folder : %s " % path)
        os.makedirs(path)

    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)
    socket.bind(topic)
    # Initialize poll set
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    tracing_topic = "%s%s%s/%s" % (proto, root_folder, topic_folder, "trace")
    tracing_socket = context.socket(zmq.DEALER)
    tracing_socket.connect(tracing_topic)

    try:
        while True:
            socks = dict(poller.poll())
            message = socket.recv_multipart()
            time_nanosec = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
            trace_msg = "%s,%s,%d\n" % (node_name, message[1].decode('utf-8'), time_nanosec)
            tracing_socket.send_string(trace_msg)
            # logging.info("trace: %s of type %s" % (trace_msg, type(trace_msg)))
            # logging.info("Receive message: %s at %d" % (message, time_nanosec))
    except KeyboardInterrupt:
        tracing_socket.close()
        socket.close()
        logging.info("Terminating Node %s" % node_name)

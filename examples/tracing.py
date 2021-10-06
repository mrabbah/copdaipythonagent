import zmq
import logging
import os
import sys

# Main function
if __name__ == '__main__':
    args = sys.argv[1:]
    logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")

    logging.info("Lunching Tracing node")

    root_folder = "/tmp/"
    proto = "ipc://"
    topic_folder = "cdp"
    topic = "%s%s%s/%s" % (proto, root_folder, topic_folder, "trace")
    logfile_path = "%s%s/%s" % (root_folder, topic_folder, "trace.csv")
    logfile = open(logfile_path, 'w+')

    # mkdir_topic_folder
    path = os.path.join(root_folder, topic_folder)
    if not os.path.exists(path):
        logging.info("Creating tracing topic folder : %s " % path)
        os.makedirs(path)

    context = zmq.Context()
    socket = context.socket(zmq.ROUTER)
    socket.bind(topic)
    # Initialize poll set
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    try:
        while True:
            socks = dict(poller.poll())
            message = socket.recv_multipart()
            logging.info("receiving message %s ..." % message[1].decode('utf-8'))
            logfile.write("%s" % message[1].decode('utf-8'))
    except KeyboardInterrupt:
        logfile.close()
        socket.close()
        logging.info("Terminating Tracing Node " )


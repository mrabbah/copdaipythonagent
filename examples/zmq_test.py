import time
import zmq
import threading
import logging
import os

root_folder = "/tmp/"
proto = "ipc://"
dealer_folder = "dealer"
router_folder = "router"
topic_folder = "cdp"
shutdown_topic_folder = "shutdown_topic"
topic = "%s%s%s/%s" % (proto, root_folder, topic_folder, 0)
# shutdown_topic = "inproc://shutdown_topic"
shutdown_topic = "%s%s%s/%s" % (proto, root_folder, shutdown_topic_folder, 0)


def server():
    logging.info("Thread server: starting")
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(topic)
    subscriber = context.socket(zmq.PULL)
    subscriber.connect(shutdown_topic)
    # close immediately on shutdown
    # backend.setsockopt(zmq.LINGER, 0)

    # Initialize poll set
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    poller.register(subscriber, zmq.POLLIN)

    while True:
        try:
            socks = dict(poller.poll())
            print(socks)
        except KeyboardInterrupt:
            logging.info("Server will finish bye")

        if socket in socks:
            message = socket.recv()
            logging.info("Receive message: %s" % message)
            socket.send(b"World")

        if subscriber in socks:
            string = subscriber.recv_string()
            logging.info("You ask me %s! server to finish bye" % string)
            break

    subscriber.close()
    socket.close()


def client(nb_messages):
    logging.info("Thread client: starting")
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    logging.info("Client Connecting to hello world server...")
    socket.connect(topic)
    publisher = context.socket(zmq.PUSH)
    publisher.bind(shutdown_topic)
    logging.info("Client bind to shutdown topic")

    for request in range(nb_messages):
        logging.info("Sending request %s ..." % request)
        socket.send(b"Hello")
        # message = socket.recv()
        # logging.info("Received reply %s [ %s ]" % (request, message))
        time.sleep(0.01)

    logging.info("Sending shutdown request to server")
    # publisher.send_multipart([b"SHUTDOWN_TOPIC", b"Can you shutdown nicely?"])
    publisher.send_string("Rest in peace")
    time.sleep(1)
    publisher.close()


def mkdir_topic_folder():
    logging.info("Checking if topic folder exist...")
    path = os.path.join(root_folder, topic_folder)
    if not os.path.exists(path):
        logging.info("Creating topic folder : %s " % path)
        os.makedirs(path)
    path = os.path.join(root_folder, shutdown_topic_folder)
    if not os.path.exists(path):
        logging.info("Creating shutdown topic folder : %s " % path)
        os.makedirs(path)


def retrieve_topics():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(shutdown_topic)

    logging.info("Retrieving topics...")
    path = os.path.join(root_folder, topic_folder)
    while True:
        if not os.path.exists(path):
            time.sleep(1)
            continue
        topics = os.listdir(path)
        logging.info("Topics list : %s " % topics)
        time.sleep(1)
        message = socket.recv()
        if message == b"done":
            break


# Main function
if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S.%f")
    logging.info("Main    : COPDAI AGENT TEST MODULE")
    mkdir_topic_folder()
    t_server = threading.Thread(target=server, args=(), daemon=True)
    t_client = threading.Thread(target=client, args=(5,), daemon=True)
    t_server.start()
    t_client.start()
    t_server.join()
    t_client.join()
    print('Finished')

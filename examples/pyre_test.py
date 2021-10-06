import pyre

def lunch():
    #  Constructor, creates a new Zyre node. Note that until you start the
    #  node it is silent and invisible to other nodes on the network.
    node = pyre.Pyre()
    #  Set node header; these are provided to other nodes during discovery
    #  and come in each ENTER message.
    node.set_header("info", "My sweet info")
    #  (TODO: Currently a Pyre node starts immediately) Start node, after setting header values. When you start a node it
    #  begins discovery and connection.
    node.start()

    #  Stop node, this signals to other peers that this node will go away.
    #  This is polite; however you can also just destroy the node without
    #  stopping it.
    node.stop()

    #  Join a named group; after joining a group you can send messages to
    #  the group and all Zyre nodes in that group will receive them.
    node.join("GROUP1")

    #  Leave a group
    node.leave("GROUP1")

    #  Receive next message from network; the message may be a control
    #  message (ENTER, EXIT, JOIN, LEAVE) or data (WHISPER, SHOUT).
    #  Returns a list of message frames
    msgs = node.recv();

    # Send message to single peer, specified as a UUID object (import uuid)
    # Destroys message after sending
    # node.whisper(peer, msg)

    # Send message to a named group
    # Destroys message after sending
    # node.shout(group, msg);

    #  Send string to single peer specified as a UUID string.
    #  String is formatted using printf specifiers.
    # node.whispers(peer, msg_string)

    #  Send message to a named group
    #  Destroys message after sending
    # node.shouts(group, msg_string);

    #  Return handle to the Zyre node, for polling
    # node.get_socket()
    # use node.get_socket().getsockopt(zmq.FD) to acquire
    # the filedescriptor
    # Don't use this for getting Pyre events you can use the
    # node.inbox to get those events


# Main function
if __name__ == '__main__':
    lunch()
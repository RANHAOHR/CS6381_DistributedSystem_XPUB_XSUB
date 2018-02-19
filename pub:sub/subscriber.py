# Sample code for CS6381
# Vanderbilt University
# Instructor: Aniruddha Gokhale
#
# Code taken from ZeroMQ examples with additional
# comments or extra statements added to make the code
# more self-explanatory  or tweak it for our purposes
#
# We are executing these samples on a Mininet-emulated environment
#
#


#
#   Weather update client
#   Connects SUB socket to tcp://localhost:5556
#   Collects weather updates and finds avg temp in zipcode
#

import sys
import zmq
import time


def client_task(ident):
    """Basic request-reply client using REQ socket."""
    socket = zmq.Context().socket(zmq.REQ)
    socket.identity = u"Client-{}".format(ident).encode("ascii")
    socket.connect("ipc://frontend.ipc")

    # Send request, get reply
    socket.send(b"HELLO")
    reply = socket.recv()
    print("{}: {}".format(socket.identity.decode("ascii"),
                          reply.decode("ascii")))
                          
def subscriber(port):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    # Here we assume publisher runs locally unless we
    # send a command line arg like 10.0.0.1
    srv_addr = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    connect_str = "tcp://" + srv_addr + ":" + port

    print("Collecting updates from weather server...")
    socket.connect(connect_str)
    # Subscribe to zipcode, default is NYC, 10001
    zip_filter = sys.argv[2] if len(sys.argv) > 2 else "10001"
    # Python2 - ascii bytes to unicode str
    if isinstance(zip_filter, bytes):
        zip_filter = zip_filter.decode('ascii')
    # any subscriber must use the SUBSCRIBE to set a subscription, i.e., tell the
    # system what it is interested in
    socket.setsockopt_string(zmq.SUBSCRIBE, zip_filter)

    return socket

def broker(port_push,port_sub):
    context = zmq.Context()
    socket_pull = context.socket(zmq.PULL)
    socket_pull.connect ("tcp://localhost:%s" % port_push)
    print "Connected to server with port %s" % port_push
    socket_sub = subscriber(port_sub)
    # socket_sub = context.socket(zmq.SUB)
    # socket_sub.connect ("tcp://localhost:%s" % port_sub)
    # socket_sub.setsockopt(zmq.SUBSCRIBE, "9")
    # print "Connected to publisher with port %s" % port_sub
    ## Initialize poll set
    poller = zmq.Poller()
    poller.register(socket_pull, zmq.POLLIN)
    poller.register(socket_sub, zmq.POLLIN)
    # Work on requests from both server and publisher
    should_continue = True
    while should_continue:
        socks = dict(poller.poll())
        if socket_pull in socks and socks[socket_pull] == zmq.POLLIN:
            message = socket_pull.recv()
            print "Recieved control command: %s" % message
            if message == "Exit":
                print "Recieved exit command, client will stop recieving messages"
                should_continue = False

        if socket_sub in socks and socks[socket_sub] == zmq.POLLIN:
            messageHandler(socket_sub)
            # string = socket_sub.recv()
            # topic, messagedata = string.split()
            # print "Processing ... ", topic, messagedata

def messageHandler(socket):
    # Process 5 updates
    total_temp = 0
    for update_nbr in range(5):
        string = socket.recv_string()
        zipcode, temperature, relhumidity = string.split()
        total_temp += int(temperature)

    print("Average temperature for zipcode '%s' was %dF" % (
          zip_filter, total_temp / (update_nbr+1))
    )


def main():
    server_sub_port = sys.argv[1]
    server_pub_port = sys.argv[2]
    Process(target=broker, args=(server_sub_port,server_pub_port,)).start()

if __name__ == "__main__":
    main()

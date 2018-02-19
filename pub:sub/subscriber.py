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

import zmq
import sys
from random import randrange
import time
from multiprocessing import Process


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

    total_temp = 0
    for update_nbr in range(5):
        string = socket.recv_string()
        zipcode, temperature, relhumidity = string.split()
        total_temp += int(temperature)

    print("Average temperature for zipcode '%s' was %dF" % (
          zip_filter, total_temp / (update_nbr+1))
    )

def main():
    # server_sub_port = sys.argv[1]
    # server_pub_port = sys.argv[2]

    server_sub_port = "5556"
    server_pub_port = "5557"
    Process(target=client_task, args=(server_pub_port,)).start()
    Process(target=subscriber, args=(server_sub_port,)).start()

if __name__ == "__main__":
    main()

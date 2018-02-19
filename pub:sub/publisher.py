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
#   Weather update server
#   Binds PUB socket to tcp://*:5556
#   Publishes random weather updates
#

import zmq
import sys
from random import randrange
import time
from multiprocessing import Process

print("Current libzmq version is %s" % zmq.zmq_version())
print("Current  pyzmq version is %s" % zmq.__version__)

topic = "1001"
ownership_strength = 0
history = 0

def worker_task(port):
    """Worker task, using a REQ socket to do load-balancing."""
    socket = zmq.Context().socket(zmq.REQ)
    socket.identity = u"Worker-{}".format(port).encode("ascii")
    socket.connect("ipc://backend.ipc")

    # Tell broker we're ready for work
    socket.send(b"READY")

    while True:
        address, empty, request = socket.recv_multipart()
        print("{}: {}".format(socket.identity.decode("ascii"),
                              request.decode("ascii")))
        socket.send_multipart([address, b"", b"OK"])
        socket.send_multipart([topic, ownership_strength, history])

def server_pub(port):
    context = zmq.Context()
    # The difference here is that this is a publisher and its aim in life is
    # to just publish some value. The binding is as before.
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)
    # keep publishing
    while True:
        zipcode = randrange(1, 100000)
        temperature = randrange(-80, 135)
        relhumidity = randrange(10, 60)

        socket.send_string("%i %i %i" % (zipcode, temperature, relhumidity))
        time.sleep(1)

def main():
    pub_port = "5556"
    push_port = "5557"
    if len(sys.argv) > 1:
        pub_port =  sys.argv[1]
        int(pub_port)

    if len(sys.argv) > 2:
        push_port =  sys.argv[2]
        int(push_port)

    if len(sys.argv) > 3:
        ownership_strength =  sys.argv[3]
        int(ownership_strength)

    if len(sys.argv) > 4:
        history =  sys.argv[4]
        int(history)

    Process(target=worker_task, args=(push_port,)).start()
    Process(target=server_pub, args=(pub_port,)).start()

if __name__ == "__main__":
    main()

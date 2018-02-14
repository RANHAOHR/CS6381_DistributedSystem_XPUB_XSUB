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
from random import randrange
import time

print("Current libzmq version is %s" % zmq.zmq_version())
print("Current  pyzmq version is %s" % zmq.__version__)

SIGNAL = False
topic = "1001"
ownership_strength = 0
history = 0
#write this as an client, the broker as a server
def register_pub(topic, ownership_strength, history):
    context = zmq.Context()
    s = context.socket(zmq.REP)
    s.bind("tcp://*:5550")

    #  Wait for next request from client
    SIGNAL = s.recv()
    print ("Received request: ", SIGNAL)
    time.sleep (0.5)
    s.send_multipart([topic, ownership_strength, history])

def main():
    context = zmq.Context()
    # The difference here is that this is a publisher and its aim in life is
    # to just publish some value. The binding is as before.
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5556")

    register_pub(topic, ownership_strength, history) #register first and wait the SIGNAL

    # keep publishing
    while SIGNAL:
        zipcode = randrange(1, 100000)
        temperature = randrange(-80, 135)
        relhumidity = randrange(10, 60)

        socket.send_string("%i %i %i" % (zipcode, temperature, relhumidity))
        time.sleep(1)

if __name__ == "__main__":
    main()

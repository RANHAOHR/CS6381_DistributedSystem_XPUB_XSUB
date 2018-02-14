import zmq
from random import randrange
import time


# let publisher and subscriber both talk to the same port here
port = "5550"
# if len(sys.argv) > 1:
#     port =  sys.argv[1]
#     int(port)

#using a server to get all the registers???
context = zmq.Context()
print "Connecting to server..."
socket = context.socket(zmq.REQ)

socket.connect ("tcp://*:5550")

def getPublisher():
    while True:
        #  Wait for next request from client
        message = socket.recv()
        print "Received request: ", message
        time.sleep (1)
        socket.send("World from %s" % port)

def getSubscriber():

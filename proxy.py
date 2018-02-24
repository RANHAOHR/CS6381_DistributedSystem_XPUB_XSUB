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

# system and time
import os
import sys
import time
import threading
import zmq
from random import randrange

cur_strength = 0
pre_strength = 0
count = 0
num = 10

history_vec = []
strengh_vec = []
pubInd = 0
newSub = False
ownership = 0

max_ownership = 0

global_url = 0
gloabal_port = 0
def background_input():
    global newSub
    global global_url
    global gloabal_port
    while True:
        addr_input = raw_input()
        ip, port = addr_input.split()
        if len(addr_input) == 13:
            pub_url = "tcp://" + ip + ":" + port
            gloabal_port = port
            global_url = pub_url
            newSub = True

# Get the context
context = zmq.Context()

# This is a proxy. We create the XSUB and XPUB endpoints
#print ("This is proxy: creating xsub and xpubsockets")
xsubsocket = context.socket(zmq.XSUB)
xsubsocket.bind("tcp://*:5555")

xpubsocket = context.socket (zmq.XPUB)
xpubsocket.setsockopt(zmq.XPUB_VERBOSE, 1)
xpubsocket.bind ("tcp://*:5556")
#here should bind all possible ports

xpubsocket.send_multipart([b'\x01', b'10001'])
# xsubsocket.send_multipart([b'\x01', b'10001'])

# Now we are going to create a poller
poller = zmq.Poller ()
poller.register (xsubsocket, zmq.POLLIN)
poller.register (xpubsocket, zmq.POLLIN)

# now threading1 runs regardless of user input
threading1 = threading.Thread(target=background_input)
threading1.daemon = True
threading1.start()

while True:
        events = dict (poller.poll (10000))
        # Is there any data from publisher?
        if xsubsocket in events:
            msg = xsubsocket.recv_multipart()
            #print ("Publication = {}".format (msg))
            content= msg[0]
            zipcode, temperature, relhumidity, ownership, history = content.split(" ")
            #print("all possible ownership", ownership)
            ownership = int(ownership.decode('ascii'))
            history = int(history.decode('ascii'))

            # creat the history stock for each publisher, should be FIFO
            if ownership not in strengh_vec:
                pubInd += 1 # the actual size of the publishers
                strengh_vec.append(ownership)
                #create list for this publisher
                history_vec.append([])
                if len(history_vec[pubInd-1]) < history:
                    history_vec[pubInd-1].append(msg)
                else:
                    history_vec[pubInd-1].pop(0)
                    history_vec[pubInd-1].append(msg)
            else:
                curInd = strengh_vec.index(ownership)
                if len(history_vec[curInd]) < history:
                    history_vec[curInd].append(msg)
                else:
                    history_vec[curInd].pop(0)
                    history_vec[curInd].append(msg)
            #print("history_vec",history_vec)
            if newSub:
                ctx = zmq.Context()
                pub = ctx.socket(zmq.PUB)
                pub.bind(global_url)
                if ownership == max(strengh_vec):
                    curInd = strengh_vec.index(ownership)
                    time.sleep(0.5)
                    for i in range(len(history_vec[curInd])):
                        # print("sending:",history_vec[curInd])
                        pub.send_multipart (history_vec[curInd][i])
                        # pub.send_multipart(['10001, 0, 0, 0, 0'])
                        time.sleep(0.1)
                pub.unbind(global_url)
                pub.close()
                ctx.term()
                xurl = "tcp://*:" + gloabal_port
                xpubsocket.bind(xurl)
                newSub = False
            else:
                #send the current message
                if ownership > cur_strength:
                    pre_strength = cur_strength
                    cur_strength = ownership
                    xpubsocket.send_multipart (msg)
                    count = 0
                elif ownership == cur_strength:
                    xpubsocket.send_multipart (msg)
                    count = 0
                else:
                    count = count +1
                    if count>= num:
                        cur_strength = pre_strength
                        count = 0
                        print("nothing happened")


        if xpubsocket in events:
            msg = xpubsocket.recv_multipart()
            # parse the incoming message
            #print ("subscription = {}".format (msg))
            # send the subscription info to publishers
            # if msg[0] == '\x0110001':
            #     # topic = msg[1:]
            #     newSub = True
            #     #print "Topic: new subscriber"
            # else:
            #     newSub = False
                #print "Topic: subscriber left"

            xsubsocket.send_multipart(msg)

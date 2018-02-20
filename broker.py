import os
import string
import sys
import time
from random import randint
import zmq
from time import sleep

def subscriber(socket, zip_filter, history, msg):
    # Process 5 updates
    print("in subscriber")
    total_temp = 0
    history = int(history)
    print("history", history)
    for update_nbr in range(history):
        pass
        # string = socket.recv_string()
        print("get something", string);
        zipcode, temperature, relhumidity = msg[:3]
        total_temp += int(temperature)
        print("temperature is:", temperature)

    print("Average temperature for zipcode '%s' was %dF" % (
        zip_filter, total_temp / (update_nbr+1))
          )

def main():

    if len(sys.argv) > 1:
        srv_addr =  sys.argv[1]

    if len(sys.argv) > 2:
        port =  sys.argv[2]
        int(port)

    xsub_url = "tcp://" + srv_addr + ":" + port

    srv_addr2 = "localhost"
    port2 = "5557"
    if len(sys.argv) > 3:
        srv_addr2 =  sys.argv[3]

    if len(sys.argv) > 4:
        port2 =  sys.argv[4]
        int(port2)

    xsub_url2 = "tcp://" + srv_addr2 + ":" + port2

    # Sockets to talk to servers
    context = zmq.Context()

    socket  = context.socket( zmq.SUB )
    socket.connect( xsub_url)
    socket2  = context.socket( zmq.SUB )
    socket2.connect( xsub_url2)

    # Set filters
    socket.setsockopt_string(  zmq.SUBSCRIBE, "topic".decode( 'ascii' ) )
    socket2.setsockopt_string( zmq.SUBSCRIBE, "topic".decode( 'ascii' ) )

    poller = zmq.Poller()
    poller.register( socket,  zmq.POLLIN )
    poller.register( socket2, zmq.POLLIN )

    zip_filter = "topic".decode( 'ascii' )
    # # Set filters
    # if isinstance(zip_filter, bytes):
    #     zip_filter = zip_filter.decode('ascii')
    
    print"routing info..."
    while True:
        socks = dict( poller.poll(1000) )
        cur_strength = 0
        print("poll socks", socks)
        if socket in socks and socks[socket] == zmq.POLLIN :
            [ content, topic, ownStrength, history,zipcode,temperature, relhumidity] = socket.recv_multipart()
            print content
            print ownStrength
            ownStrength = ownStrength.decode('ascii')
            history = history.decode('ascii')
            zipcode = zipcode.decode('ascii')
            temperature = temperature.decode('ascii')
            relhumidity = relhumidity.decode('ascii')
            msg = [zipcode, temperature, relhumidity]
            if ownStrength > cur_strength:
                cur_strength = ownStrength
                subscriber(socket, zip_filter, history, msg) # subscribe to this socket
            else:
                print("nothing happened")

            # if content == "ownership_strength":
            #     value = value.decode('ascii')
            #     if value > cur_strength:
            #         cur_strength = value
            #         subscriber(socket, zip_filter) # subscribe to this socket
            #     else:
            #         print("nothing happened")

        sleep(1)

if __name__ == "__main__":
    main()
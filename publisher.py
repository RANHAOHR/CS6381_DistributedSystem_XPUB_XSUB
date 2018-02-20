import zmq
from random import randrange
import sys
from time import sleep

print("Current libzmq version is %s" % zmq.zmq_version())
print("Current  pyzmq version is %s" % zmq.__version__)

def main():

    # Default value
    topic  = 10001
    ownership_strength = 2
    history = 1

    if len(sys.argv) > 1:
        srv_addr =  sys.argv[1]

    if len(sys.argv) > 2:
        port =  sys.argv[2]
        int(port)

    if len(sys.argv) > 3:
        ownership_strength =  sys.argv[3]
        int(ownership_strength)


    xpub_url = "tcp://" + srv_addr + ":" + port
    # Server socket
    context = zmq.Context()
    socket  = context.socket( zmq.XPUB )
    socket.bind( xpub_url )

    while True:
        zipcode = randrange(1, 100000)
        temperature = randrange(-80, 135)
        relhumidity = randrange(10, 60)
        # socket.send_string("%i %i %i" % (zipcode, temperature, relhumidity))

        socket.send_multipart( [ "topic", str(topic), str(ownership_strength), str(history), str(zipcode), str(temperature), str(relhumidity) ] )
        # socket.send_multipart( [ "ownership_strength", str(ownership_strength) ])
        # socket.send_multipart( [ "history", str(history) ])

        print("publishing!")
        sleep( 1 )

if __name__ == "__main__":
    main()
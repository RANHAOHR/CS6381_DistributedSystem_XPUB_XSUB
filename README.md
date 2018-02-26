# CS6381_Distributed_System_XPUB_XSUB

A package for Publish-Subscribe using ZMQ and Mininet, build for CS6381 Distributed System assignment#1.
The package builds a small layer of middleware on top of XPUB/XSUB to support anonymity, OWNERSHIP_STRENGTH and HISTORY.

## Collaborators

Ran Hao (rxh349@case.edu) Xiaodong Yang (xiaodong.yang@vanderbilt.edu) Tong Liang (liangtong39@gmail.com)

##### Run the bash file for installation of Mininet and ZMQ:
Go to the package directory and run
`chmod +x setup_mininetZMQ.sh` and `./setup_mininetZMQ.sh github_username github_email`

#### Run the broker on any host by

`python proxy.py`

#### Run any publisher by

`python publisher.py "address of the broker node" "OWNERSHIP_STRENGTH"`
The history of the publisher is set to 3, the default OWNERSHIP_STRENGTH is set to 2.

#### Run the first subscriber by

`python subscriber.py "address of the broker node"`

#### When running additional subscribers, run

`python subscriber.py "address of the broker node" "port of the subscriber"`

And please indicate the port for the broker: type in the address of the broker and the port number of the subscriber in the broker host window, for example,
when running the broker on host 3,  running the 2nd subscriber on host 5:

#### Run
`python subscriber1.py 10.0.0.3 1000`
and type: `10.0.0.3 1000` on the broker's window:

![Alt text](/images/subscriber.png?raw=true)

![Alt text](/images/broker.png?raw=true)

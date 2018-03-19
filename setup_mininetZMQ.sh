#/bin/bash
#RH 2018, for CS6381
USERNAME=$1
EMAIL=$2

if [ "$USERNAME" != "" ] || [ "$EMAIL" != "" ];
then
  echo "Install Mininet."
  sudo apt-get install mininet
  sudo mn -c

  echo "Install git."
  sudo apt-get install git

  git config --global user.email "EMAIL"
  git config --global user.name "USERNAME"
  
  echo "Config Mininet."
  git clone https://github.com/mininet/mininet.git
  sudo apt-get install net-tools
  mininet/util/install.sh –a

  echo "Install Pip and ZeroMQ."
  sudo apt-get install python-pip python-dev build-essential
  sudo pip install --upgrade pip
  sudo pip install --upgrade virtualenv

  sudo pip install pyzmq

else
  echo "USAGE: ./setup_mininetZMQ.sh github_username github_email"
fi

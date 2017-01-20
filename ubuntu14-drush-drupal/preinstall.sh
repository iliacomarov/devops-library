#!/bin/bash

sudo apt-get update

# checking and installation virtualbox
dpkg -l | grep virtualbox 1> /dev/null
rc=$?;
if [ $rc != 0 ]; then
   cd /tmp && wget http://download.virtualbox.org/virtualbox/5.1.14/virtualbox-5.1_5.1.14-112924~Ubuntu~trusty_amd64.deb && sudo dpkg -i virtualbox-5.1_5.1.14-112924~Ubuntu~trusty_amd64.deb;
else
   echo "virtualbox is installed";
fi

# checking and installation vagrant
dpkg -l | grep vagrant 1> /dev/null
rc2=$?;
if [ $rc2 != 0 ]; then
   cd /tmp && wget https://releases.hashicorp.com/vagrant/1.9.1/vagrant_1.9.1_x86_64.deb && sudo dpkg -i vagrant_1.9.1_x86_64.deb;
else
   echo "vagrant is installed";
fi

# installation necessary libraries of python
sudo apt-get install -y python-pip pithon-unipath
sudo pip install fabric fabtools

# start vagrant
vagrant up

#sudo echo "192.168.33.111 demo.loc" >> /etc/hosts


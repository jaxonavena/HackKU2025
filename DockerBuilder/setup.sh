#!/bin/bash
echo 'Setting up your environment...'
apt-get update
apt-get install -y cmake g++ pkg-config libjson-c-dev libwebsockets-dev git make
git clone https://github.com/tsl0922/ttyd.git /tmp/ttyd
cd /tmp/ttyd
mkdir build && cd build
cmake ..
make && make install

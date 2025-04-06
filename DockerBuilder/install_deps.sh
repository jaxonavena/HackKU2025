#!/usr/bin/env bash

set -e  # Exit immediately on error
echo "Updating package lists..."
apt-get update

echo "Installing Python 3 + pip..."
apt-get install -y python3 python3-pip

echo "Installing ttyd..."
apt-get install -y cmake g++ pkg-config libjson-c-dev libwebsockets-dev git make

git clone https://github.com/tsl0922/ttyd.git /tmp/ttyd
cd /tmp/ttyd
mkdir build && cd build
cmake ..
make && make install

echo "All dependencies installed successfully!"
#!/usr/bin/env bash
set -e

echo "Updating package lists..."
apt-get update

echo "Installing build tools, Python & pip..."
apt-get install -y python3 python3-pip python3-dev build-essential

echo "Installing Python packages..."
pip3 install numpy flask

echo "Installing Node.js & npm..."
curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
apt-get install -y nodejs
python3 app.py &
echo "Installing ttyd build dependencies..."
apt-get install -y cmake g++ pkg-config libjson-c-dev libwebsockets-dev git make

echo "Cloning and building ttyd..."
git clone https://github.com/tsl0922/ttyd.git /tmp/ttyd
cd /tmp/ttyd
mkdir build && cd build
cmake ..
make && make install

echo "Cleaning up..."
rm -rf /tmp/ttyd

echo "All dependencies installed!"
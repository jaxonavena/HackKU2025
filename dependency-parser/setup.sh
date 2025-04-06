#!/bin/bash
echo 'Setting up your environment...'
sudo apt-get update
apt-get install -y cmake g++ pkg-config libjson-c-dev libwebsockets-dev git make
git clone https://github.com/tsl0922/ttyd.git /tmp/ttyd
cd /tmp/ttyd
mkdir build && cd build
cmake ..
make && make install
sudo apt-get install -y build-essential
sudo apt-get install -y curl
sudo apt-get install -y python3.9 
python3.9 -m pip install jupyter line_profiler matplotlib==1.5.1 memory_profiler netcdf4 notebook numexpr numpy==1.11.1 pandas-datareader pandas==0.18.1 pillow==3.4.2 scikit-image==0.12.3 scikit-learn==0.17.1 scipy==0.17.1 seaborn==0.7.0

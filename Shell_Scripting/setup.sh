#!/bin/bash
echo 'Setting up your environment...'
sudo apt-get update
sudo apt-get install -y system_packages
sudo apt-get install -y python3.9
python3.9 -m pip install requests==2.25.1 flask==2.0.1
sudo apt-get install -y node16.x
node16.x npm install express axios

#!/usr/bin/env bash

set -e  # Exit immediately on error

# 1. Base environment setup
echo "Updating package lists..."
apt-get update

echo "Installing system packages..."
apt-get install -y build-essential curl

# 2. Language: Python (version 3.9)
echo "Installing Python 3.9..."
# (In a real script, you'd add a PPA or use system repositories for Python 3.9)
apt-get install -y python3.9 python3.9-distutils python3-pip

echo "Installing Python packages..."
pip3 install requests==2.25.1 flask==2.0.1

# 3. Language: Node (version 16.x)
echo "Installing Node.js 16.x..."
curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
apt-get install -y nodejs

echo "Installing Node packages..."
npm install express axios

echo "All dependencies installed successfully!"

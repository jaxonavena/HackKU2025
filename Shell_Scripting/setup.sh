#!/bin/bash
echo 'Setting up your environment...'
sudo apt-get update
sudo apt-get install -y build-essential
sudo apt-get install -y curl
sudo apt-get install -y python3.9
python3.9 -m pip install requests==2.25.1 flask==2.0.1 numpy==1.21.0 pandas==1.3.0
sudo apt-get install -y nodejs npm
npm install express axios lodash react
sudo apt-get install -y ruby
gem install rails sinatra rake
sudo apt-get install -y java
mvn install spring-boot hibernate junit log4j
sudo apt-get install -y gcc g++
sudo apt-get install libc6-dev libssl-dev build-essential
sudo apt-get install -y gcc g++
sudo apt-get install libstdc++-8-dev libboost-all-dev g++ cmake
sudo apt-get install -y rust
cargo install tokio serde actix-web rocket
sudo apt-get install -y golang
go get gorilla/mux gin-gonic/gin golang/x/tools protobuf
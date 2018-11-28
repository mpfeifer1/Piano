#!/usr/bin/env bash

# This script is only for ubuntu linux

# if any command inside script returns error, exit and return that error 
set -e

echo "-----Installing Hooks Script-----"
./install-hooks.bash
echo "-----Installing Python3-----"
sudo apt-get install python3
echo "-----Installing Pip3-----"
sudo apt-get install python3-pip
echo "-----Installing Mido-----"
pip3 install mido
echo "-----Installing Lark-----"
pip3 install lark
echo "-----Installing Lark Parser-----"
pip3 install lark-parser

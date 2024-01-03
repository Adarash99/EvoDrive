#!/bin/bash


sudo pip uninstall -y timm
cd ./../leaderboard/interfuser
sudo python3.7 setup.py develop -d /usr/local/lib/python3.7/dist-packages
cd ../

#!/bin/bash

cd ~
wget https://github.com/NREL/EnergyPlus/releases/download/v8.7.0/EnergyPlus-8.7.0-78a111df4a-Linux-x86_64.sh
chmod 770 EnergyPlus-8.7.0-78a111df4a-Linux-x86_64.sh
sudo ./EnergyPlus-8.7.0-78a111df4a-Linux-x86_64.sh

exit
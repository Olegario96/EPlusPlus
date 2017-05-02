#!/bin/bash

PARENT_COMMAND="$(ps -o comm=$PPID)"

cd ~
sudo apt-get install sqlitebrowser
if [ $? -eq 0 ]; then
	exit
fi

sudo pacman -S sqlitebrowser
if [ $? -eq 0 ]; then
	exit
fi

sudo dnf install sqlitebrowser
if [ $? -eq 0 ]; then
	exit
fi

echo "IT WASN'T POSSIBLE TO INSTALL sqlitebrowser!"
sleep 5
kill -9 $PARENT_COMMAND
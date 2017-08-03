#!/bin/bash
#defined file paths
CURRENT_DIR=$pwd
SCRIPT_DIR=$(dirname $0)
SCRIPT_NAME=argparse.py
version=2.6
LIB_DIR=/usr/lib/python$version

#Main script
if [ ! -e $LIB_DIR/$SCRIPT_NAME ]; then
	echo "Script not found...proceed to installation"
	cp $SCRIPT_DIR/SCRIPT_NAME $LIB_DIR
	echo "Installation completed"
else
	echo "Script found...no installation required"
	
fi

#!/bin/bash

if [ $# -eq 2 ]; 
	then
	
	python2.7 q_1.py "$1" "$2"
fi

if [ $# -eq 1 ];
	then
	python2.7 q_2.py "$1"
fi
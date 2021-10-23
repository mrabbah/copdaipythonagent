#!/bin/bash

. install/setup.bash  

echo "Number of listners to run = $1 "

for i in $(seq "$1"); do
	ros2 run py_pubsub listener "listner$i" &
done

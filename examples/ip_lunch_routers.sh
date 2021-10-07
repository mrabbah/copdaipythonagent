#!/bin/bash

echo "Number of nodes to run = $1 "

for i in $(seq "$1"); do
    ./routers_ip.py "$i" &
    PID=$(pgrep -f "routers_ip.py $i")
    echo "router $i process id = $PID"
    chrt -f -p 99 "$PID"
done

#!/bin/bash

# launch carla world
$CARLA_ROOT/CarlaUE4.sh -quality-level=low -world-port=$PORT -resx=800 -resy=600 &
#$CARLA_ROOT/CarlaUE4.sh -quality-level=low -world-port=$PORT -RenderOffScreen &
PID=$!
echo "Carla PID=$PID"

sleep 10

echo "carla running"

#!/bin/bash


##################################
kill -9 -1
##################################


export ROOT=/EvoDrive
export CARLA_ROOT=/Carla
export LEADERBOARD_ROOT=/${ROOT}/leaderboard
export SCENARIO_RUNNER_ROOT=/${ROOT}/scenario_runner
export CARLA=/EvoDrive/

export PORT=2000
export ROUTES=${LEADERBOARD_ROOT}/data/routes_devtest.xml 


export PYTHONPATH="${SCENARIO_RUNNER_ROOT}":"${LEADERBOARD_ROOT}":"${CARLA_ROOT}/PythonAPI/carla":$PYTHONPATH
export PYTHONPATH="${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.14-py3.7-linux-x86_64.egg":$PYTHONPATH

# launch carla world
$CARLA_ROOT/CarlaUE4.sh -quality-level=low -world-port=$PORT -resx=800 -resy=600 &
PID=$!
echo "Carla PID=$PID"

sleep 10

echo "carla running"

#!/bin/bash


##################################
kill -9 -1
xhost +

##################################


export ROOT=/CTESTER
export CARLA_ROOT=/CARLA
export LEADERBOARD_ROOT=/${ROOT}/leaderboard
export SCENARIO_RUNNER_ROOT=/${ROOT}/scenario_runner


##################################
sudo chown -R carla ${LEADERBOARD_ROOT} ${SCENARIO_RUNNER_ROOT}
#sudo chown -R carla ${CARLA_ROOT}
##################################


export PORT=2000
export ROUTES=${LEADERBOARD_ROOT}/data/routes_devtest.xml 
#export ROUTES=${LEADERBOARD_ROOT}/data/routes_testing.xml 
#export ROUTES=${LEADERBOARD_ROOT}/data/routes_validation.xml 
export REPETITIONS=1
export DEBUG_CHALLENGE=1
export TEAM_AGENT=${LEADERBOARD_ROOT}/leaderboard/autoagents/human_agent.py
#export TEAM_AGENT=${LEADERBOARD_ROOT}/team_code/interfuser_agent.py
#export TEAM_CONFIG=${LEADERBOARD_ROOT}/team_code/interfuser_config.py
export CHECKPOINT_ENDPOINT=${LEADERBOARD_ROOT}/results.json
export CHALLENGE_TRACK_CODENAME=SENSORS

export PYTHONPATH="${SCENARIO_RUNNER_ROOT}":"${LEADERBOARD_ROOT}":"${CARLA_ROOT}/PythonAPI/carla":$PYTHONPATH
export PYTHONPATH="${CARLA_ROOT}/PythonAPI/carla/dist/carla-0.9.14-py3.7-linux-x86_64.egg":$PYTHONPATH

# launch carla world
$CARLA_ROOT/CarlaUE4.sh -quality-level=low -world-port=$PORT -resx=800 -resy=600 &
PID=$!
echo "Carla PID=$PID"

sleep 10

echo "carla running"